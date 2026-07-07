"""Chapter 5 challenge — model acceptEdits auto-approval.

acceptEdits mode auto-approves file edits and a fixed set of filesystem Bash
commands, but only for paths inside the working directory or additionalDirectories,
and never for the rm -rf / and rm -rf ~ circuit breaker. Implement the functions
below so the tests pass.

Docs: https://code.claude.com/docs/en/agent-sdk/permissions
"""

import os  # noqa: F401  (you will likely want os.path helpers)

# Fill this in from the chapter: the exact commands acceptEdits auto-approves.
ACCEPT_EDITS_FS_COMMANDS: set[str] = set()


def in_scope(path: str, cwd: str, additional_dirs: list[str]) -> bool:
    """True when `path` resolves inside cwd or one of additional_dirs."""
    raise NotImplementedError()


def is_circuit_breaker(command: str) -> bool:
    """True for rm/rmdir targeting / or the home directory."""
    raise NotImplementedError()


def accept_edits_approves(
    tool_name: str, tool_input: dict, cwd: str, additional_dirs: list[str] | None = None
) -> bool:
    """Return True if acceptEdits auto-approves this call without a prompt."""
    raise NotImplementedError()
