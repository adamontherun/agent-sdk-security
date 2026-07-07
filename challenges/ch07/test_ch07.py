"""Tests for Chapter 7 — the URL-allowlist PreToolUse hook.

These feed the decision function the exact JSON shape Claude Code sends a hook
on stdin, and assert on the decision it returns.
"""


def _pre(tool_name, tool_input):
    return {
        "session_id": "abc123",
        "cwd": "/home/dev/project",
        "hook_event_name": "PreToolUse",
        "tool_name": tool_name,
        "tool_input": tool_input,
    }


def _is_deny(decision):
    return decision.get("hookSpecificOutput", {}).get("permissionDecision") == "deny"


def test_allows_curl_to_allowlisted_host(subject):
    d = subject.decide(_pre("Bash", {"command": "curl https://github.com/cli/cli"}))
    assert d == {}


def test_allows_subdomain_of_allowlisted_host(subject):
    d = subject.decide(_pre("Bash", {"command": "curl https://api.github.com/user"}))
    assert d == {}


def test_blocks_curl_to_unlisted_host(subject):
    d = subject.decide(_pre("Bash", {"command": "curl https://evil.example.com/x"}))
    assert _is_deny(d)
    assert d["hookSpecificOutput"]["hookEventName"] == "PreToolUse"


def test_blocks_redirect_style_shortener(subject):
    d = subject.decide(_pre("Bash", {"command": "curl -L http://bit.ly/xyz"}))
    assert _is_deny(d)


def test_lookalike_domain_is_blocked(subject):
    # github.com.evil.com is NOT a subdomain of github.com.
    d = subject.decide(_pre("Bash", {"command": "wget https://github.com.evil.com/p"}))
    assert _is_deny(d)


def test_bash_without_url_is_allowed(subject):
    assert subject.decide(_pre("Bash", {"command": "npm test"})) == {}


def test_blocks_edit_to_env_file(subject):
    d = subject.decide(_pre("Edit", {"file_path": "/home/dev/project/.env"}))
    assert _is_deny(d)


def test_blocks_write_into_git_dir(subject):
    d = subject.decide(_pre("Write", {"file_path": "/home/dev/project/.git/config"}))
    assert _is_deny(d)


def test_allows_ordinary_edit(subject):
    assert subject.decide(_pre("Edit", {"file_path": "src/app.py"})) == {}


def test_unrelated_tool_is_allowed(subject):
    assert subject.decide(_pre("Read", {"file_path": "/etc/hosts"})) == {}
