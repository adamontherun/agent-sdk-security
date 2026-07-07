"""Build the OTEL environment the SDK passes through to the Claude Code CLI.

The Agent SDK does not emit telemetry itself. It forwards environment variables
to the `claude` subprocess, which has OpenTelemetry instrumentation built in and
exports directly to your collector:

    https://code.claude.com/docs/en/agent-sdk/observability

This script builds the env dict you would hand to
`ClaudeAgentOptions(env=...)`, tags it with a per-request end-user identity so
tool calls in your backend are attributable to the user the agent acted for, and
prints it. It makes no `query()` call, so it runs without a Claude session.

Run it:

    python examples/ch20/otel_env.py

Note what is NOT here: none of the OTEL_LOG_* content flags. Prompt text and
tool inputs stay out of exports by default; adding those flags is a deliberate
decision that sends the content your agent handled to your collector.
"""

from urllib.parse import quote

BASE_OTEL_ENV = {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    # Required for traces (beta). Metrics and log events export without it.
    "CLAUDE_CODE_ENHANCED_TELEMETRY_BETA": "1",
    "OTEL_TRACES_EXPORTER": "otlp",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "http/protobuf",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.internal:4318",
}


def otel_env_for_request(user_id: str, tenant_id: str, service: str) -> dict:
    """Return the base OTEL env plus resource attributes that attribute every
    span and event to one end user and tenant. Values are percent-encoded
    because OTEL_RESOURCE_ATTRIBUTES reserves commas, spaces, and equals."""
    attributes = f"enduser.id={quote(user_id)},tenant.id={quote(tenant_id)}"
    return {
        **BASE_OTEL_ENV,
        "OTEL_SERVICE_NAME": service,
        "OTEL_RESOURCE_ATTRIBUTES": attributes,
    }


def main() -> None:
    env = otel_env_for_request(
        user_id="user 4931",
        tenant_id="acme-corp",
        service="support-triage-agent",
    )
    for key, value in env.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
