GOOD = {
    "boot-source": {"kernel_image_path": "/images/vmlinux"},
    "drives": [
        {"drive_id": "rootfs", "is_root_device": True, "path_on_host": "/images/rootfs.ext4"}
    ],
    "machine-config": {"vcpu_count": 2, "mem_size_mib": 1024},
    "vsock": {"guest_cid": 3, "uds_path": "/run/fc.vsock"},
    "network-interfaces": [],
}


def _without(key):
    return {k: v for k, v in GOOD.items() if k != key}


def test_valid_isolated_config(subject):
    assert subject.validate_microvm_config(GOOD) == []


def test_missing_boot_source(subject):
    assert "missing-boot-source" in subject.validate_microvm_config(_without("boot-source"))


def test_missing_root_drive(subject):
    cfg = dict(GOOD)
    cfg["drives"] = [{"drive_id": "data", "is_root_device": False}]
    assert "missing-root-drive" in subject.validate_microvm_config(cfg)


def test_missing_machine_config(subject):
    cfg = dict(GOOD)
    cfg["machine-config"] = {"vcpu_count": 0, "mem_size_mib": 0}
    assert "missing-machine-config" in subject.validate_microvm_config(cfg)


def test_external_nic_breaks_isolation(subject):
    cfg = dict(GOOD)
    cfg["network-interfaces"] = [{"iface_id": "eth0", "host_dev_name": "tap0"}]
    assert "external-nic-present" in subject.validate_microvm_config(cfg)


def test_missing_vsock(subject):
    assert "missing-vsock" in subject.validate_microvm_config(_without("vsock"))
