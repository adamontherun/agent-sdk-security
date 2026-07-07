# Bake the allowlist config into the sidecar image. The stock ubuntu/squid
# image ships an allow-all config, so shipping our squid.conf is what turns it
# into an egress control. Build and push to the ECR repo referenced by the
# squid_image Terraform variable.
FROM ubuntu/squid:6.6-24.04_beta

COPY squid.conf /etc/squid/squid.conf
