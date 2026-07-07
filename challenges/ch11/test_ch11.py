GOOD_DAEMON = {"runtimes": {"runsc": {"path": "/usr/local/bin/runsc"}}}


def test_correct_setup_is_clean(subject):
    assert subject.validate_runsc_setup(GOOD_DAEMON, ["--runtime=runsc", "agent-image"]) == []


def test_two_token_runtime_form(subject):
    assert subject.validate_runsc_setup(GOOD_DAEMON, ["--runtime", "runsc", "agent-image"]) == []


def test_missing_registration(subject):
    assert subject.validate_runsc_setup({"runtimes": {}}, ["--runtime=runsc", "img"]) == [
        "runtime-not-registered"
    ]


def test_registered_but_not_selected(subject):
    assert subject.validate_runsc_setup(GOOD_DAEMON, ["agent-image"]) == ["runtime-not-selected"]


def test_both_wrong(subject):
    assert subject.validate_runsc_setup({}, ["agent-image"]) == sorted(
        ["runtime-not-registered", "runtime-not-selected"]
    )


def test_default_runtime_is_not_runsc(subject):
    assert "runtime-not-selected" in subject.validate_runsc_setup(
        GOOD_DAEMON, ["--runtime", "runc", "img"]
    )
