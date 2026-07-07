import pytest


@pytest.fixture
def tree(tmp_path):
    """A fake project/home tree mixing secret files with innocuous ones."""

    def write(rel, content="x"):
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)

    # Should be flagged.
    write(".env")
    write(".env.local")
    write("service/.git-credentials")
    write(".aws/credentials")
    write(".config/gcloud/application_default_credentials.json")
    write(".azure/accessTokens.json")
    write(".docker/config.json")
    write(".kube/config")
    write("frontend/.npmrc")
    write("backend/.pypirc")
    write("deploy/prod-service-account.json")
    write("certs/server.pem")
    write("certs/server.key")

    # Should NOT be flagged.
    write("README.md")
    write("src/main.py")
    write("config.yaml")
    write("env_helpers.py")
    write("notes/kube-config-guide.txt")
    return tmp_path


def test_flags_all_known_credential_files(subject, tree):
    result = subject.scan_for_secrets(str(tree))
    assert result == [
        ".aws/credentials",
        ".azure/accessTokens.json",
        ".config/gcloud/application_default_credentials.json",
        ".docker/config.json",
        ".env",
        ".env.local",
        ".kube/config",
        "backend/.pypirc",
        "certs/server.key",
        "certs/server.pem",
        "deploy/prod-service-account.json",
        "frontend/.npmrc",
        "service/.git-credentials",
    ]


def test_does_not_flag_innocuous_files(subject, tree):
    result = subject.scan_for_secrets(str(tree))
    for safe in ("README.md", "src/main.py", "config.yaml", "env_helpers.py"):
        assert safe not in result


def test_empty_tree_returns_empty_list(subject, tmp_path):
    assert subject.scan_for_secrets(str(tmp_path)) == []


def test_result_is_sorted(subject, tree):
    result = subject.scan_for_secrets(str(tree))
    assert result == sorted(result)
