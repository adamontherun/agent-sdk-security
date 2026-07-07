"""Resolve a multi-scope settings stack into one effective policy.

    python3 examples/ch08/precedence_demo.py

Uses the reference model in solutions/ch08.py. The scenario: managed settings
lock the fleet down, and a developer's user settings try to loosen it.
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "solutions"))
import ch08 as settings  # noqa: E402

SCOPES = {
    "managed": {
        "permissions": {
            "deny": ["Bash(curl *)"],
            "allow": ["Bash(npm run test:*)"],
        },
        "allowManagedPermissionRulesOnly": True,
        "disableBypassPermissionsMode": "disable",
    },
    "user": {
        "permissions": {
            "allow": ["Bash(curl *)", "Bash(rm *)"],
            "deny": ["Read(./.env)"],
        },
        "defaultMode": "bypassPermissions",
    },
}


def main() -> None:
    effective = settings.resolve(SCOPES)
    print("effective policy:")
    print(json.dumps(effective, indent=2))


if __name__ == "__main__":
    main()
