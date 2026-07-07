"""Reference solution for Chapter 4 — the permission evaluation pipeline.

A teaching model of the Agent SDK's six-step evaluation order:
hooks -> deny rules -> ask rules -> permission mode -> allow rules -> canUseTool.
This is a model of the documented behaviour for building intuition, not Claude
Code's actual matcher.

Source: https://code.claude.com/docs/en/agent-sdk/permissions
"""

from collections.abc import Callable

# Modes that auto-approve file operations at the permission-mode step.
_FILE_OP_AUTO_MODES = {"acceptEdits"}


def evaluate(call: dict) -> str:
    """Return the final decision for one tool call: "deny", "ask", or "allow".

    `call` describes the state each step sees:
      hook_decision: None | "allow" | "deny"  (what a PreToolUse hook returned)
      deny_match:    bool                      (a scoped deny rule matches)
      ask_match:     bool                      (an ask rule matches)
      mode:          str                       (default/acceptEdits/plan/
                                                bypassPermissions/dontAsk/auto)
      allow_match:   bool                      (an allow rule matches)
      is_file_op:    bool                      (Edit/Write or a filesystem Bash op)
      can_use_tool:  Callable[[], str]         (the runtime callback)
    """
    hook_decision = call.get("hook_decision")
    mode = call.get("mode", "default")
    can_use_tool: Callable[[], str] | None = call.get("can_use_tool")

    # Step 1 — hooks run first. A hook can deny outright. A hook that returns
    # "allow" does NOT skip the deny and ask rules below.
    if hook_decision == "deny":
        return "deny"

    # Step 2 — deny rules. A matching deny blocks the call in every mode,
    # including bypassPermissions, and even when the hook returned "allow".
    if call.get("deny_match"):
        return "deny"

    # Step 3 — ask rules. A match forces confirmation even in bypassPermissions.
    # In dontAsk mode there is no one to prompt, so an ask becomes a deny.
    if call.get("ask_match"):
        return "deny" if mode == "dontAsk" else "ask"

    # Step 4 — permission mode.
    if mode == "bypassPermissions":
        return "allow"
    if mode in _FILE_OP_AUTO_MODES and call.get("is_file_op"):
        return "allow"
    if mode == "plan" and call.get("is_file_op"):
        # Plan mode never auto-approves writes, even when an allow rule matches.
        return _run_callback(can_use_tool, mode)

    # Step 5 — allow rules.
    if call.get("allow_match"):
        return "allow"

    # Step 6 — canUseTool. In dontAsk mode this step is skipped and the call
    # is denied instead of prompting.
    return _run_callback(can_use_tool, mode)


def _run_callback(can_use_tool: Callable[[], str] | None, mode: str) -> str:
    if mode == "dontAsk":
        return "deny"
    if can_use_tool is None:
        # No callback provided: default behaviour is a prompt (ask).
        return "ask"
    return can_use_tool()


def can_use_tool_reachable(mode: str, allowed_tools: list[str], tool: str) -> bool:
    """Model the CLAUDE_SDK_CAN_USE_TOOL_SHADOWED check.

    Return False when the six-step order can never reach canUseTool for `tool`,
    so a check placed there would be silently bypassed. Two configurations
    shadow the callback: bypassPermissions mode, and a bare allowed_tools entry
    (no specifier) naming the tool. A scoped entry like "Bash(ls *)" does not
    shadow, because non-matching calls still fall through.
    """
    if mode == "bypassPermissions":
        return False
    # A bare entry (no specifier) naming this tool auto-approves it before the
    # callback is consulted; a scoped entry like "Bash(ls *)" does not.
    return not any("(" not in entry and entry == tool for entry in allowed_tools)
