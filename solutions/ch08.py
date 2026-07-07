"""Reference solution for Chapter 8 — settings precedence and managed lockdown.

A teaching model of how Claude Code resolves permission rules across settings
scopes. Precedence, highest to lowest: managed, cli, local, shared, user. Deny
rules from any scope always win; a managed-only flag can drop everyone else's
allow/ask rules; and disableBypassPermissionsMode removes bypass from the
effective mode.

Sources:
  https://code.claude.com/docs/en/permissions  (settings precedence, managed-only)
"""

# Highest priority first.
SCOPE_ORDER = ["managed", "cli", "local", "shared", "user"]


def _rules(scope: dict, kind: str) -> list[str]:
    return list(scope.get("permissions", {}).get(kind, []))


def resolve(scopes: dict) -> dict:
    """Resolve per-scope settings into the effective policy.

    `scopes` maps a scope name from SCOPE_ORDER to a settings dict, e.g.
        {"managed": {"permissions": {"deny": ["Bash(curl *)"]},
                     "allowManagedPermissionRulesOnly": True},
         "user":    {"permissions": {"allow": ["Bash"]},
                     "defaultMode": "acceptEdits"}}

    Returns {"allow", "ask", "deny", "defaultMode", "bypassAllowed"}.
    """
    managed = scopes.get("managed", {})
    managed_only = managed.get("allowManagedPermissionRulesOnly", False)

    # Which scopes may contribute allow/ask rules.
    rule_scopes = ["managed"] if managed_only else [s for s in SCOPE_ORDER if s in scopes]

    allow: list[str] = []
    ask: list[str] = []
    for name in rule_scopes:
        for r in _rules(scopes[name], "allow"):
            if r not in allow:
                allow.append(r)
        for r in _rules(scopes[name], "ask"):
            if r not in ask:
                ask.append(r)

    # Deny always merges from every scope, even under allowManagedPermissionRulesOnly.
    deny: list[str] = []
    for name in SCOPE_ORDER:
        if name in scopes:
            for r in _rules(scopes[name], "deny"):
                if r not in deny:
                    deny.append(r)

    # A denied rule can't also be allowed or asked: deny wins.
    deny_set = set(deny)
    allow = [r for r in allow if r not in deny_set]
    ask = [r for r in ask if r not in deny_set]

    # defaultMode: the highest-priority scope that sets one wins.
    default_mode = "default"
    for name in SCOPE_ORDER:
        if name in scopes and "defaultMode" in scopes[name]:
            default_mode = scopes[name]["defaultMode"]
            break

    # disableBypassPermissionsMode works from any scope.
    bypass_disabled = any(
        scopes.get(name, {}).get("disableBypassPermissionsMode") == "disable"
        for name in SCOPE_ORDER
    )
    if bypass_disabled and default_mode == "bypassPermissions":
        default_mode = "default"

    return {
        "allow": allow,
        "ask": ask,
        "deny": deny,
        "defaultMode": default_mode,
        "bypassAllowed": not bypass_disabled,
    }
