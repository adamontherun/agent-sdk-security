# The stock ubuntu/squid image is built against GnuTLS and ships no
# security_file_certgen helper, so it cannot generate the per-site
# certificates that TLS bumping needs. Alpine's squid package is built
# --with-openssl and includes the helper, which is what makes chapter 15's
# decryption and header-injection steps actually work. We verified both facts
# by running `squid -v` inside the image (see chapter 15).
FROM alpine:3.20

RUN apk add --no-cache squid openssl ca-certificates \
 && rm -f /etc/squid/squid.conf

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 3128
ENTRYPOINT ["/entrypoint.sh"]
