def test_credential_never_in_agent_is_always_prevented(subject):
    # Injected at the proxy: the agent has nothing to leak.
    assert subject.proxy_pattern_prevents({"credential_in_agent": False}) is True
    assert (
        subject.proxy_pattern_prevents(
            {"credential_in_agent": False, "exfil_to_blocked_host": False}
        )
        is True
    )


def test_agent_holds_secret_but_exfil_blocked_is_prevented(subject):
    # The allowlist stops the request from leaving.
    assert (
        subject.proxy_pattern_prevents({"credential_in_agent": True, "exfil_to_blocked_host": True})
        is True
    )


def test_agent_holds_secret_and_can_reach_allowed_host_is_not_prevented(subject):
    # The one gap: the agent has the secret and an allowed egress path.
    assert (
        subject.proxy_pattern_prevents(
            {"credential_in_agent": True, "exfil_to_blocked_host": False}
        )
        is False
    )


def test_empty_scenario_defaults_to_prevented(subject):
    # No credential in the agent by default, so nothing to leak.
    assert subject.proxy_pattern_prevents({}) is True
