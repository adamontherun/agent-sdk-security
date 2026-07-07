"""Chapter 9 challenge — a documented-behavior model of the built-in sandbox.

This is NOT Claude Code's sandbox engine. It is a small teaching simulation of
the *documented* filesystem and credential rules from
https://code.claude.com/docs/en/sandboxing, so you can reason about what a given
`sandbox.filesystem` / `sandbox.credentials` config would allow before you rely
on the real thing. The real enforcement is Seatbelt/bubblewrap at the OS level.

Implement `evaluate(config, request)` to return "allow" or "deny".

`config` looks like:
    {
        "cwd": "/home/agent/project",
        "tmpdir": "/tmp/claude-xyz",
        "home": "/home/agent",
        "filesystem": {
            "allowWrite": ["/home/agent/.kube"],
            "denyWrite": [],
            "denyRead": [],
            "allowRead": [],
        },
        "credentials": {
            "denyFiles": ["/home/agent/.aws"],   # mode: deny
            "denyEnv": ["GITHUB_TOKEN"],          # mode: deny
        },
    }

`request` is one of:
    {"op": "write", "path": "/home/agent/project/out.txt"}
    {"op": "read",  "path": "/home/agent/.aws/credentials"}
    {"op": "env",   "name": "GITHUB_TOKEN"}

Paths may use a leading "~/" which expands against config["home"].

The documented defaults you must model:
  * write: allowed only under cwd or tmpdir, or under a filesystem.allowWrite
    path; a filesystem.denyWrite path always blocks.
  * read: allowed *everywhere by default* (this is the footgun the chapter is
    about) EXCEPT paths under a filesystem.denyRead region or a credentials
    denyFiles entry. A filesystem.allowRead path re-allows within a denyRead
    region. A credentials denyFiles entry cannot be re-allowed.
  * env: allowed unless the variable name is in credentials denyEnv.
"""


def evaluate(config: dict, request: dict) -> str:
    raise NotImplementedError()
