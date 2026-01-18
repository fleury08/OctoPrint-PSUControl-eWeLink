---
description: Start a new conversation about the PSUControl-eWeLink plugin with full project context
---

# PSUControl-eWeLink Project Context

**Project:** OctoPrint plugin integrating eWeLink smart switches (Sonoff, etc.) with PSU Control

## Project Structure

```
ewelink-psucontrol/                    # Parent workspace directory
├── OctoPrint-PSUControl-eWeLink/      # Main plugin repository
│   ├── octoprint_psucontrol_ewelink/  # Plugin Python package
│   ├── extras/psucontrol_ewelink.md   # Local copy of registry metadata
│   ├── docs/                          # Documentation
│   └── pyproject.toml                # Version, dependencies, metadata
│
└── plugins.octoprint.org/             # Official OctoPrint plugin registry (fork)
    └── _plugins/psucontrol_ewelink.md # Registry metadata (submit via PR)
```

## Quick Links

| Resource | Path |
|----------|------|
| **Main Plugin** | `@[OctoPrint-PSUControl-eWeLink]` |
| **Plugin Registry (local)** | `extras/psucontrol_ewelink.md` |
| **Plugin Registry (official)** | `../plugins.octoprint.org/_plugins/psucontrol_ewelink.md` |
| **OctoPrint Instance** | http://octopi.tail01e1b4.ts.net/ |

## Files That Must Stay in Sync

When changing these values, update **all** locations:

| Value | Files to Update |
|-------|-----------------|
| **Python version** | `pyproject.toml`, `__init__.py` (`__plugin_pythoncompat__`), `extras/psucontrol_ewelink.md`, `plugins.octoprint.org/.../psucontrol_ewelink.md`, `docs/TROUBLESHOOTING.md` |
| **Plugin version** | `pyproject.toml` (line 7), `docs/CHANGELOG.md` |
| **Description/features** | `extras/psucontrol_ewelink.md`, `plugins.octoprint.org/.../psucontrol_ewelink.md`, `README.md` |
| **Dependencies** | `pyproject.toml` (`project.dependencies`) |
| **OctoPrint compatibility** | `extras/psucontrol_ewelink.md`, `plugins.octoprint.org/.../psucontrol_ewelink.md` |

## Core Files

| File | Description |
|------|-------------|
| [`__init__.py`](octoprint_psucontrol_ewelink/__init__.py) | Main plugin class, API handlers, obfuscation |
| [`psucontrol_ewelink.js`](octoprint_psucontrol_ewelink/static/js/psucontrol_ewelink.js) | Settings UI logic (Knockout.js) |
| [`psucontrol_ewelink_settings.jinja2`](octoprint_psucontrol_ewelink/templates/psucontrol_ewelink_settings.jinja2) | Settings HTML template |
| [`pyproject.toml`](pyproject.toml) | Version (line 7), dependencies, metadata |

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

1. Bump version in `pyproject.toml` (line 7)
2. Update `docs/CHANGELOG.md`
3. **Commit ALL files**: Always `git add .` (or specific files) to ensure **all** changes (including compiled translations, modified source, etc.) are included.
4. Push to main → GitHub Action creates release
5. Update `plugins.octoprint.org` repo if description/features changed

## My Request

[Describe your task here]
