"""Tests for Chapter 8 — settings precedence and managed lockdown."""


def test_deny_from_any_scope_wins_over_allow(subject):
    scopes = {
        "managed": {"permissions": {"deny": ["Bash(curl *)"]}},
        "user": {"permissions": {"allow": ["Bash(curl *)", "Bash(npm *)"]}},
    }
    out = subject.resolve(scopes)
    assert "Bash(curl *)" in out["deny"]
    assert "Bash(curl *)" not in out["allow"]
    assert "Bash(npm *)" in out["allow"]


def test_allow_merges_across_scopes_by_default(subject):
    scopes = {
        "shared": {"permissions": {"allow": ["Bash(git *)"]}},
        "user": {"permissions": {"allow": ["Bash(npm *)"]}},
    }
    out = subject.resolve(scopes)
    assert set(out["allow"]) == {"Bash(git *)", "Bash(npm *)"}


def test_managed_only_drops_local_allow(subject):
    scopes = {
        "managed": {
            "permissions": {"allow": ["Bash(git *)"]},
            "allowManagedPermissionRulesOnly": True,
        },
        "user": {"permissions": {"allow": ["Bash(curl *)"]}},
    }
    out = subject.resolve(scopes)
    assert out["allow"] == ["Bash(git *)"]


def test_managed_only_drops_user_deny(subject):
    # allowManagedPermissionRulesOnly drops user/project allow, ask, AND deny
    # rules: only managed rules apply. A user deny does not survive it.
    scopes = {
        "managed": {
            "permissions": {"deny": ["Bash(curl *)"]},
            "allowManagedPermissionRulesOnly": True,
        },
        "user": {"permissions": {"deny": ["Bash(rm *)"]}},
    }
    out = subject.resolve(scopes)
    assert out["deny"] == ["Bash(curl *)"]
    assert "Bash(rm *)" not in out["deny"]


def test_deny_merges_across_scopes_without_flag(subject):
    # Without the flag, a developer can always tighten: a user deny merges in.
    scopes = {
        "managed": {"permissions": {"deny": ["Bash(curl *)"]}},
        "user": {"permissions": {"deny": ["Bash(rm *)"]}},
    }
    out = subject.resolve(scopes)
    assert set(out["deny"]) == {"Bash(curl *)", "Bash(rm *)"}


def test_default_mode_highest_scope_wins(subject):
    scopes = {
        "managed": {"defaultMode": "default"},
        "user": {"defaultMode": "acceptEdits"},
    }
    assert subject.resolve(scopes)["defaultMode"] == "default"


def test_default_mode_falls_back(subject):
    assert subject.resolve({"user": {}})["defaultMode"] == "default"


def test_disable_bypass_blocks_mode(subject):
    scopes = {
        "managed": {"disableBypassPermissionsMode": "disable"},
        "user": {"defaultMode": "bypassPermissions"},
    }
    out = subject.resolve(scopes)
    assert out["bypassAllowed"] is False
    assert out["defaultMode"] == "default"


def test_bypass_allowed_by_default(subject):
    assert subject.resolve({"user": {}})["bypassAllowed"] is True
