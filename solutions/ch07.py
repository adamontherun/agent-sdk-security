"""Reference solution for Chapter 7 — the URL-allowlist hook decision.

Mirrors the standalone hook in examples/ch07/url_guard.py, minus the stdin/stdout
plumbing, so the same logic can be unit-tested directly.

Docs: https://code.claude.com/docs/en/hooks-guide
"""

import re

ALLOWED_DOMAINS = frozenset({"github.com", "api.github.com", "pypi.org", "files.pythonhosted.org"})

PROTECTED_FILE_PATTERNS = (".env", ".git/", ".ssh/", ".aws/credentials")

_URL_RE = re.compile(r"https?://([^/\s:'\"]+)", re.IGNORECASE)


def _host_allowed(host: str) -> bool:
    host = host.lower().rstrip(".")
    return any(host == domain or host.endswith("." + domain) for domain in ALLOWED_DOMAINS)


def _deny(reason: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def decide(input_data: dict) -> dict:
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {}) or {}

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        for host in _URL_RE.findall(command):
            if not _host_allowed(host):
                return _deny(
                    f"URL host '{host}' is not on the allowlist. "
                    f"Allowed: {', '.join(sorted(ALLOWED_DOMAINS))}."
                )
        return {}

    if tool_name in {"Edit", "Write", "MultiEdit"}:
        file_path = tool_input.get("file_path", "")
        for pattern in PROTECTED_FILE_PATTERNS:
            if pattern in file_path:
                return _deny(f"'{file_path}' matches protected pattern '{pattern}'.")
        return {}

    return {}
