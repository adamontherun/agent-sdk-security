"""Reference solution for the chapter 11 runsc-setup validator."""


def _runtime_selected(run_args: list[str]) -> bool:
    for i, tok in enumerate(run_args):
        if tok == "--runtime" and i + 1 < len(run_args) and run_args[i + 1] == "runsc":
            return True
        if tok == "--runtime=runsc":
            return True
    return False


def validate_runsc_setup(daemon_json: dict, run_args: list[str]) -> list[str]:
    problems: list[str] = []

    registered = daemon_json.get("runtimes", {}).get("runsc", {}).get("path")
    if not registered:
        problems.append("runtime-not-registered")

    if not _runtime_selected(run_args):
        problems.append("runtime-not-selected")

    return sorted(problems)
