# The Anthropic API key lives in Secrets Manager, not in the task definition's
# environment and not baked into an image. ECS resolves the ARN at task start
# and injects the value; the plaintext never appears in the task definition,
# CloudFormation events, or `describe-task-definition` output.
resource "aws_secretsmanager_secret" "anthropic_api_key" {
  name        = "${var.name}/anthropic-api-key"
  description = "Anthropic API key, injected into the Squid sidecar at task start."
}

# The secret value is set out of band (console, CLI, or a separate pipeline),
# not committed here. This resource records that a version exists without
# putting a real key in state on every apply; replace the placeholder through
# `aws secretsmanager put-secret-value` after the first apply.
resource "aws_secretsmanager_secret_version" "anthropic_api_key" {
  secret_id     = aws_secretsmanager_secret.anthropic_api_key.id
  secret_string = "REPLACE_ME_OUT_OF_BAND"

  lifecycle {
    ignore_changes = [secret_string]
  }
}
