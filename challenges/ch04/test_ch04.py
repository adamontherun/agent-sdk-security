"""Tests for Chapter 4 — the permission evaluation pipeline model."""


def _call(**kw):
    base = {
        "hook_decision": None,
        "deny_match": False,
        "ask_match": False,
        "mode": "default",
        "allow_match": False,
        "is_file_op": False,
        "can_use_tool": lambda: "allow",
    }
    base.update(kw)
    return base


def test_deny_beats_a_hook_allow(subject):
    # A PreToolUse hook returning "allow" does not skip the deny rules.
    assert subject.evaluate(_call(hook_decision="allow", deny_match=True)) == "deny"


def test_deny_beats_bypass_permissions(subject):
    assert subject.evaluate(_call(deny_match=True, mode="bypassPermissions")) == "deny"


def test_ask_still_prompts_under_bypass(subject):
    assert subject.evaluate(_call(ask_match=True, mode="bypassPermissions")) == "ask"


def test_ask_becomes_deny_in_dontask(subject):
    assert subject.evaluate(_call(ask_match=True, mode="dontAsk")) == "deny"


def test_bypass_approves_when_no_deny_or_ask(subject):
    assert subject.evaluate(_call(mode="bypassPermissions")) == "allow"


def test_accept_edits_approves_file_op(subject):
    assert subject.evaluate(_call(mode="acceptEdits", is_file_op=True)) == "allow"


def test_accept_edits_does_not_approve_non_file_op(subject):
    # A non-file Bash command in acceptEdits falls through to the callback.
    assert subject.evaluate(_call(mode="acceptEdits", is_file_op=False)) == "allow"


def test_plan_routes_writes_to_callback_despite_allow(subject):
    # Even with an allow rule, plan mode never auto-approves a write.
    called = {"n": 0}

    def cb():
        called["n"] += 1
        return "ask"

    out = subject.evaluate(_call(mode="plan", is_file_op=True, allow_match=True, can_use_tool=cb))
    assert out == "ask"
    assert called["n"] == 1


def test_allow_rule_approves(subject):
    assert subject.evaluate(_call(allow_match=True)) == "allow"


def test_falls_through_to_callback(subject):
    assert subject.evaluate(_call(can_use_tool=lambda: "deny")) == "deny"


def test_dontask_skips_callback(subject):
    def cb():
        raise AssertionError("callback must not run in dontAsk mode")

    assert subject.evaluate(_call(mode="dontAsk", can_use_tool=cb)) == "deny"


def test_shadow_bypass(subject):
    assert subject.can_use_tool_reachable("bypassPermissions", [], "Bash") is False


def test_shadow_bare_allow_entry(subject):
    assert subject.can_use_tool_reachable("default", ["Read"], "Read") is False


def test_scoped_allow_entry_does_not_shadow(subject):
    assert subject.can_use_tool_reachable("default", ["Bash(ls *)"], "Bash") is True


def test_unrelated_allow_entry_does_not_shadow(subject):
    assert subject.can_use_tool_reachable("default", ["Read"], "Bash") is True
