def test_allowlisted_program_is_allowed(subject):
    assert subject.decide("npm", {"npm", "ls"}) == "allow"


def test_unmatched_program_fails_closed(subject):
    assert subject.decide("curl", {"npm", "ls"}) == "prompt"


def test_empty_allowlist_fails_closed(subject):
    assert subject.decide("ls", set()) == "prompt"


def test_eval_always_prompts_even_when_allowlisted(subject):
    # The always-prompt construct overrides the allow rule.
    assert subject.decide("eval", {"eval", "npm"}) == "prompt"
