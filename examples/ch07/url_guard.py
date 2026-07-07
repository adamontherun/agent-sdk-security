#!/usr/bin/env python3
"""A PreToolUse hook that enforces a URL allowlist on Bash commands.

Permission rules can't reliably constrain a URL inside a Bash command (see
Chapter 6). A hook can: it sees the full command string and can parse every URL
out of it before the command runs. This script also blocks edits to a small set
of protected files.

Claude Code invokes a hook by running it with the tool-call JSON on stdin. This
script reads that JSON, decides, and communicates back the way the docs specify:
it prints a structured JSON decision to stdout and exits 0. An empty decision
(no output) means "no objection, run the normal permission flow".

Wire it up in .claude/settings.json:

    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash|Edit|Write",
            "hooks": [
              {"type": "command",
               "command": "python3 examples/ch07/url_guard.py"}
            ]
          }
        ]
      }
    }

Docs: https://code.claude.com/docs/en/hooks-guide
"""

import json
import re
import sys

# Hosts a network command is allowed to reach. Everything else is blocked.
ALLOWED_DOMAINS = frozenset(
    {
        "github.com",
        "api.github.com",
        "pypi.org",
        "files.pythonhosted.org",
    }
)

# File paths a hook should never let the agent edit, matched as substrings.
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
    """Return a PreToolUse decision dict, or {} to raise no objection."""
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


def main() -> int:
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # Malformed input: fail closed for a security hook.
        print(json.dumps(_deny("Hook received malformed JSON on stdin.")))
        return 0

    decision = decide(input_data)
    if decision:
        print(json.dumps(decision))
    return 0


if __name__ == "__main__":
    sys.exit(main())
