# Caddy builder with modules

This repo builds custom docker a custom image for caddy with the modules that I use. This is for my personal
use, but feel free to use the image if it fits your needs.

The container is [available on GHCR](https://ghcr.io/sintan1729/caddy-custom).

A workflow checks updates for `caddy` and the plugins daily, and builds new docker images whenever necessary.

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/sintan1729/custom-caddy-builder/update-and-release.yml)](https://github.com/SinTan1729/custom-caddy-builder/actions/workflows/update-and-release.yml)

## Modules

- [github.com/caddy-dns/cloudflare](https://pkg.go.dev/github.com/caddy-dns/cloudflare)
- [pkg.jsn.cam/caddy-defender](https://pkg.go.dev/pkg.jsn.cam/caddy-defender)
- [github.com/mholt/caddy-ratelimit](https://pkg.go.dev/github.com/mholt/caddy-ratelimit)
