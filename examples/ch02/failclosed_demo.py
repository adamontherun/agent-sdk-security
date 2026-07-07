"""Show fail-closed matching classifying a batch of commands.

Run it:

    python examples/ch02/failclosed_demo.py

This mirrors the shape of Claude Code's permission decision: a program either
matches an allow rule (and runs), is an always-prompt construct (and stops), or
fails closed to a prompt because nothing matched. No Claude session is needed.
"""

ALWAYS_PROMPT = frozenset({"eval"})

# What an operator allowlisted for this project.
ALLOW_RULES = {"ls", "cat", "git", "npm"}


def decide(program: str, allow_rules: set[str]) -> str:
    if program in ALWAYS_PROMPT:
        return "prompt"
    if program in allow_rules:
        return "allow"
    return "prompt"


COMMANDS = ["ls", "npm", "git", "curl", "wget", "sudo", "eval"]


def main() -> None:
    for program in COMMANDS:
        decision = decide(program, ALLOW_RULES)
        reason = ""
        if program in ALWAYS_PROMPT:
            reason = "always-prompt construct"
        elif decision == "prompt":
            reason = "no matching allow rule (fail-closed)"
        print(f"{program:>6}  ->  {decision:<6} {reason}")


if __name__ == "__main__":
    main()
