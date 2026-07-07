"""Reference solution for the chapter 10 container-hardening audit."""


def _values(args: list[str], flag: str) -> list[str]:
    """All values given to `flag`, whether as `--flag val` or `--flag=val`."""
    out: list[str] = []
    for i, tok in enumerate(args):
        if tok == flag:
            if i + 1 < len(args):
                out.append(args[i + 1])
        elif tok.startswith(flag + "="):
            out.append(tok.split("=", 1)[1])
    return out


def missing_hardening(args: list[str]) -> list[str]:
    missing: list[str] = []

    if "ALL" not in [v.upper() for v in _values(args, "--cap-drop")]:
        missing.append("cap-drop-all")

    secopts = _values(args, "--security-opt")
    if not any(v.startswith("no-new-privileges") for v in secopts):
        missing.append("no-new-privileges")

    if "--read-only" not in args:
        missing.append("read-only")

    if "none" not in _values(args, "--network"):
        missing.append("network-isolated")

    users = _values(args, "--user")
    uids = [u.split(":", 1)[0] for u in users]
    if (
        not users
        or any(uid == "0" or uid == "root" for uid in uids)
        or all(uid == "" for uid in uids)
    ):
        missing.append("non-root")

    if not _values(args, "--pids-limit"):
        missing.append("pids-limit")

    if not _values(args, "--memory"):
        missing.append("memory-limit")

    return sorted(missing)
