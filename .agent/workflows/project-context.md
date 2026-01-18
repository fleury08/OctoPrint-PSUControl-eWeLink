---
description: Start a new conversation about the PSUControl-eWeLink plugin with full project context
---

# PSUControl-eWeLink Project Context

**Project:** OctoPrint plugin integrating eWeLink smart switches (Sonoff, etc.) with PSU Control

## Quick Links

| Resource | Path |
|----------|------|
| **Main Plugin** | `@[OctoPrint-PSUControl-eWeLink]` |
| **Plugin Registry** | `../plugins.octoprint.org/_plugins/psucontrol_ewelink.md` |
| **OctoPrint Instance** | http://octopi.tail01e1b4.ts.net/ |

## Core Files

| File | Description |
|------|-------------|
| [`__init__.py`](octoprint_psucontrol_ewelink/__init__.py) | Main plugin class, API handlers, obfuscation |
| [`psucontrol_ewelink.js`](octoprint_psucontrol_ewelink/static/js/psucontrol_ewelink.js) | Settings UI logic (Knockout.js) |
| [`psucontrol_ewelink_settings.jinja2`](octoprint_psucontrol_ewelink/templates/psucontrol_ewelink_settings.jinja2) | Settings HTML template |
| [`setup.py`](setup.py) | Version (line 17), dependencies, metadata |

## Documentation

| Doc | Purpose |
|-----|---------|
| [`README.md`](README.md) | Overview, installation, configuration |
| [`docs/SECURITY.md`](docs/SECURITY.md) | Credential handling, obfuscation details |
| [`docs/API.md`](docs/API.md) | Endpoints, PSU Control integration |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Component diagram, async design |
| [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) | Setup, testing, guidelines |
| [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) | Common issues |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md) | Version history |
| [`PRIVACY.md`](PRIVACY.md) | Data handling policy |

## Tests

| File | Purpose |
|------|---------|
| [`tests/test_plugin.py`](tests/test_plugin.py) | Unit tests (17 tests) |

Run with: `python3 -m unittest tests/test_plugin.py`

## Architecture Notes

- **Async bridge**: Dedicated asyncio thread bridges sync OctoPrint with async eWeLink library
- **Credential storage**: XOR obfuscation with local salt (not encryption)
- **PSU Control integration**: Registers via helper system, exposes `turn_psu_on()`, `turn_psu_off()`, `get_psu_state()`

## Gotchas

- **Commits**: Always use [Conventional Commits](https://www.conventionalcommits.org/) format with one-line messages
  - Examples: `feat: add device discovery`, `fix: handle connection timeout`, `docs: update README`, `chore: bump Python version`
- See [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) for known quirks, workarounds, and guidelines.

## Release Process

1. Bump version in `setup.py` (line 17)
2. Update `docs/CHANGELOG.md`
3. Push to main → GitHub Action creates release
4. Update `plugins.octoprint.org` repo if description/features changed

## My Request

[Describe your task here]
