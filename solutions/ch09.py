"""Reference solution for the chapter 9 sandbox-decision model."""


def _expand(path: str, home: str) -> str:
    if path == "~":
        return home
    if path.startswith("~/"):
        return home.rstrip("/") + "/" + path[2:]
    return path


def _under(path: str, base: str) -> bool:
    """True if `path` is `base` itself or lives beneath it."""
    if base in ("", "/"):
        return True
    base = base.rstrip("/")
    return path == base or path.startswith(base + "/")


def _under_any(path: str, bases, home: str) -> bool:
    return any(_under(path, _expand(b, home)) for b in bases)


def evaluate(config: dict, request: dict) -> str:
    home = config.get("home", "")
    fs = config.get("filesystem", {})
    creds = config.get("credentials", {})
    op = request["op"]

    if op == "env":
        name = request["name"]
        return "deny" if name in creds.get("denyEnv", []) else "allow"

    path = _expand(request["path"], home)

    if op == "write":
        if _under_any(path, fs.get("denyWrite", []), home):
            return "deny"
        if _under(path, config.get("cwd", "")) or _under(path, config.get("tmpdir", "")):
            return "allow"
        if _under_any(path, fs.get("allowWrite", []), home):
            return "allow"
        return "deny"

    if op == "read":
        if _under_any(path, creds.get("denyFiles", []), home):
            return "deny"
        if _under_any(path, fs.get("denyRead", []), home):
            if _under_any(path, fs.get("allowRead", []), home):
                return "allow"
            return "deny"
        return "allow"

    raise ValueError(f"unknown op: {op!r}")
