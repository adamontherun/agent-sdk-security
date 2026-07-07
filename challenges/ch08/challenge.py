"""Chapter 8 challenge — resolve settings precedence and managed lockdown.

Implement resolve(scopes) to merge per-scope settings into one effective policy.
The rules you must encode:

  * Precedence, highest to lowest: managed, cli, local, shared, user
    (SCOPE_ORDER below).
  * deny rules merge from EVERY scope and always win. A rule in deny is removed
    from the effective allow and ask lists.
  * When managed sets allowManagedPermissionRulesOnly = True, only managed
    allow/ask rules count. deny still merges from all scopes.
  * defaultMode: the highest-priority scope that sets one wins; otherwise
    "default".
  * If any scope sets disableBypassPermissionsMode = "disable", bypass is not
    allowed, and a defaultMode of "bypassPermissions" falls back to "default".

Return {"allow", "ask", "deny", "defaultMode", "bypassAllowed"}.

Docs: https://code.claude.com/docs/en/permissions
"""

SCOPE_ORDER = ["managed", "cli", "local", "shared", "user"]


def resolve(scopes: dict) -> dict:
    """Resolve per-scope settings into the effective policy."""
    raise NotImplementedError()
