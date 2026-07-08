"""Resolve a multi-scope settings stack into one effective policy.

    python3 examples/ch08/precedence_demo.py

Uses the reference model in solutions/ch08.py. Two scenarios, so both halves of
the precedence rule are visible: a developer can always tighten policy, but
allowManagedPermissionRulesOnly is stricter still and drops even the
developer's own rules.
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "solutions"))
import ch08 as settings  # noqa: E402

# Scenario A: normal precedence, no allowManagedPermissionRulesOnly. The
# developer tries to loosen policy (allow curl and rm, switch to bypass) and
# also adds a deny of their own. The loosening fails; the tightening survives.
WITHOUT_FLAG = {
    "managed": {
        "permissions": {
            "deny": ["Bash(curl *)"],
            "allow": ["Bash(npm run test:*)"],
        },
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

# Scenario B: the same stack, but managed settings add
# allowManagedPermissionRulesOnly. Now every non-managed rule is dropped,
# including the developer's own Read(./.env) deny. Managed is the only source.
WITH_FLAG = {
    "managed": {
        "permissions": {
            "deny": ["Bash(curl *)"],
            "allow": ["Bash(npm run test:*)"],
        },
        "allowManagedPermissionRulesOnly": True,
        "disableBypassPermissionsMode": "disable",
    },
    "user": WITHOUT_FLAG["user"],
}


def main() -> None:
    print("A. normal precedence (developer can tighten, not loosen):")
    print(json.dumps(settings.resolve(WITHOUT_FLAG), indent=2))
    print("\nB. allowManagedPermissionRulesOnly (only managed rules apply):")
    print(json.dumps(settings.resolve(WITH_FLAG), indent=2))


if __name__ == "__main__":
    main()
