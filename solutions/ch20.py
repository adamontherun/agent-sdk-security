"""Chapter 20 reference solution — triage a proxy access log."""

from collections.abc import Collection, Iterable


def host_from_target(method: str, target: str) -> str:
    host = target
    if "://" in host:
        host = host.split("://", 1)[1]
    # Drop any path or query.
    host = host.split("/", 1)[0]
    # Drop the port.
    host = host.rsplit(":", 1)[0] if ":" in host else host
    return host


def scan_access_log(lines: Iterable[str], allowlist: Collection[str]) -> list[dict]:
    allowed = set(allowlist)
    findings: list[dict] = []
    for line_no, raw in enumerate(lines, start=1):
        fields = raw.split()
        if len(fields) < 7:
            continue
        method, target = fields[5], fields[6]
        host = host_from_target(method, target)
        if host not in allowed:
            findings.append({"line_no": line_no, "method": method, "host": host})
    return findings
