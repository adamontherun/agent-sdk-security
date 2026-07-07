"""Show the Bash rule matcher's word-boundary and compound-command behaviour.

    python3 examples/ch06/bash_match_demo.py

Uses the reference model in solutions/ch06.py.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "solutions"))
import ch06 as rules  # noqa: E402

SINGLE = [
    ("ls *", "ls -la"),
    ("ls *", "lsof"),
    ("ls*", "lsof"),
    ("git * main", "git push origin main"),
    ("npm run *", "npm test"),
]

COMPOUND = [
    ("git status", "git status && rm -rf /"),
    ("git *", "git add . && git commit -m x"),
]


def main() -> None:
    print("single command  (rule -> command):")
    for pattern, command in SINGLE:
        print(f"  {str(rules.matches(pattern, command)):5}  {pattern!r:14} -> {command!r}")

    print("\ncompound command  (allow rule must match every subcommand):")
    for pattern, command in COMPOUND:
        print(f"  {str(rules.rule_allows(pattern, command)):5}  {pattern!r:12} -> {command!r}")
        print(f"         subcommands: {rules.split_commands(command)}")


if __name__ == "__main__":
    main()
