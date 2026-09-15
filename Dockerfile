FROM caddy:2.11.4-builder-alpine AS builder

WORKDIR /app
RUN git clone https://github.com/JasonLovesDoggo/caddy-defender --branch v0.10.1

WORKDIR /app/caddy-defender
RUN go run ranges/main.go --fetch-tor

WORKDIR /usr/bin
RUN xcaddy build \
   --with github.com/caddy-dns/cloudflare@v0.2.4 \
   --with pkg.jsn.cam/caddy-defender@v0.10.1=/app/caddy-defender \
   --with github.com/mholt/caddy-ratelimit@v0.1.0 \
   --with github.com/caddy-dns/desec@v1.1.0

# The actual shipped container
FROM caddy:2.11.4-alpine
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
