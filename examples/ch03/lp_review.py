"""Review two deployment configs against the least-privilege table.

Run it:

    python examples/ch03/lp_review.py

The first config is a wide-open default; the second applies each row of the
least-privilege table. No Claude session or network access is needed.
"""


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


WIDE_OPEN = {
    "filesystem_writable_root": True,
    "network_unrestricted": True,
    "credentials_in_agent_env": True,
    "linux_caps_dropped": False,
}

HARDENED = {
    "filesystem_writable_root": False,
    "network_unrestricted": False,
    "credentials_in_agent_env": False,
    "linux_caps_dropped": True,
}


def main() -> None:
    for label, config in (("wide-open default", WIDE_OPEN), ("hardened", HARDENED)):
        violations = review_least_privilege(config)
        summary = ", ".join(violations) if violations else "none"
        print(f"{label:>18}: {len(violations)} violation(s) -> {summary}")


if __name__ == "__main__":
    main()
