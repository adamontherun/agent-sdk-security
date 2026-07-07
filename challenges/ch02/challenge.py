"""Chapter 2 challenge — a fail-closed permission matcher.

Claude Code decides whether a Bash command runs automatically or has to stop
for approval. Two behaviors from that decision matter here:

  * Fail-closed matching: a command that does not match an allow rule defaults
    to requiring manual approval, rather than being allowed by default.
  * Always-prompt constructs: a small set of constructs such as `eval` always
    require approval regardless of allow rules.

Implement `decide` to model that logic on a simplified input: the program name
(the first token of a command, e.g. "npm") and the set of allowed program
names an operator has configured.
"""

# Constructs that always require approval, even when an allow rule would
# otherwise match them.
ALWAYS_PROMPT = frozenset({"eval"})


def decide(program: str, allow_rules: set[str]) -> str:
    """Return "allow" or "prompt" for a program name.

    Rules, in order:
      1. If `program` is an always-prompt construct, return "prompt" even if
         it also appears in `allow_rules`.
      2. Otherwise, if `program` is in `allow_rules`, return "allow".
      3. Otherwise fail closed: return "prompt".
    """
    raise NotImplementedError()
