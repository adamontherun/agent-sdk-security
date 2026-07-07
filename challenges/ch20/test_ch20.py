import pathlib

SAMPLE = pathlib.Path(__file__).parent / "access_sample.log"
ALLOWLIST = {"api.anthropic.com", "registry.npmjs.org", "github.com"}


def test_host_from_connect_target(subject):
    assert subject.host_from_target("CONNECT", "api.anthropic.com:443") == "api.anthropic.com"


def test_host_from_full_url(subject):
    assert subject.host_from_target("GET", "http://registry.npmjs.org/left-pad") == (
        "registry.npmjs.org"
    )


def test_host_from_url_with_port(subject):
    assert subject.host_from_target("GET", "http://api.anthropic.com:443/v1/models") == (
        "api.anthropic.com"
    )


def test_scan_flags_only_offlist_hosts(subject):
    lines = SAMPLE.read_text().splitlines()
    findings = subject.scan_access_log(lines, ALLOWLIST)
    assert findings == [
        {"line_no": 4, "method": "CONNECT", "host": "evil.example.net"},
        {"line_no": 5, "method": "CONNECT", "host": "paste.example.io"},
        {"line_no": 8, "method": "GET", "host": "169.254.169.254"},
    ]


def test_blank_and_short_lines_skipped(subject):
    lines = ["", "   ", "not enough fields here", "1 2 3 4 5 6"]
    assert subject.scan_access_log(lines, ALLOWLIST) == []


def test_everything_allowed_returns_empty(subject):
    lines = SAMPLE.read_text().splitlines()
    wide = ALLOWLIST | {"evil.example.net", "paste.example.io", "169.254.169.254"}
    assert subject.scan_access_log(lines, wide) == []
