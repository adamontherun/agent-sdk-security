#!/usr/bin/env bash
# The MicroVM lifecycle, in the CLI verbs that have no Terraform equivalent.
# Flags here are copied from `aws lambda-microvms <cmd> help` on aws-cli
# 2.35.15; run those help commands yourself to confirm before an apply. This
# script is a reference, not a turnkey deploy: it needs AWS credentials and the
# Terraform outputs from ../terraform, and it stops short of any destructive
# call you have not reviewed.
set -euo pipefail

REGION="${AWS_REGION:-us-east-1}"
NAME="agent-microvm"

# Build-time inputs. BUILD_ROLE_ARN and ARTIFACT_BUCKET come from the Terraform
# in ../terraform (`terraform output`). BASE_IMAGE_ARN is a Lambda-managed base
# image; list them first.
aws lambda-microvms list-managed-microvm-images --region "$REGION"

BASE_IMAGE_ARN="${BASE_IMAGE_ARN:?set to an ARN from the list above}"
BUILD_ROLE_ARN="${BUILD_ROLE_ARN:?terraform output build_role_arn}"
EXEC_ROLE_ARN="${EXEC_ROLE_ARN:?terraform output execution_role_arn}"
ARTIFACT_URI="${ARTIFACT_URI:?s3://your-bucket/agent.zip}"

# 1. Build the image. Lambda runs your Dockerfile, initializes the app, and
#    snapshots memory and disk. The build is async: the image goes CREATING ->
#    CREATED. --code-artifact is a tagged union whose only key is uri.
IMAGE_ID=$(aws lambda-microvms create-microvm-image \
  --region "$REGION" \
  --name "$NAME" \
  --base-image-arn "$BASE_IMAGE_ARN" \
  --build-role-arn "$BUILD_ROLE_ARN" \
  --code-artifact "uri=$ARTIFACT_URI" \
  --resources 'minimumMemoryInMiB=2048' \
  --query 'imageId' --output text)

# 2. Poll the build to CREATED before launching anything from it.
aws lambda-microvms get-microvm-image \
  --region "$REGION" \
  --image-identifier "$IMAGE_ID"

# 3. Launch a MicroVM. Every launch resumes from the snapshot instead of cold
#    booting. The idle policy auto-suspends after 15 min idle and auto-resumes
#    on the next request; the runtime is capped at the 8-hour platform maximum
#    (28,800 s). See examples' build_run_request() for the validated body.
MICROVM_ID=$(aws lambda-microvms run-microvm \
  --region "$REGION" \
  --image-identifier "$IMAGE_ID" \
  --execution-role-arn "$EXEC_ROLE_ARN" \
  --idle-policy 'maxIdleDurationSeconds=900,suspendedDurationSeconds=300,autoResumeEnabled=true' \
  --maximum-duration-in-seconds 28800 \
  --query 'microvmId' --output text)

# 4. Mint a short-lived token scoped to one port, then reach the MicroVM with it
#    in the X-aws-proxy-auth header. Tokens expire in at most 60 minutes.
TOKEN=$(aws lambda-microvms create-microvm-auth-token \
  --region "$REGION" \
  --microvm-identifier "$MICROVM_ID" \
  --expiration-in-minutes 15 \
  --allowed-ports 'port=8080' \
  --query 'token' --output text)

# The endpoint URL comes from get-microvm; the token authenticates the request.
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

echo "MicroVM $MICROVM_ID running from image $IMAGE_ID"
