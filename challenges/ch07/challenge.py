"""Chapter 7 challenge — complete the URL-allowlist hook decision.

A PreToolUse hook receives the tool call as JSON on stdin. Your job is the
decision function: given the parsed input, return a decision dict that Claude
Code understands. Return {} to raise no objection (the normal permission flow
then applies), or a deny dict shaped like:

    {"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "<why>"}}

Block two things:
  1. A Bash command whose http(s) URL host is not in ALLOWED_DOMAINS. A host
     counts as allowed when it equals an allowed domain or is a subdomain of one.
  2. An Edit/Write/MultiEdit whose file_path contains any PROTECTED_FILE_PATTERNS
     substring.

Everything else returns {}.

Docs: https://code.claude.com/docs/en/hooks-guide
"""

import re  # noqa: F401  (you will want a regex to pull URLs out of the command)

ALLOWED_DOMAINS = frozenset({"github.com", "api.github.com", "pypi.org", "files.pythonhosted.org"})

PROTECTED_FILE_PATTERNS = (".env", ".git/", ".ssh/", ".aws/credentials")


def decide(input_data: dict) -> dict:
    """Return a PreToolUse deny dict, or {} to raise no objection."""
    raise NotImplementedError()
