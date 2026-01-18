# Security Implementation

This document describes the security measures implemented in the OctoPrint-PSUControl-eWeLink plugin.

## Overview

The plugin handles sensitive credentials (eWeLink email and password). Multiple layers of security prevent exposure:

| Layer | Protection |
|-------|------------|
| **UI** | Password field masked with `********` |
| **Storage** | XOR obfuscation with unique salt (prevents casual exposure) |
| **Transmission** | POST requests (not GET with URL params) |
| **API** | HTTPS to eWeLink cloud |

## 1. UI Password Masking

### Problem
OctoPrint's settings system syncs data to the browser. Without protection, the password would be visible in:
- The password input field (value attribute)
- Browser developer tools (JavaScript objects)
- Network inspector (settings payload)

### Solution

**JavaScript (`psucontrol_ewelink.js`):**

```javascript
self.onBeforeBinding = function() {
    // Mask password on initial load
    if (pluginSettings.password()) {
        pluginSettings.password("********");
    }

    // Re-mask if encrypted string appears after save
    pluginSettings.password.subscribe(function(newValue) {
        if (newValue && newValue.indexOf("ENC:") === 0) {
            pluginSettings.password("********");
        }
    });
};
```

**Key behaviors:**
- On page load: Real password replaced with `********`
- After save: If `ENC:...` string returns, immediately re-masked
- Test Connection: If password is `********`, sends empty string → backend uses stored password

## 2. Storage Obfuscation (XOR + Salt)

### Problem
OctoPrint stores settings in `~/.octoprint/config.yaml` as plain text:
```yaml
psucontrol_ewelink:
    password: my_secret_password  # BAD: Plain text!
```

### Solution

**Salt Generation:**
```python
def _get_salt(self):
    salt_path = os.path.join(self.get_plugin_data_folder(), "salt")
    if os.path.exists(salt_path):
        with open(salt_path, "rb") as f:
            self._salt = f.read()
    else:
        self._salt = os.urandom(32)  # 256-bit random salt
        with open(salt_path, "wb") as f:
            f.write(self._salt)
    return self._salt
```

**Encryption:**
```python
def _encrypt_password(self, plaintext):
    salt = self._get_salt()
    encrypted = self._xor(plaintext.encode('utf-8'), salt)
    return "ENC:" + binascii.hexlify(encrypted).decode('ascii')
```

**Result in config.yaml:**
```yaml
psucontrol_ewelink:
    password: ENC:ca421e6a2ab0a2eb201dc225e9  # Obfuscated
```

### Security Properties

| Property | Status |
|----------|--------|
| **Casual snooping** | ✅ Protected (password not human-readable) |
| **config.yaml theft** | ✅ Protected (salt file also required) |
| **Salt file theft** | ⚠️ Vulnerable (attacker can decrypt if both stolen) |
| **Memory inspection** | ⚠️ Vulnerable (password in memory briefly) |

> **Note**: This is obfuscation, not military-grade encryption. It prevents casual exposure but isn't designed to withstand targeted attacks with system access.

### Migration

Existing plain-text passwords are automatically encrypted on startup:

```python
def on_after_startup(self):
    stored_password = self._settings.get(["password"])
    if stored_password and not stored_password.startswith("ENC:"):
        self._logger.info("Migrating plaintext password...")
        encrypted = self._encrypt_password(stored_password)
        self._settings.set(["password"], encrypted)
        self._settings.save()
```

## 3. API Security

### POST Request Body

Credentials are sent in the POST request body, not in URL parameters:

```
POST /api/plugin/psucontrol_ewelink
Content-Type: application/json
{"command": "get_devices", "email": "...", "password": "..."}
```

This prevents credentials from appearing in:
- Browser history
- Server access logs
- URL bars

### Mask Handling

When "Test Connection" is clicked with a masked password:

1. Frontend sends: `{ "password": "" }` (empty string)
2. Backend detects empty password
3. Backend retrieves and decrypts stored password
4. Uses real password for API call

```python
if not password:
    stored_encrypted = self._settings.get(["password"])
    password = self._decrypt_password(stored_encrypted)
```

## 4. Settings Save Protection

### Problem
If user clicks "Save" while password shows `********`, this mask would overwrite the real password.

### Solution

```python
def on_settings_save(self, data):
    if data.get("password") == "********":
        data.pop("password", None)  # Don't save mask
    elif data.get("password"):
        data["password"] = self._encrypt_password(data["password"])  # Encrypt new password
```

## Files Affected

| File | Security Feature |
|------|-----------------|
| `__init__.py` | Encryption/decryption, mask handling, settings protection |
| `psucontrol_ewelink.js` | UI masking, subscription for re-masking |
| `~/.octoprint/data/psucontrol_ewelink/salt` | Encryption salt (generated on first run) |
| `~/.octoprint/config.yaml` | Contains `ENC:` obfuscated password |

## Recommendations

1. **Protect your Pi**: Standard Linux file permissions are the first line of defense
2. **Don't share config.yaml**: It contains your obfuscated password
3. **Use a dedicated eWeLink account**: Don't use your primary account if concerned
4. **Check logs**: Passwords are never logged by this plugin

---

📚 **More docs:** [README](../README.md) · [Troubleshooting](TROUBLESHOOTING.md) · [API](API.md) · [Architecture](ARCHITECTURE.md) · [Development](DEVELOPMENT.md) · [Changelog](CHANGELOG.md) · [Translations](TRANSLATIONS.md)
