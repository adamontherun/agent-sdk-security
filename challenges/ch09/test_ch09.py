BASE = {
    "cwd": "/home/agent/project",
    "tmpdir": "/tmp/claude-xyz",
    "home": "/home/agent",
    "filesystem": {"allowWrite": [], "denyWrite": [], "denyRead": [], "allowRead": []},
    "credentials": {"denyFiles": [], "denyEnv": []},
}


def _cfg(**overrides):
    cfg = {k: (v.copy() if isinstance(v, dict) else v) for k, v in BASE.items()}
    for key, val in overrides.items():
        cfg[key] = val
    return cfg


def test_write_under_cwd_allowed(subject):
    assert subject.evaluate(BASE, {"op": "write", "path": "/home/agent/project/out.txt"}) == "allow"


def test_write_to_tmpdir_allowed(subject):
    assert subject.evaluate(BASE, {"op": "write", "path": "/tmp/claude-xyz/scratch"}) == "allow"


def test_write_outside_cwd_denied(subject):
    assert subject.evaluate(BASE, {"op": "write", "path": "/etc/passwd"}) == "deny"


def test_allowwrite_grants_write(subject):
    cfg = _cfg(
        filesystem={"allowWrite": ["~/.kube"], "denyWrite": [], "denyRead": [], "allowRead": []}
    )
    assert subject.evaluate(cfg, {"op": "write", "path": "/home/agent/.kube/config"}) == "allow"


def test_denywrite_beats_cwd(subject):
    cfg = _cfg(
        filesystem={
            "allowWrite": [],
            "denyWrite": ["/home/agent/project/.git"],
            "denyRead": [],
            "allowRead": [],
        }
    )
    assert (
        subject.evaluate(cfg, {"op": "write", "path": "/home/agent/project/.git/config"}) == "deny"
    )


def test_default_read_exposes_aws_credentials(subject):
    # The documented footgun: reads are broad by default, so this is ALLOWED
    # until you add a credentials deny entry.
    assert subject.evaluate(BASE, {"op": "read", "path": "~/.aws/credentials"}) == "allow"


def test_credentials_denyfiles_blocks_read(subject):
    cfg = _cfg(credentials={"denyFiles": ["~/.aws"], "denyEnv": []})
    assert subject.evaluate(cfg, {"op": "read", "path": "~/.aws/credentials"}) == "deny"


def test_denyread_home_but_allowread_project(subject):
    cfg = _cfg(
        filesystem={
            "allowWrite": [],
            "denyWrite": [],
            "denyRead": ["~/"],
            "allowRead": ["/home/agent/project"],
        }
    )
    assert subject.evaluate(cfg, {"op": "read", "path": "/home/agent/project/main.py"}) == "allow"
    assert subject.evaluate(cfg, {"op": "read", "path": "/home/agent/.ssh/id_rsa"}) == "deny"


def test_env_deny(subject):
    cfg = _cfg(credentials={"denyFiles": [], "denyEnv": ["GITHUB_TOKEN"]})
    assert subject.evaluate(cfg, {"op": "env", "name": "GITHUB_TOKEN"}) == "deny"
    assert subject.evaluate(cfg, {"op": "env", "name": "PATH"}) == "allow"
