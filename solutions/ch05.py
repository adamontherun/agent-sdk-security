"""Reference solution for Chapter 5 — what acceptEdits actually auto-approves.

A teaching model of acceptEdits mode: file edits plus a fixed list of
filesystem Bash commands, scoped to the working directory and additional
directories. Not Claude Code's real matcher.

Sources:
  https://code.claude.com/docs/en/agent-sdk/permissions  (acceptEdits list)
  https://code.claude.com/docs/en/permissions             (bypass circuit breaker)
"""

import os

# The exact filesystem commands acceptEdits auto-approves alongside Edit/Write.
ACCEPT_EDITS_FS_COMMANDS = {"mkdir", "touch", "rm", "rmdir", "mv", "cp", "sed"}

_FILE_EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def _normalize(path: str, cwd: str) -> str:
    expanded = os.path.expanduser(path)
    if not os.path.isabs(expanded):
        expanded = os.path.join(cwd, expanded)
    return os.path.normpath(expanded)


def in_scope(path: str, cwd: str, additional_dirs: list[str]) -> bool:
    """True when `path` resolves inside cwd or one of additional_dirs."""
    target = _normalize(path, cwd)
    roots = [os.path.normpath(os.path.expanduser(cwd))]
    roots += [os.path.normpath(os.path.expanduser(d)) for d in additional_dirs]
    return any(target == root or target.startswith(root + os.sep) for root in roots)


def is_circuit_breaker(command: str) -> bool:
    """True for removals that always prompt even in bypassPermissions:
    rm -rf / and rm -rf ~ (and $HOME)."""
    tokens = command.split()
    if not tokens or tokens[0] not in {"rm", "rmdir"}:
        return False
    targets = [t for t in tokens[1:] if not t.startswith("-")]
    home = os.path.expanduser("~")
    for t in targets:
        resolved = os.path.normpath(os.path.expanduser(t.replace("$HOME", home)))
        if resolved in {"/", home}:
            return True
    return False


def accept_edits_approves(
    tool_name: str, tool_input: dict, cwd: str, additional_dirs: list[str] | None = None
) -> bool:
    """Return True if acceptEdits mode auto-approves this call without a prompt."""
    additional_dirs = additional_dirs or []

    if tool_name in _FILE_EDIT_TOOLS:
        path = tool_input.get("file_path", "")
        return in_scope(path, cwd, additional_dirs)

    if tool_name == "Bash":
        command = tool_input.get("command", "").strip()
        if is_circuit_breaker(command):
            return False
        tokens = command.split()
        if not tokens or tokens[0] not in ACCEPT_EDITS_FS_COMMANDS:
            return False
        # Every path argument must stay inside the approved scope.
        path_args = [t for t in tokens[1:] if not t.startswith("-")]
        return all(in_scope(p, cwd, additional_dirs) for p in path_args)

    return False
