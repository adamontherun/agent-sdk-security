"""Chapter 4 challenge — model the six-step permission pipeline.

Implement both functions so the tests in test_ch04.py pass. The order you must
reproduce is the Agent SDK's documented one:

    hooks -> deny rules -> ask rules -> permission mode -> allow rules -> canUseTool

Read the chapter for the exact behaviour of each step. The three facts most
people get wrong: a hook that returns "allow" does NOT skip deny/ask; a deny
match wins even under bypassPermissions; and in dontAsk mode an ask (and the
final canUseTool step) becomes a deny instead of a prompt.

Docs: https://code.claude.com/docs/en/agent-sdk/permissions
"""

from collections.abc import Callable


def evaluate(call: dict) -> str:
    """Return "deny", "ask", or "allow" for one tool call.

    `call` keys: hook_decision (None|"allow"|"deny"), deny_match (bool),
    ask_match (bool), mode (str), allow_match (bool), is_file_op (bool),
    can_use_tool (Callable[[], str]).
    """
    raise NotImplementedError()


def can_use_tool_reachable(mode: str, allowed_tools: list[str], tool: str) -> bool:
    """Return False when the evaluation order can never reach canUseTool for
    `tool` (the CLAUDE_SDK_CAN_USE_TOOL_SHADOWED condition), True otherwise."""
    raise NotImplementedError()
