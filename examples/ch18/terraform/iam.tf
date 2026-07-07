# Two roles, two jobs. The execution role belongs to the ECS agent that starts
# the task: it pulls the image, writes logs, and resolves the secret ARN. The
# task role belongs to the running container. Keeping them separate means the
# permissions the platform needs to start the task are not handed to the code
# the agent runs.

data "aws_iam_policy_document" "ecs_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# --- Execution role: platform-side permissions only. ---
resource "aws_iam_role" "execution" {
  name               = "${var.name}-exec"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

resource "aws_iam_role_policy_attachment" "execution_managed" {
  role       = aws_iam_role.execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# The execution role reads exactly one secret: the Anthropic key, injected into
# the Squid sidecar. It is scoped to that ARN, not secretsmanager:* on "*".
data "aws_iam_policy_document" "execution_secrets" {
  statement {
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [aws_secretsmanager_secret.anthropic_api_key.arn]
  }
}

resource "aws_iam_role_policy" "execution_secrets" {
  name   = "${var.name}-exec-secrets"
  role   = aws_iam_role.execution.id
  policy = data.aws_iam_policy_document.execution_secrets.json
}

# --- Task role: what the agent's own process may do. ---
# Credentials are injected at the proxy, so the agent needs no AWS API access.
# The role exists (a task role is required to attribute actions) but carries no
# policies. Least privilege here means an empty policy set, not a broad one.
resource "aws_iam_role" "task" {
  name               = "${var.name}-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}
