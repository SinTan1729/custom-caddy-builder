# Caddy builder with modules

This repo builds custom docker a custom image for caddy with the modules that I use. This is for my personal
use, but feel free to use the image if it fits your needs.

The container is [available on GHCR](https://ghcr.io/sintan1729/caddy-custom).

It's built monthly, and whenever a new version of caddy is released.

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/sintan1729/custom-caddy-builder/main.yml)

## Modules

- [github.com/caddy-dns/cloudflare](https://github.com/caddy-dns/cloudflare)
- [pkg.jsn.cam/caddy-defender](https://pkg.jsn.cam/caddy-defender)
- [github.com/muety/caddy-remote-host](https://github.com/muety/caddy-remote-host)
- [github.com/mholt/caddy-ratelimit](https://github.com/mholt/caddy-ratelimit)
