"""Chapter 14 reference solution — does the proxy pattern prevent this exposure?"""


def proxy_pattern_prevents(scenario: dict) -> bool:
    if not scenario.get("credential_in_agent", False):
        return True
    return bool(scenario.get("exfil_to_blocked_host", False))
