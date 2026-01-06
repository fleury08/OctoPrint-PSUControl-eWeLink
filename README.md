# OctoPrint-PSUControl-eWeLink

Integrate [eWeLink](https://ewelink.cc/) smart switches (Sonoff, etc.) with [OctoPrint-PSUControl](https://github.com/kantlivelong/OctoPrint-PSUControl) to turn your 3D printer on and off.

## Requirements

*   **OctoPrint**: 1.3.10 or higher
*   **OctoPrint-PSUControl**: Installed and configured
*   **eWeLink Account**: Email and Password
*   **eWeLink Device**: A smart switch (e.g., Sonoff Basic, S26) connected to your printer

## Installation

### Plugin Manager (Recommended)
1.  Open the **OctoPrint Settings**.
2.  Go to **Plugin Manager** > **Get More**.
3.  Search for **PSUControl-eWeLink**.
4.  Click **Install**.

### Manual Installation
1.  Copy the URL of this repository.
2.  Open **OctoPrint Settings** > **Plugin Manager** > **Get More**.
3.  Paste the URL into the **... form URL** field and click **Install**.

## Configuration

1.  Open **OctoPrint Settings** and navigate to **PSU Control - eWeLink** (under Plugins).
2.  Enter your **eWeLink Email** and **Password**.
3.  Click **Test Connection / Get Devices**. 
    *   This will check your credentials and fetch your available devices.
    *   The region is auto-detected by the eWeLink API.
4.  Select your printer's smart switch from the **Device ID** dropdown.
5.  Click **Save**.
6.  Navigate to **PSU Control** settings.
7.  Set **Switching Method** to **Plugin**.
8.  Select **OctoPrint-PSUControl-eWeLink** from the plugin list.

## Security

This plugin takes security seriously:
*   **Encrypted Storage**: Credentials are NOT stored in plain text. They are scrambled using a local salt (XOR Obfuscation) in `config.yaml`.
*   **UI Masking**: Passwords are masked (`********`) in the settings UI and stripped from the browser memory.
*   **Secure API**: Credentials are transmitted to the eWeLink API over HTTPS.

## Documentation

| Document | Description |
|----------|-------------|
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues and solutions |
| [Security](docs/SECURITY.md) | How credentials are protected |
| [API Reference](docs/API.md) | Internal APIs and integration points |
| [Architecture](docs/ARCHITECTURE.md) | Technical design overview |
| [Development](docs/DEVELOPMENT.md) | Setup for contributors |
| [Changelog](docs/CHANGELOG.md) | Version history |
| [Privacy Policy](PRIVACY.md) | Data handling practices |

## License

MIT
