# Changelog

All notable changes to this project are documented in this file.

## [1.0.6] - 2026-01-18

### Added
- **EditorConfig** - Added `.editorconfig` for consistent code style across editors
- **MANIFEST.in** - Added manifest file for proper PyPI source distribution packaging
- **GitHub Issue Templates** - Added structured bug report and feature request forms
- **Modern Packaging** - Migrated from `setup.py` to `pyproject.toml` (PEP 517/518)

### Changed
- **Version Location** - Version now in `pyproject.toml` (line 7) instead of `setup.py`

### Maintenance
- **Code Style** - Fixed all files for editorconfig compliance (trailing whitespace, tabs→spaces, indentation)
- **Documentation** - Updated README and project-context workflow to reflect pyproject.toml migration

## [1.0.4] - 2026-01-16

### Security
- **API Protection** - Added `is_api_adminonly()` to restrict API access to admin users only
- **XSS Prevention** - Added `text_escape: true` to all PNotify notifications to prevent XSS from untrusted cloud data (device names, error messages)

### Changed
- **Terminology** - Rebranded "encryption" to "obfuscation" throughout documentation to honestly describe XOR-based password protection

### Documentation
- **README** - Added release process instructions
- **SECURITY.md** - Clarified that storage protection prevents casual exposure, not targeted attacks

## [1.0.3] - 2026-01-07

### Maintenance
- **Repository** - Prepared for official plugin repository submission.
- **Metadata** - Added privacy policy links and screenshots to registration data.
- **Packaging** - Cleaned up `setup.py` and `MANIFEST.in`.

## [1.0.1] - 2026-01-06

### Fixed
- **Configuration** - Added a prominent error message when the required `OctoPrint-PSUControl` plugin is missing.
- **Documentation** - Updated troubleshooting guide with "Missing Requirement" error.

## [1.0.0] - 2026-01-06

Initial public release.

### Features
- **eWeLink Cloud Integration** - Control any eWeLink-compatible smart switch (Sonoff Basic, S26, etc.)
- **Device Discovery** - Test connection and browse devices directly in OctoPrint settings
- **State Sensing** - Real-time feedback on switch state through PSU Control
- **Secure Credentials** - Passwords obfuscated locally using XOR with unique salt
- **Region Auto-Detection** - No manual region configuration needed; API automatically detects correct region
- **Password Masking** - UI shows `********` instead of real password
- **Configuration Warnings** - Alerts if PSU Control not properly configured to use this plugin

### Technical
- Asyncio bridge for eWeLink library
- Background thread for event loop
- POST-based API for secure credential handling
- Software update support via OctoPrint's update mechanism

### Documentation
- Complete documentation suite: README, SECURITY, TROUBLESHOOTING, API, ARCHITECTURE, DEVELOPMENT

---

📚 **More docs:** [README](../README.md) · [Troubleshooting](TROUBLESHOOTING.md) · [Security](SECURITY.md) · [API](API.md) · [Architecture](ARCHITECTURE.md) · [Development](DEVELOPMENT.md)
- Privacy Policy for cloud service usage
