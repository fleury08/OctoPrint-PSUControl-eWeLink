# Changelog

All notable changes to this project are documented in this file.

## [1.0.0] - 2026-01-06

Initial public release.

### Features
- **eWeLink Cloud Integration** - Control any eWeLink-compatible smart switch (Sonoff Basic, S26, etc.)
- **Device Discovery** - Test connection and browse devices directly in OctoPrint settings
- **State Sensing** - Real-time feedback on switch state through PSU Control
- **Secure Credentials** - Passwords encrypted locally using XOR obfuscation with unique salt
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
- Privacy Policy for cloud service usage
