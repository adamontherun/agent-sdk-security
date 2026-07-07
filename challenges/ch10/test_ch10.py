HARDENED = [
    "--cap-drop",
    "ALL",
    "--security-opt",
    "no-new-privileges",
    "--read-only",
    "--tmpfs",
    "/tmp:rw,noexec,nosuid,size=64m",
    "--network",
    "none",
    "--memory",
    "512m",
    "--cpus",
    "1",
    "--pids-limit",
    "128",
    "--user",
    "1000:1000",
    "agent-image",
]


def test_fully_hardened_has_no_gaps(subject):
    assert subject.missing_hardening(HARDENED) == []


def test_bare_run_flags_everything(subject):
    result = subject.missing_hardening(["agent-image"])
    assert result == sorted(
        [
            "cap-drop-all",
            "no-new-privileges",
            "read-only",
            "network-isolated",
            "non-root",
            "pids-limit",
            "memory-limit",
        ]
    )


def test_root_user_is_flagged(subject):
    args = [a for a in HARDENED]
    args[args.index("1000:1000")] = "0:0"
    assert "non-root" in subject.missing_hardening(args)


def test_equals_syntax_accepted(subject):
    args = [
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges:true",
        "--read-only",
        "--network=none",
        "--memory=1g",
        "--pids-limit=64",
        "--user=1000:1000",
        "img",
    ]
    assert subject.missing_hardening(args) == []


def test_network_bridge_is_not_isolated(subject):
    args = [a for a in HARDENED]
    args[args.index("none")] = "bridge"
    assert "network-isolated" in subject.missing_hardening(args)
