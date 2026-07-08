# Two roles the MicroVM CLI calls reference by ARN:
#   * build role  -> passed to create-microvm-image as --build-role-arn; assumed
#                    while Lambda runs the Dockerfile and snapshots the result.
#                    It needs to read the code artifact from S3.
#   * exec role   -> passed to run-microvm as --execution-role-arn; assumed by
#                    the running MicroVM. Scoped to nothing beyond logs, since
#                    credentials reach the agent through the proxy, not the role.
#
# These roles are assumed by lambda.amazonaws.com with both sts:AssumeRole and
# sts:TagSession. That principal and the TagSession requirement were confirmed by
# running a real build while writing chapter 19: omitting sts:TagSession fails the
# build. Tighten the trust policy with an aws:SourceArn condition once the account
# and image ARNs are known, so only your own images can assume the role.

data "aws_iam_policy_document" "microvm_assume" {
  statement {
    actions = ["sts:AssumeRole", "sts:TagSession"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# --- Build role ---
resource "aws_iam_role" "build" {
  name               = "${var.name}-build"
  assume_role_policy = data.aws_iam_policy_document.microvm_assume.json
}

data "aws_iam_policy_document" "build_permissions" {
  statement {
    sid       = "ReadCodeArtifact"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.artifacts.arn}/*"]
  }

  statement {
    sid       = "WriteBuildLogs"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents", "logs:CreateLogGroup"]
    resources = ["arn:aws:logs:${var.aws_region}:*:log-group:/aws/lambda-microvms/*"]
  }
}

resource "aws_iam_role_policy" "build" {
  name   = "${var.name}-build"
  role   = aws_iam_role.build.id
  policy = data.aws_iam_policy_document.build_permissions.json
}

# --- Execution role ---
resource "aws_iam_role" "execution" {
  name               = "${var.name}-exec"
  assume_role_policy = data.aws_iam_policy_document.microvm_assume.json
}

data "aws_iam_policy_document" "execution_permissions" {
  statement {
    sid       = "WriteRuntimeLogs"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["arn:aws:logs:${var.aws_region}:*:log-group:/aws/lambda-microvms/*"]
  }
}

resource "aws_iam_role_policy" "execution" {
  name   = "${var.name}-exec"
  role   = aws_iam_role.execution.id
  policy = data.aws_iam_policy_document.execution_permissions.json
}
