"""Chapter 19 reference solution — build a valid run-microvm request."""

MAX_DURATION_SECONDS = 28_800  # 8 hours, the platform cap.
MIN_IDLE_SECONDS = 60


def build_run_request(
    image_identifier: str,
    maximum_duration_seconds: int,
    max_idle_seconds: int,
    suspended_seconds: int,
    auto_resume: bool,
) -> dict:
    if not 1 <= maximum_duration_seconds <= MAX_DURATION_SECONDS:
        raise ValueError(
            f"maximum_duration_seconds must be 1..{MAX_DURATION_SECONDS}, "
            f"got {maximum_duration_seconds}"
        )
    if max_idle_seconds < MIN_IDLE_SECONDS:
        raise ValueError(f"max_idle_seconds must be at least {MIN_IDLE_SECONDS}")
    if suspended_seconds < 0:
        raise ValueError("suspended_seconds must not be negative")

    return {
        "imageIdentifier": image_identifier,
        "maximumDurationInSeconds": maximum_duration_seconds,
        "idlePolicy": {
            "maxIdleDurationSeconds": max_idle_seconds,
            "suspendedDurationSeconds": suspended_seconds,
            "autoResumeEnabled": auto_resume,
        },
    }
