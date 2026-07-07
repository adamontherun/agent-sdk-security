"""Chapter 11 challenge — validate a gVisor (runsc) Docker setup.

Running an agent under gVisor takes two things that have to agree: the daemon
must have the `runsc` runtime registered, and the container has to actually
select it. Either half alone does nothing.

Implement `validate_runsc_setup(daemon_json, run_args)` returning a sorted list
of problem keys ([] means the setup is correct).

`daemon_json` is the parsed contents of /etc/docker/daemon.json, e.g.:
    {"runtimes": {"runsc": {"path": "/usr/local/bin/runsc"}}}

`run_args` are the `docker run` tokens, e.g. ["--runtime=runsc", "agent-image"]
or ["--runtime", "runsc", "agent-image"].

Problems to detect:
  * "runtime-not-registered" -> daemon_json has no runtimes.runsc.path
  * "runtime-not-selected"   -> run_args does not pass `--runtime runsc`
                                (two-token or `=` form)
"""


def validate_runsc_setup(daemon_json: dict, run_args: list[str]) -> list[str]:
    raise NotImplementedError()
