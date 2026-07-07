#!/usr/bin/env python3
"""Pre-flight credential scan for a directory you are about to mount.

Run it against any tree before wiring it into a container mount:

    python3 examples/ch16/preflight_scan.py /path/to/code

It walks the tree, flags every file matching the secure-deployment guide's
credential-exclusion table, and exits non-zero if it finds anything, so it can
gate a mount in a build script or CI step. It reads nothing but filenames and
paths; it never opens the files, so it is safe to point at a tree full of
secrets.
"""

import os
import sys
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


def is_sensitive(rel_posix: str) -> bool:
    name = rel_posix.rsplit("/", 1)[-1]
    if any(fnmatch(name, pat) for pat in NAME_PATTERNS):
        return True
    return any(fnmatch(rel_posix, pat) or fnmatch(rel_posix, "*/" + pat) for pat in PATH_PATTERNS)


def scan_for_secrets(root: str) -> list[str]:
    hits: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for filename in filenames:
            rel = os.path.relpath(os.path.join(dirpath, filename), root)
            rel_posix = rel.replace(os.sep, "/")
            if is_sensitive(rel_posix):
                hits.append(rel_posix)
    return sorted(hits)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <directory>", file=sys.stderr)
        return 2
    root = argv[1]
    hits = scan_for_secrets(root)
    if not hits:
        print(f"clean: no credential files found under {root}")
        return 0
    print(f"BLOCK: {len(hits)} credential file(s) under {root} — do not mount:")
    for path in hits:
        print(f"  {path}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
