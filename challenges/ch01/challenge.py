"""Chapter 1 challenge — model the lethal trifecta.

Simon Willison's "lethal trifecta" is the combination of three capabilities
that, together, let an attacker turn prompt injection into data theft:

  1. access to private data
  2. exposure to untrusted content
  3. the ability to communicate externally

Any one or two of these on their own is survivable. All three at once is the
dangerous configuration, and removing any single leg breaks it.

Implement `assess_trifecta` so that it reports which legs a deployment has,
whether the combination is lethal, and — when it is — which legs could be cut
to break the trifecta.
"""

LEG_NAMES = ("private_data", "untrusted_content", "external_comms")


def assess_trifecta(
    private_data: bool,
    untrusted_content: bool,
    external_comms: bool,
) -> dict:
    """Return a report on a deployment's trifecta exposure.

    The returned dict has three keys:

      "present":  a list of the leg names that are True, in LEG_NAMES order.
      "lethal":   True only when all three legs are present.
      "breakable_by_cutting": when lethal, the list of legs that could be
                  removed to break the trifecta (cutting any one is enough,
                  so this is every present leg); an empty list otherwise.
    """
    raise NotImplementedError()
