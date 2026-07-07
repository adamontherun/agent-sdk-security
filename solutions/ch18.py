"""Chapter 18 reference solution — audit an ECS task definition's posture."""

SECRET_SUBSTRINGS = ("SECRET", "TOKEN", "PASSWORD")


def _looks_like_secret(name: str) -> bool:
    upper = name.upper()
    if any(sub in upper for sub in SECRET_SUBSTRINGS):
        return True
    return upper.endswith("_KEY") or upper == "API_KEY"


def audit_task_definition(task_def: dict) -> list[str]:
    findings: set[str] = set()

    task_role = task_def.get("taskRoleArn")
    exec_role = task_def.get("executionRoleArn")
    if not task_role:
        findings.add("missing_task_role")
    if not exec_role:
        findings.add("missing_execution_role")
    if task_role and exec_role and task_role == exec_role:
        findings.add("shared_role")

    for container in task_def.get("containerDefinitions", []):
        if container.get("privileged"):
            findings.add("privileged_container")
        for entry in container.get("environment", []):
            if _looks_like_secret(entry.get("name", "")):
                findings.add("plaintext_secret")

    return sorted(findings)
