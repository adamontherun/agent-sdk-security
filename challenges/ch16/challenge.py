"""Chapter 16 challenge — a pre-flight scanner for credential files.

Before you mount a directory into an agent container, even read-only, you want
to know whether it contains any of the credential files the secure-deployment
guide warns about. Implement `scan_for_secrets` to walk a directory tree and
return every file that matches one of those patterns.

The patterns, from the guide's exclusion table:

  name matches (any directory):
    .env, .env.local (and other .env.*), .git-credentials, .npmrc, .pypirc,
    *-service-account.json, *.pem, *.key
  path matches (a specific location within the tree):
    .aws/credentials
    .config/gcloud/application_default_credentials.json
    anything under .azure/
    .docker/config.json
    .kube/config

Return relative POSIX paths (forward slashes), sorted.
"""

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


def scan_for_secrets(root: str) -> list[str]:
    """Return the sorted relative POSIX paths under `root` that match a known
    credential-file pattern.

    Walk every file under `root`. For each file, compute its path relative to
    `root` using forward slashes. Flag it if its filename matches any entry in
    NAME_PATTERNS, or if its relative path matches (or ends with) any entry in
    PATH_PATTERNS. Use fnmatch for the wildcards. Return the flagged paths
    sorted alphabetically.
    """
    raise NotImplementedError()
