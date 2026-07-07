#!/bin/sh
# Generate the proxy's own certificate authority. Squid uses this CA to mint
# per-site certificates on the fly when it bumps (decrypts) a TLS connection,
# so any client that is going to trust the bumped connection must also trust
# this CA. The private key here is what makes the person-in-the-middle
# possible; treat it as a secret and never ship it to the agent's side of the
# boundary. certs/ is gitignored for exactly this reason.
set -eu

DIR="$(cd "$(dirname "$0")" && pwd)/certs"
mkdir -p "$DIR"

if [ -f "$DIR/squid-ca.pem" ]; then
  echo "CA already exists at $DIR/squid-ca.pem — delete it to regenerate."
  exit 0
fi

# A 10-year self-signed CA. -nodes leaves the key unencrypted so Squid can
# read it unattended; the compensating control is filesystem permissions and
# keeping the key outside the agent boundary, not a passphrase.
openssl req -new -newkey rsa:2048 -sha256 -days 3650 -nodes -x509 \
  -keyout "$DIR/squid-ca.key" \
  -out "$DIR/squid-ca.pem" \
  -subj "/C=US/O=Agent SDK Security Lab/CN=Squid Egress Proxy CA"

chmod 600 "$DIR/squid-ca.key"
echo "Wrote $DIR/squid-ca.pem and $DIR/squid-ca.key"
