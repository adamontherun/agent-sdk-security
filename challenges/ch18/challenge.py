"""Chapter 18 challenge — audit an ECS task definition's security posture.

The Terraform in this chapter encodes a specific posture: the agent task carries
a scoped task role that is not the execution role, no container runs privileged,
and secrets arrive through ECS's `secrets` field (a Secrets Manager / SSM ARN
resolved at start) rather than sitting in plaintext `environment` entries.

Write `audit_task_definition` to catch a task definition that violates any of
those rules. It takes a parsed task-definition dict (the shape
`aws ecs register-task-definition` accepts) and returns a sorted list of
finding codes. An empty list means the definition passes.

Emit these codes:

  "missing_task_role"       - no `taskRoleArn`.
  "missing_execution_role"  - no `executionRoleArn`.
  "shared_role"             - `taskRoleArn` equals `executionRoleArn`
                              (the two roles must stay separate; the execution
                              role is for the ECS agent, the task role is for
                              the running container).
  "privileged_container"    - any container definition with `privileged` true.
  "plaintext_secret"        - any container with an `environment` entry whose
                              name looks like a secret. Treat a name as a
                              secret if, upper-cased, it contains any of
                              SECRET, TOKEN, PASSWORD, or ends in _KEY or is
                              exactly API_KEY. `ANTHROPIC_API_KEY` and
                              `DB_PASSWORD` should trip this; `LOG_LEVEL` and
                              `HTTPS_PROXY` should not.

Each code appears at most once, even if several containers trip the same rule.
"""

SECRET_SUBSTRINGS = ("SECRET", "TOKEN", "PASSWORD")


def audit_task_definition(task_def: dict) -> list[str]:
    """Return a sorted list of unique finding codes for the task definition."""
    raise NotImplementedError()
