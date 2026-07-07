"""Run the six-step permission model against a few worked examples.

    python3 examples/ch04/pipeline_demo.py

Uses the reference model in solutions/ch04.py so the printed decisions match the
documented evaluation order exactly.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "solutions"))
import ch04 as pipeline  # noqa: E402

CASES = [
    ("hook says allow, but a deny rule matches", {"hook_decision": "allow", "deny_match": True}),
    ("deny rule under bypassPermissions", {"deny_match": True, "mode": "bypassPermissions"}),
    ("ask rule under bypassPermissions", {"ask_match": True, "mode": "bypassPermissions"}),
    ("ask rule under dontAsk", {"ask_match": True, "mode": "dontAsk"}),
    ("acceptEdits, a file edit", {"mode": "acceptEdits", "is_file_op": True}),
    (
        "plan mode, a file edit with an allow rule",
        {"mode": "plan", "is_file_op": True, "allow_match": True},
    ),
    ("nothing matches, default mode", {}),
]


def main() -> None:
    for label, overrides in CASES:
        call = {
            "hook_decision": None,
            "deny_match": False,
            "ask_match": False,
            "mode": "default",
            "allow_match": False,
            "is_file_op": False,
            "can_use_tool": lambda: "ask",
        }
        call.update(overrides)
        print(f"{pipeline.evaluate(call):5}  <-  {label}")

    print()
    for mode, allowed, tool in [
        ("bypassPermissions", [], "Bash"),
        ("default", ["Read"], "Read"),
        ("default", ["Bash(ls *)"], "Bash"),
    ]:
        reachable = pipeline.can_use_tool_reachable(mode, allowed, tool)
        print(f"canUseTool reachable for {tool}: {reachable}  (mode={mode}, allow={allowed})")


if __name__ == "__main__":
    main()
