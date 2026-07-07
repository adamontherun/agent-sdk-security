def test_fully_hardened_has_no_violations(subject):
    config = {
        "filesystem_writable_root": False,
        "network_unrestricted": False,
        "credentials_in_agent_env": False,
        "linux_caps_dropped": True,
    }
    assert subject.review_least_privilege(config) == []


def test_wide_open_flags_all_four(subject):
    config = {
        "filesystem_writable_root": True,
        "network_unrestricted": True,
        "credentials_in_agent_env": True,
        "linux_caps_dropped": False,
    }
    assert subject.review_least_privilege(config) == [
        "credentials",
        "filesystem",
        "network",
        "system_capabilities",
    ]


def test_missing_keys_default_to_worst_case_for_caps(subject):
    # An empty config: caps were never dropped, so that is the one violation.
    assert subject.review_least_privilege({}) == ["system_capabilities"]


def test_result_is_sorted(subject):
    config = {"network_unrestricted": True, "credentials_in_agent_env": True}
    result = subject.review_least_privilege(config)
    assert result == sorted(result)
    assert "network" in result
    assert "credentials" in result
