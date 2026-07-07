#!/bin/sh
# Squid's bump helper keeps a small on-disk database of the certificates it has
# minted. It must be initialised once (the -c flag) before Squid starts, and it
# must be owned by the user Squid drops to (squid on Alpine). We build it under
# /var/lib/squid/ssl_db on every start so the container is stateless and a fresh
# `docker compose up` always comes up clean.
set -eu

SSL_DB=/var/lib/squid/ssl_db

if [ ! -d "$SSL_DB" ]; then
  mkdir -p /var/lib/squid
  /usr/lib/squid/security_file_certgen -c -s "$SSL_DB" -M 4MB
  chown -R squid:squid /var/lib/squid
fi

# Make sure the log and swap directories exist and are writable.
mkdir -p /var/log/squid /var/spool/squid
chown -R squid:squid /var/log/squid /var/spool/squid

# A `docker compose restart` reuses the container filesystem, so clear any PID
# file left by the previous process before starting a new one.
rm -f /run/squid.pid /var/run/squid.pid

# Validate the config, then run in the foreground (-N) with logging to stderr
# so `docker compose logs squid` shows access lines directly.
squid -k parse
exec squid -N -d1 -f /etc/squid/squid.conf
