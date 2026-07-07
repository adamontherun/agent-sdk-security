"""Tests for Chapter 6 — Bash rule matching semantics."""

import pytest


@pytest.mark.parametrize(
    "pattern,command,expected",
    [
        # Word boundary: space before * requires space-or-end after the prefix.
        ("ls *", "ls -la", True),
        ("ls *", "ls", True),
        ("ls *", "lsof", False),
        ("ls*", "lsof", True),
        ("ls*", "ls -la", True),
        # Wildcards span multiple arguments.
        ("git *", "git log --oneline --all", True),
        ("git * main", "git checkout main", True),
        ("git * main", "git push origin main", True),
        ("git * main", "git checkout dev", False),
        # Middle and leading wildcards.
        ("* --version", "python --version", True),
        ("* install", "npm install", True),
        ("npm run *", "npm run build", True),
        ("npm run *", "npm test", False),
        # :* suffix is equivalent to a trailing " *".
        ("ls:*", "ls -la", True),
        ("ls:*", "lsof", False),
        # Exact match.
        ("npm run build", "npm run build", True),
        ("npm run build", "npm run build --prod", False),
    ],
)
def test_matches(subject, pattern, command, expected):
    assert subject.matches(pattern, command) is expected


def test_split_on_and(subject):
    assert subject.split_commands("git status && npm test") == ["git status", "npm test"]


def test_split_on_pipe_and_semicolon(subject):
    assert subject.split_commands("cat f | grep x ; echo done") == [
        "cat f",
        "grep x",
        "echo done",
    ]


def test_split_on_pipe_amp(subject):
    assert subject.split_commands("make |& tee log") == ["make", "tee log"]


def test_rule_allows_single(subject):
    assert subject.rule_allows("npm run *", "npm run build")


def test_rule_rejects_compound_escape(subject):
    # The classic bypass: a safe prefix chained to something the rule never saw.
    assert not subject.rule_allows("git status", "git status && rm -rf /")


def test_rule_allows_when_every_part_matches(subject):
    assert subject.rule_allows("git *", "git add . && git commit -m x")
