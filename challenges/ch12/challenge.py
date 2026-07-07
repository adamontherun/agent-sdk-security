"""Chapter 12 challenge — validate a Firecracker microVM config for the
no-external-NIC isolation pattern.

Firecracker is configured by a sequence of API calls (boot-source, drives,
machine-config, and so on). This challenge works on a single merged dict that
collects those settings, and checks it matches the isolation pattern the
chapter describes: a real kernel and rootfs, sized CPU/memory, and NO external
network interface. The VM reaches the outside world only through a vsock to a
host-side proxy, never a virtio-net device.

Implement `validate_microvm_config(cfg)` returning a sorted list of problems.

`cfg` merges the API bodies, e.g.:
    {
        "boot-source": {"kernel_image_path": "/images/vmlinux"},
        "drives": [{"drive_id": "rootfs", "is_root_device": True,
                    "path_on_host": "/images/rootfs.ext4"}],
        "machine-config": {"vcpu_count": 2, "mem_size_mib": 1024},
        "vsock": {"guest_cid": 3, "uds_path": "/run/fc.vsock"},
        "network-interfaces": [],
    }

Problems to detect:
  * "missing-boot-source"   -> no boot-source.kernel_image_path
  * "missing-root-drive"    -> no drive with is_root_device True
  * "missing-machine-config"-> vcpu_count or mem_size_mib absent/not positive
  * "external-nic-present"  -> network-interfaces is non-empty (breaks the
                               vsock-only isolation pattern)
  * "missing-vsock"         -> no vsock block (the agent would have no way out)
"""


def validate_microvm_config(cfg: dict) -> list[str]:
    raise NotImplementedError()
