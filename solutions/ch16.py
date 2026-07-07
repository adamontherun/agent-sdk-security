"""Chapter 16 reference solution — scan a directory tree for credential files."""

import os
from fnmatch import fnmatch

NAME_PATTERNS = [
    ".env",
    ".env.*",
    ".git-credentials",
    ".npmrc",
    ".pypirc",
    "*-service-account.json",
    "*.pem",
    "*.key",
]

PATH_PATTERNS = [
    ".aws/credentials",
    ".config/gcloud/application_default_credentials.json",
    ".azure/*",
    ".docker/config.json",
    ".kube/config",
]


def _is_sensitive(rel_posix: str) -> bool:
    name = rel_posix.rsplit("/", 1)[-1]
    if any(fnmatch(name, pat) for pat in NAME_PATTERNS):
        return True
    return any(fnmatch(rel_posix, pat) or fnmatch(rel_posix, "*/" + pat) for pat in PATH_PATTERNS)


def scan_for_secrets(root: str) -> list[str]:
    """Return the sorted relative POSIX paths under `root` that match a known
    credential-file pattern and should not be mounted into an agent container."""
    hits: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for filename in filenames:
            abs_path = os.path.join(dirpath, filename)
            rel = os.path.relpath(abs_path, root)
            rel_posix = rel.replace(os.sep, "/")
            if _is_sensitive(rel_posix):
                hits.append(rel_posix)
    return sorted(hits)
