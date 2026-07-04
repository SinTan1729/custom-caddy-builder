FROM caddy:2.11.4-builder AS builder
ADD . ./
RUN xcaddy build \
   --with github.com/caddy-dns/cloudflare@v0.2.4 \
   --with pkg.jsn.cam/caddy-defender@v0.10.0 \
   --with github.com/mholt/caddy-ratelimit@v0.1.0

FROM caddy

COPY --from=builder /usr/bin/caddy /usr/bin/caddy

