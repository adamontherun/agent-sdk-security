"""First-pass incident triage: what did the agent actually reach?

When you suspect a prompt injection pushed an agent somewhere it shouldn't have
gone, the egress proxy's access log is the ground truth. The permission
pipeline records what the agent *tried*; the proxy records what left the box.
This script reads a Squid native access.log and prints every request whose
destination host is not on the allowlist.

Run it:

    python examples/ch20/triage_access_log.py

It reads examples/ch20/proxy_access.log against a small allowlist and needs no
network access. The two flagged lines in the sample are a paste site and the
EC2 instance-metadata endpoint (169.254.169.254), which is exactly the shape of
a credential-exfiltration attempt worth waking someone up for.
"""

import pathlib
from collections.abc import Collection, Iterable

LOG = pathlib.Path(__file__).parent / "proxy_access.log"
ALLOWLIST = {"api.anthropic.com", "registry.npmjs.org", "github.com"}


def host_from_target(method: str, target: str) -> str:
    host = target
    if "://" in host:
        host = host.split("://", 1)[1]
    host = host.split("/", 1)[0]
    return host.rsplit(":", 1)[0] if ":" in host else host


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


def main() -> None:
    findings = scan_access_log(LOG.read_text().splitlines(), ALLOWLIST)
    if not findings:
        print("No off-allowlist requests. Nothing to triage.")
        return
    print(f"{len(findings)} off-allowlist request(s):")
    for f in findings:
        print(f"  line {f['line_no']:>3}  {f['method']:<7}  {f['host']}")


if __name__ == "__main__":
    main()
