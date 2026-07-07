"""Chapter 10 challenge — audit a `docker run` invocation against a minimum
hardening checklist.

You are handed the container's run arguments already split into tokens (the way
`shlex.split` would give them to you), for example:

    ["--cap-drop", "ALL", "--read-only", "--user", "1000:1000",
     "--network", "none", "--pids-limit", "128", "--memory", "512m", "agent-image"]

Implement `missing_hardening(args)` to return a sorted list of the checklist
keys that are NOT satisfied. A fully hardened invocation returns [].

The checklist (from the secure-deployment doc's hardened container example):
  * "cap-drop-all"      -> `--cap-drop ALL` present
  * "no-new-privileges" -> `--security-opt no-new-privileges` present
                           (the value may be "no-new-privileges" or
                            "no-new-privileges:true")
  * "read-only"         -> `--read-only` present
  * "network-isolated"  -> `--network none` present
  * "non-root"          -> `--user` present AND its uid is not 0
  * "pids-limit"        -> `--pids-limit` present
  * "memory-limit"      -> `--memory` present

Flags may be written as two tokens (`--user 1000:1000`) or joined with `=`
(`--user=1000:1000`). Handle both.
"""


def missing_hardening(args: list[str]) -> list[str]:
    raise NotImplementedError()
