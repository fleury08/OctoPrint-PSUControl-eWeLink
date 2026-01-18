# Privacy Policy

**Last updated:** January 6, 2026

This privacy policy describes how the OctoPrint-PSUControl-eWeLink plugin handles your data.

## Data Collection

This plugin collects and transmits the following data to eWeLink's cloud servers:

- **eWeLink account email** - Used for authentication
- **eWeLink account password** - Transmitted securely over HTTPS for authentication
- **Device control commands** - On/off commands sent to your selected device

## Data Storage

### Local Storage
- Credentials are stored locally in OctoPrint's `config.yaml` file
- Passwords are obfuscated using XOR with a randomly generated local salt
- The obfuscation salt is stored in the plugin's data folder
- No plaintext passwords are stored

### External Storage
- No data is collected or stored by the plugin author
- eWeLink stores data according to their own privacy policy

## Third-Party Services

This plugin uses [eWeLink's](https://ewelink.cc/) cloud API to communicate with your smart devices. Please refer to [eWeLink's Privacy Policy](https://web.ewelink.cc/privacy-policy.html) for their data handling practices.

**No other third-party services are used by this plugin.**

## Data Security

- All API communications use HTTPS encryption
- Passwords are never stored in plaintext locally
- Passwords are masked in the OctoPrint web interface
- No credentials are logged or exposed in console output

## Data Sharing

This plugin does **not**:
- Send any data to the plugin author
- Include analytics or tracking
- Share your data with any parties other than eWeLink

## Your Rights

You can:
- Delete your stored credentials at any time through OctoPrint settings
- Uninstall the plugin to remove all locally stored data
- Request data deletion from eWeLink according to their policies

## Contact

For questions about this privacy policy, please open an issue on [GitHub](https://github.com/chrismin13/OctoPrint-PSUControl-eWeLink/issues).

---

📚 **More docs:** [README](README.md) · [Troubleshooting](docs/TROUBLESHOOTING.md) · [Security](docs/SECURITY.md) · [API](docs/API.md) · [Architecture](docs/ARCHITECTURE.md) · [Development](docs/DEVELOPMENT.md) · [Changelog](docs/CHANGELOG.md) · [Translations](docs/TRANSLATIONS.md)
