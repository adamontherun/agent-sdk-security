#!/usr/bin/env bash
# The MicroVM lifecycle, in the CLI verbs that have no Terraform equivalent.
# This whole sequence was run end to end against a real account (aws-cli
# 2.35.15) while writing chapter 19, so the flags and query expressions below
# are the ones that actually worked, not just the help-text synopsis. It still
# needs AWS credentials and the Terraform outputs from ../terraform, and it
# stops short of any destructive call you have not reviewed.
#
# Two things the help text alone would not have told you: get-microvm-image and
# get-microvm want the resource ARN, not the bare name (the name returns
# "Invalid ARN format"); and reachability comes from the managed ingress/egress
# network connectors on run-microvm, not from the optional --execution-role-arn.
set -euo pipefail

REGION="${AWS_REGION:-us-east-1}"
NAME="agent-microvm"
CONN="arn:aws:lambda:${REGION}:aws:network-connector:aws-network-connector"

# Build-time inputs. BUILD_ROLE_ARN and ARTIFACT_URI come from the Terraform in
# ../terraform (`terraform output`). BASE_IMAGE_ARN is a Lambda-managed base
# image; list them first. The build role must be assumable by
# lambda.amazonaws.com with BOTH sts:AssumeRole and sts:TagSession, or the build
# fails; the Terraform trust policy already includes both.
aws lambda-microvms list-managed-microvm-images --region "$REGION"

BASE_IMAGE_ARN="${BASE_IMAGE_ARN:?set to an ARN from the list above}"
BUILD_ROLE_ARN="${BUILD_ROLE_ARN:?terraform output build_role_arn}"
ARTIFACT_URI="${ARTIFACT_URI:?s3://your-bucket/agent.zip}"

# 1. Build the image. Lambda runs your Dockerfile, initializes the app, and
#    snapshots memory and disk. The build is async: the image goes CREATING ->
#    CREATED. --code-artifact is a tagged union whose only key is uri. The
#    response returns imageArn, which is the identifier every later call needs.
IMAGE_ARN=$(aws lambda-microvms create-microvm-image \
  --region "$REGION" \
  --name "$NAME" \
  --base-image-arn "$BASE_IMAGE_ARN" \
  --build-role-arn "$BUILD_ROLE_ARN" \
  --code-artifact "uri=$ARTIFACT_URI" \
  --resources 'minimumMemoryInMiB=2048' \
  --query 'imageArn' --output text)

# 2. Poll the build to CREATED before launching anything from it. Identify the
#    image by its ARN; the bare name is rejected as an invalid ARN.
until [ "$(aws lambda-microvms get-microvm-image --region "$REGION" \
  --image-identifier "$IMAGE_ARN" --query 'state' --output text)" = "CREATED" ]; do
  sleep 15
done

# 3. Launch a MicroVM. Every launch resumes from the snapshot instead of cold
#    booting. The two managed network connectors are what make it reachable:
#    ALL_INGRESS lets HTTPS in, INTERNET_EGRESS lets the app reach out. The idle
#    policy auto-suspends after 15 min idle and auto-resumes on the next request;
#    the runtime is capped at the 8-hour platform maximum (28,800 s).
MICROVM_ID=$(aws lambda-microvms run-microvm \
  --region "$REGION" \
  --image-identifier "$IMAGE_ARN" \
  --ingress-network-connectors "${CONN}:ALL_INGRESS" \
  --egress-network-connectors "${CONN}:INTERNET_EGRESS" \
  --idle-policy '{"autoResumeEnabled":true,"maxIdleDurationSeconds":900,"suspendedDurationSeconds":300}' \
  --maximum-duration-in-seconds 28800 \
  --query 'microvmId' --output text)

until [ "$(aws lambda-microvms get-microvm --region "$REGION" \
  --microvm-identifier "$MICROVM_ID" --query 'state' --output text)" = "RUNNING" ]; do
  sleep 8
done

# 4. Mint a short-lived token, then reach the MicroVM with it in the
#    X-aws-proxy-auth header. Tokens expire in at most 60 minutes. The token
#    comes back under authToken, keyed by the header name it belongs in, so the
#    query is authToken."X-aws-proxy-auth", not token.
TOKEN=$(aws lambda-microvms create-microvm-auth-token \
  --region "$REGION" \
  --microvm-identifier "$MICROVM_ID" \
  --expiration-in-minutes 15 \
  --allowed-ports '[{"allPorts":{}}]' \
  --query 'authToken."X-aws-proxy-auth"' --output text)

# The endpoint URL comes from get-microvm; the token authenticates the request.
# A request with no token is answered 403.
ENDPOINT=$(aws lambda-microvms get-microvm \
  --region "$REGION" \
  --microvm-identifier "$MICROVM_ID" \
  --query 'endpoint' --output text)

curl --silent --show-error \
  --header "X-aws-proxy-auth: $TOKEN" \
  "https://${ENDPOINT}/health"

# 5. Suspend when idle to stop paying for compute while keeping full state, or
#    terminate to tear the session down. Uncomment when you mean it.
# aws lambda-microvms suspend-microvm   --region "$REGION" --microvm-identifier "$MICROVM_ID"
# aws lambda-microvms resume-microvm    --region "$REGION" --microvm-identifier "$MICROVM_ID"
# aws lambda-microvms terminate-microvm --region "$REGION" --microvm-identifier "$MICROVM_ID"

echo "MicroVM $MICROVM_ID running from image $IMAGE_ARN"
