"""Chapter 19 challenge — build a valid run-microvm request.

`aws lambda-microvms run-microvm` accepts a JSON body (via --cli-input-json)
that this chapter builds. The CLI enforces hard limits, and getting them wrong
means the launch is rejected at the API rather than at your desk:

  * maximumDurationInSeconds is 1..28800 (28,800 seconds is the 8-hour cap).
  * idlePolicy.maxIdleDurationSeconds must be at least 60.
  * idlePolicy.suspendedDurationSeconds must be at least 0.

These come straight from `aws lambda-microvms run-microvm help` on aws-cli
2.35.15. Implement `build_run_request` to validate its inputs against those
limits and return the request body as a dict, so a bad value is caught before
it reaches AWS.
"""

MAX_DURATION_SECONDS = 28_800  # 8 hours, the platform cap.
MIN_IDLE_SECONDS = 60


def build_run_request(
    image_identifier: str,
    maximum_duration_seconds: int,
    max_idle_seconds: int,
    suspended_seconds: int,
    auto_resume: bool,
) -> dict:
    """Return the run-microvm request body:

        {
            "imageIdentifier": <image_identifier>,
            "maximumDurationInSeconds": <maximum_duration_seconds>,
            "idlePolicy": {
                "maxIdleDurationSeconds": <max_idle_seconds>,
                "suspendedDurationSeconds": <suspended_seconds>,
                "autoResumeEnabled": <auto_resume>,
            },
        }

    Raise ValueError if maximum_duration_seconds is outside 1..28800, if
    max_idle_seconds is below 60, or if suspended_seconds is negative.
    """
    raise NotImplementedError()
