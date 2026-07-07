"""Reference solution for Chapter 6 — Bash rule matching semantics.

A teaching model of how a Bash permission specifier matches a command:
word-boundary wildcards, the :* suffix, and compound-command splitting. It is a
model of the documented behaviour, not Claude Code's real matcher (which also
strips process wrappers and canonicalizes far more than this).

Source: https://code.claude.com/docs/en/permissions  (Bash rule section)
"""

import re

# The command separators Claude Code recognizes. Multi-character operators come
# first so the alternation prefers them over their single-character prefixes.
_SEPARATORS = re.compile(r"&&|\|\||;|\|&|\||&|\n")


def split_commands(command: str) -> list[str]:
    """Split a compound command into its subcommands on shell operators."""
    parts = _SEPARATORS.split(command)
    return [p.strip() for p in parts if p.strip()]


def _compile(pattern: str) -> re.Pattern:
    # The :* suffix is equivalent to a trailing " *".
    if pattern.endswith(":*"):
        pattern = pattern[:-2] + " *"

    word_boundary = pattern.endswith(" *")
    core = pattern[:-2] if word_boundary else pattern

    # Escape everything, then turn each literal "*" back into ".*".
    regex = ".*".join(re.escape(seg) for seg in core.split("*"))

    # A word boundary means the prefix must be followed by a space or the end
    # of the string; otherwise the match is anchored exactly.
    regex = "^" + regex + (r"(?: .*)?$" if word_boundary else "$")
    return re.compile(regex)


def matches(pattern: str, command: str) -> bool:
    """True if `pattern` matches a single command string.

    "ls *" matches "ls -la" and "ls" but not "lsof" (word boundary).
    "ls*" matches "ls -la" and "lsof" (no boundary).
    """
    return _compile(pattern).match(command.strip()) is not None


def rule_allows(pattern: str, command: str) -> bool:
    """True only if `pattern` matches every subcommand of a compound command.

    A rule that matches `safe-cmd` does not authorize `safe-cmd && evil-cmd`.
    """
    subcommands = split_commands(command)
    if not subcommands:
        return False
    return all(matches(pattern, sub) for sub in subcommands)
