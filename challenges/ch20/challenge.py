"""Chapter 20 challenge — triage a proxy access log.

When you suspect a prompt injection drove an agent somewhere it shouldn't have
gone, the egress proxy's access log is the ground truth of what the agent
actually reached over the network. This is the first place to look.

Implement `scan_access_log` to read Squid native `access.log` lines and flag
every request whose destination host is not on the allowlist. Squid's native
format is space-separated; the fields you need are the request method (field 5,
zero-indexed) and the request target (field 6):

    1699999999.001 42 10.0.1.9 TCP_MISS/200 512 GET http://example.com/x - ...
    1699999999.002 88 10.0.1.9 TCP_TUNNEL/200 4096 CONNECT api.anthropic.com:443 - ...

For a CONNECT tunnel the target is `host:port`; for a plain method it is a full
URL. In both cases derive the bare hostname (no port, no scheme, no path) and
compare it against the allowlist. Skip blank lines and any line with fewer than
seven fields.
"""

from collections.abc import Collection, Iterable


def host_from_target(method: str, target: str) -> str:
    """Return the bare hostname from a Squid log target.

    CONNECT targets are `host:port`. Other methods carry a full URL such as
    `http://host:port/path` or `https://host/path`. Strip the scheme, any
    port, and any path so only the hostname remains.
    """
    raise NotImplementedError()


def scan_access_log(lines: Iterable[str], allowlist: Collection[str]) -> list[dict]:
    """Return one finding dict per off-allowlist request, in file order.

    Each finding has:
      "line_no": 1-based line number in the input.
      "method":  the HTTP method (e.g. "GET", "CONNECT").
      "host":    the bare destination hostname.

    Requests whose host is on the allowlist produce no finding. Blank lines and
    lines with fewer than seven whitespace-separated fields are skipped.
    """
    raise NotImplementedError()
