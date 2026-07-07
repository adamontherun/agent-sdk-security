"""Chapter 6 challenge — implement the Bash rule matcher.

Reproduce three pieces of the documented Bash matching behaviour:

  split_commands(command)  -> break a compound command on &&, ||, ;, |, |&, &,
                              and newlines into its subcommands.
  matches(pattern, cmd)    -> match one command against a specifier, honoring the
                              space-before-* word boundary and the :* suffix.
  rule_allows(pattern, cmd)-> an allow rule permits a compound command only if it
                              matches every subcommand.

The word boundary is the subtle part: "ls *" matches "ls -la" and "ls" but not
"lsof", while "ls*" matches all three. Read the chapter, then make the tests pass.

Docs: https://code.claude.com/docs/en/permissions
"""


def split_commands(command: str) -> list[str]:
    """Split a compound command into its subcommands (stripped, no empties)."""
    raise NotImplementedError()


def matches(pattern: str, command: str) -> bool:
    """True if `pattern` matches a single command string."""
    raise NotImplementedError()


def rule_allows(pattern: str, command: str) -> bool:
    """True only if `pattern` matches every subcommand of `command`."""
    raise NotImplementedError()
