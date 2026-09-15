FROM caddy:2.11.4-builder-alpine AS builder

RUN go install github.com/caddyserver/xcaddy/cmd/xcaddy@v0.10.1
WORKDIR /app
RUN git clone https://github.com/JasonLovesDoggo/caddy-defender.git

WORKDIR /app/caddy-defender
RUN go run ranges/main.go --fetch-tor

RUN xcaddy build \
   --with github.com/caddy-dns/cloudflare@v0.2.4 \
   --with pkg.jsn.cam/caddy-defender@v0.10.1 \
   --with github.com/mholt/caddy-ratelimit@v0.1.0 \
   --with github.com/caddy-dns/desec@v1.1.0

RUN mv /app/caddy-defender/caddy /usr/bin/caddy

# The actual shipped container
FROM caddy:2.11.4-alpine
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
