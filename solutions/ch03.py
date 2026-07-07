"""Chapter 3 reference solution — review a deployment against least privilege."""


def review_least_privilege(config: dict) -> list[str]:
    violations = []
    if config.get("filesystem_writable_root"):
        violations.append("filesystem")
    if config.get("network_unrestricted"):
        violations.append("network")
    if config.get("credentials_in_agent_env"):
        violations.append("credentials")
    if not config.get("linux_caps_dropped"):
        violations.append("system_capabilities")
    return sorted(violations)
