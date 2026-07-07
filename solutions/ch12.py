"""Reference solution for the chapter 12 microVM config validator."""


def validate_microvm_config(cfg: dict) -> list[str]:
    problems: list[str] = []

    if not cfg.get("boot-source", {}).get("kernel_image_path"):
        problems.append("missing-boot-source")

    drives = cfg.get("drives", [])
    if not any(d.get("is_root_device") for d in drives):
        problems.append("missing-root-drive")

    machine = cfg.get("machine-config", {})
    vcpus = machine.get("vcpu_count", 0)
    mem = machine.get("mem_size_mib", 0)
    if not (isinstance(vcpus, int) and vcpus > 0 and isinstance(mem, int) and mem > 0):
        problems.append("missing-machine-config")

    if cfg.get("network-interfaces"):
        problems.append("external-nic-present")

    if not cfg.get("vsock"):
        problems.append("missing-vsock")

    return sorted(problems)
