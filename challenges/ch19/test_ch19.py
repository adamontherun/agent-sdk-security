import pytest


def test_valid_request_shape(subject):
    body = subject.build_run_request(
        image_identifier="arn:aws:lambda:us-east-1:111:microvm-image/agent",
        maximum_duration_seconds=3600,
        max_idle_seconds=900,
        suspended_seconds=300,
        auto_resume=True,
    )
    assert body == {
        "imageIdentifier": "arn:aws:lambda:us-east-1:111:microvm-image/agent",
        "maximumDurationInSeconds": 3600,
        "idlePolicy": {
            "maxIdleDurationSeconds": 900,
            "suspendedDurationSeconds": 300,
            "autoResumeEnabled": True,
        },
    }


def test_eight_hour_cap_is_allowed(subject):
    body = subject.build_run_request("img", 28_800, 60, 0, False)
    assert body["maximumDurationInSeconds"] == 28_800


def test_over_eight_hours_rejected(subject):
    with pytest.raises(ValueError):
        subject.build_run_request("img", 28_801, 60, 0, False)


def test_zero_duration_rejected(subject):
    with pytest.raises(ValueError):
        subject.build_run_request("img", 0, 60, 0, False)


def test_idle_below_sixty_rejected(subject):
    with pytest.raises(ValueError):
        subject.build_run_request("img", 3600, 59, 0, True)


def test_negative_suspended_rejected(subject):
    with pytest.raises(ValueError):
        subject.build_run_request("img", 3600, 60, -1, True)
