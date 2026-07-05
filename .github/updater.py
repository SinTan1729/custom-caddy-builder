#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025-2026 Sayantan Santra <sayantan.santra689@gmail.com>
# SPDX-License-Identifier: MIT

# Update versions of caddy-builder and plugins

import time
import requests
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DOCKERFILE = Path(sys.argv[1] if len(sys.argv) > 1 else "Dockerfile")
SUMMARY_FILE = Path("./update-summary.txt")

if not DOCKERFILE.exists():
    raise SystemExit(f"Dockerfile not found: {DOCKERFILE}")

SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
Version = tuple[int, int, int]


def http_json(url: str, headers: dict[str, str] | None = None) -> Any:
    req_headers = {
        "Accept": "application/json",
        **(headers or {}),
    }
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def github_json(url: str) -> Any:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return http_json(url, headers=headers)


def parse_semver(tag: str) -> Version | None:
    m = SEMVER_RE.fullmatch(tag)
    if not m:
        return None
    major, minor, patch = (int(x) for x in m.groups())
    return (major, minor, patch)


def latest_caddy_docker_tag() -> str:
    url = "https://hub.docker.com/v2/repositories/library/caddy/tags?page_size=100"
    candidates: list[Version] = []

    while url:
        data = http_json(url)
        for result in data.get("results", []):
            name = result.get("name", "")
            version = parse_semver(name)
            if version is not None:
                candidates.append(version)
        url = data.get("next")

    if not candidates:
        raise RuntimeError("No stable semver Docker tags found for library/caddy")

    candidates.sort(reverse=True)
    latest = candidates[0]
    return f"{latest[0]}.{latest[1]}.{latest[2]}"


def latest_plugin_version(repo: str) -> str:
    req = requests.get(f"https://pkg.go.dev/v1beta/versions/{repo}", timeout=3)
    req.raise_for_status()
    return req.json()["items"][0]["latestVersion"]


# ---------- Dockerfile parsing ----------


def current_caddy_version(text: str) -> str:
    m = re.search(r"(?m)^FROM caddy:([0-9]+\.[0-9]+\.[0-9]+)-builder AS builder$", text)
    if not m:
        raise RuntimeError("Could not find builder Caddy version in Dockerfile")
    return m.group(1)


def current_plugin_versions(text: str) -> dict[str, str]:
    """
    Parse:
      --with module@version
    """
    pairs = re.findall(r"--with\s+([^\s@\\]+)@([^\s\\]+)", text)
    if not pairs:
        raise RuntimeError(f"No versioned xcaddy plugins found in {DOCKERFILE}")
    # preserve first occurrence if repeated
    out: dict[str, str] = {}
    for module, version in pairs:
        out.setdefault(module, version)
    return out


def update_text(text: str, caddy_version: str, module_updates: dict[str, str]) -> str:
    # Update builder image
    text = re.sub(
        r"(?m)^FROM caddy:[0-9]+\.[0-9]+\.[0-9]+-builder AS builder$",
        f"FROM caddy:{caddy_version}-builder AS builder",
        text,
    )

    # Update runtime image
    text = re.sub(
        r"(?m)^FROM caddy:[0-9]+\.[0-9]+\.[0-9]+$",
        f"FROM caddy:{caddy_version}",
        text,
    )

    # Update plugin versions
    def repl(match: re.Match[str]) -> str:
        module = match.group(1)
        oldver = match.group(2)
        newver = module_updates.get(module, oldver)
        return f"--with {module}@{newver}"

    text = re.sub(
        r"--with\s+([^\s@\\]+)@([^\s\\]+)",
        repl,
        text,
    )

    return text


def write_summary(changes: list[dict[str, str]]) -> None:
    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    print("\nUpdates available:")
    for c in changes:
        msg = f"  {c['name']}: {c['from']} -> {c['to']}\n"
        print(msg)
        SUMMARY_FILE.write_text(msg)


def remove_summary_if_present() -> None:
    if SUMMARY_FILE.exists():
        SUMMARY_FILE.unlink()


def main() -> int:
    text = DOCKERFILE.read_text()

    current_caddy = current_caddy_version(text)
    current_plugins = current_plugin_versions(text)

    print("Checking versions...")
    print(f"Current caddy: v{current_caddy}")

    latest_caddy = latest_caddy_docker_tag()
    print(f"Latest caddy: v{latest_caddy}")

    latest_plugins: dict[str, str] = {}
    for module, current_version in current_plugins.items():
        print(f"Current {module}: {current_version}")
        latest_version = latest_plugin_version(module)
        latest_plugins[module] = latest_version
        print(f"Latest {module}: {latest_version}")
        time.sleep(1)

    new_text = update_text(text, latest_caddy, latest_plugins)

    changes: list[dict[str, str]] = []

    if current_caddy != latest_caddy:
        changes.append(
            {
                "name": "caddy",
                "from": current_caddy,
                "to": latest_caddy,
            }
        )

    for module, current_version in current_plugins.items():
        latest_version = latest_plugins[module]
        if current_version != latest_version:
            changes.append(
                {
                    "name": module,
                    "from": current_version,
                    "to": latest_version,
                }
            )

    if changes:
        DOCKERFILE.write_text(new_text)
        write_summary(changes)
        print(f"Updated {DOCKERFILE}")
        print(f"Wrote {SUMMARY_FILE}")
    else:
        remove_summary_if_present()
        print("No changes needed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
