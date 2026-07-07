"""Chapter 2 reference solution — a fail-closed permission matcher."""

ALWAYS_PROMPT = frozenset({"eval"})


def decide(program: str, allow_rules: set[str]) -> str:
    if program in ALWAYS_PROMPT:
        return "prompt"
    if program in allow_rules:
        return "allow"
    return "prompt"
