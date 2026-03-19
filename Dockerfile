FROM caddy:2.11.2-builder AS builder
# Don't change to caddy:2-builder to get automated updates
ADD . ./
RUN xcaddy build \
   --with github.com/caddy-dns/cloudflare \
   --with pkg.jsn.cam/caddy-defender \
   --with github.com/muety/caddy-remote-host \
   --with github.com/mholt/caddy-ratelimit

FROM caddy

COPY --from=builder /usr/bin/caddy /usr/bin/caddy

