"""Chapter 14 challenge — reason about what the proxy pattern actually prevents.

The chapter's thesis is that a credential the agent never holds is a credential
it can never leak. The proxy pattern gives you two independent mechanisms:

  1. Credential injection: the proxy adds the credential to outgoing requests,
     so the raw secret is never inside the agent's boundary at all.
  2. Egress allowlist: the proxy refuses to forward requests to hosts you did
     not permit, so an attempted exfiltration to an arbitrary server never
     leaves.

Implement `proxy_pattern_prevents` to decide whether a given exposure scenario
is stopped by these two mechanisms.
"""


def proxy_pattern_prevents(scenario: dict) -> bool:
    """Return True if the proxy pattern prevents the described exposure.

    `scenario` may contain these boolean keys (a missing key is treated as
    False):

      "credential_in_agent"    the raw credential is available inside the
                               agent's boundary (an env var, a mounted file)
      "exfil_to_blocked_host"  the leak attempt targets a host the egress
                               allowlist does not permit

    The pattern prevents the exposure when the agent never holds the credential
    (there is nothing to leak), or when the exfiltration targets a host the
    allowlist blocks (the request never leaves). It does NOT prevent the
    exposure when the agent holds the credential and can still reach an allowed
    host to send it to.
    """
    raise NotImplementedError()
