#!/usr/bin/env bash
# REFERENCE ONLY, not executed on this macOS build machine (Firecracker needs
# Linux + KVM). This is the API-call form of the same microVM described in
# firecracker-vm-config.json, one PUT per resource, matching the official
# getting-started guide:
#   https://github.com/firecracker-microvm/firecracker/blob/main/docs/getting-started.md
# The vsock body fields are from docs/vsock.md; note there is deliberately no
# /network-interfaces call, so the guest gets no virtio-net device. Its only
# path off the box is the vsock UDS, which a host-side proxy listens on.
set -euo pipefail
API_SOCKET=/run/fc.sock
KERNEL=/images/vmlinux-6.1
ROOTFS=/images/agent-rootfs.ext4

# 1. Kernel + boot args
curl -X PUT --unix-socket "${API_SOCKET}" \
  --data "{\"kernel_image_path\": \"${KERNEL}\", \"boot_args\": \"console=ttyS0 reboot=k panic=1 pci=off\"}" \
  "http://localhost/boot-source"

# 2. Root filesystem
curl -X PUT --unix-socket "${API_SOCKET}" \
  --data "{\"drive_id\": \"rootfs\", \"path_on_host\": \"${ROOTFS}\", \"is_root_device\": true, \"is_read_only\": false}" \
  "http://localhost/drives/rootfs"

# 3. CPU + memory
curl -X PUT --unix-socket "${API_SOCKET}" \
  --data '{"vcpu_count": 2, "mem_size_mib": 1024}' \
  "http://localhost/machine-config"

# 4. vsock for host<->guest comms (no NIC anywhere in this config)
curl -X PUT --unix-socket "${API_SOCKET}" \
  --data '{"guest_cid": 3, "uds_path": "/run/fc.vsock"}' \
  "http://localhost/vsock"

# 5. Boot it
curl -X PUT --unix-socket "${API_SOCKET}" \
  --data '{"action_type": "InstanceStart"}' \
  "http://localhost/actions"
