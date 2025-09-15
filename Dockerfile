FROM caddy:2.10.2-builder AS builder
ADD . ./
RUN xcaddy build \
   --with github.com/caddy-dns/cloudflare \
   --with pkg.jsn.cam/caddy-defender \
   --with github.com/muety/caddy-remote-host \
   --with github.com/mholt/caddy-ratelimit

FROM caddy

COPY --from=builder /usr/bin/caddy /usr/bin/caddy

