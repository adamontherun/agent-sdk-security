"""Show which calls acceptEdits mode auto-approves.

    python3 examples/ch05/acceptedits_demo.py

Uses the reference model in solutions/ch05.py.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "solutions"))
import ch05 as ae  # noqa: E402

CWD = "/home/dev/project"
EXTRA = ["/home/dev/shared"]

CASES = [
    ("Edit", {"file_path": "src/app.py"}),
    ("Edit", {"file_path": "/etc/hosts"}),
    ("Write", {"file_path": "/home/dev/shared/notes.md"}),
    ("Bash", {"command": "mkdir build"}),
    ("Bash", {"command": "rm src/old.py"}),
    ("Bash", {"command": "rm /etc/passwd"}),
    ("Bash", {"command": "rm -rf /"}),
    ("Bash", {"command": "curl https://example.com"}),
]


def main() -> None:
    print(f"acceptEdits filesystem commands: {sorted(ae.ACCEPT_EDITS_FS_COMMANDS)}\n")
    for tool, tool_input in CASES:
        verdict = (
            "auto-approve" if ae.accept_edits_approves(tool, tool_input, CWD, EXTRA) else "PROMPT"
        )
        detail = tool_input.get("command") or tool_input.get("file_path")
        print(f"{verdict:12}  {tool:5}  {detail}")


if __name__ == "__main__":
    main()
