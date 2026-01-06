# Developer Notes & Contribution Guide

This document captures key technical decisions and learnings discovered during the development of the OctoPrint-PSUControl-eWeLink plugin.

## 1. Asynchronous Architecture
The `ewelink` Python library is completely asynchronous (`asyncio`/`aiohttp`). OctoPrint's plugin system is primarily synchronous.
*   **Problem**: Simply calling `asyncio.run()` inside OctoPrint hooks creates a new event loop for every call, which kills the persistent `aiohttp` session needed by the library.
*   **Solution**: We spawn a dedicated background thread (`self._loop_thread`) that runs a persistent `asyncio` event loop. All `ewelink` library calls are dispatched to this loop using `asyncio.run_coroutine_threadsafe`.

## 2. eWeLink App Credentials
*   **Critical**: The standard user email/password is NOT enough. The library also requires an "App ID" and "App Secret" to sign requests.
*   **Finding**: Generic or default credentials often fail with "invalid appid" or signature errors.
*   **Fix**: We successfully tested and hardcoded a known working set of credentials (extracted from the `SonoffLAN` Home Assistant integration).
    *   **App ID**: `R8Oq3y0eSZSYdKccHlrQzT1ACCOUT9Gv`
    *   **Secret**: `1ve5Qk9GXfUhKAn1svnKwpAlxXkMarru` (Do not change these unless confirmed broken).

## 3. Library Limitations & Workarounds
The `ewelink` Python library has some incomplete implementations.
*   `app.get_thing_list()` raises `NotImplementedError`.
*   Solution: We manually call `app._auth_request("GET", "v2/device/thing")` to get the raw device list.
*   Device object methods (`device.on()`, `device.off()`) were also unreliable.
*   Solution: We implemented `_toggle_device` helper to send raw `POST` requests to `v2/device/thing/status`.

## 4. OctoPrint Metadata & Syntax
*   **Pitfall**: OctoPrint reads `__init__.py` (AST parsing) to determine plugin metadata like `__plugin_pythoncompat__`.
*   **Warning**: If `__init__.py` contains **ANY** syntax error (even deep inside a method like an `IndentationError`), the AST parser may fail silently or partially, causing OctoPrint to default to generic values (e.g., claiming the plugin is "Python 2.7" compatible only).
*   **Best Practice**: 
    1.  Keep metadata (`__plugin_name__`, `__plugin_pythoncompat__`) at the very top of `__init__.py`.
    2.  Ensure strict syntax correctness before packaging.
    3.  Avoid complex top-level imports that might fail in environments with missing dependencies, although standard imports are fine if the environment is correct.

## 5. Region Auto-Detection

The eWeLink API automatically redirects to the correct region:

```python
# When logging in with wrong region:
await app.login(region="us")  # Account is actually EU

# API returns error 301 with correct region
# Library auto-retries with correct region
# Final result: login.region == "eu"
```

This allows us to remove the region dropdown entirely and just hardcode "us" as the initial attempt.

## 6. Password Security Flow

```
User enters password
    ↓
on_settings_save()
    ↓
_encrypt_password(plaintext)
    ↓
XOR with unique salt + hex encode
    ↓
Store as "ENC:abc123..." in config.yaml
    ↓
On load: _decrypt_password() reverses the process
```

Salt is stored in: `~/.octoprint/data/psucontrol_ewelink/salt`

## 7. PSU Control Integration Points

PSU Control discovers sub-plugins via a helper registration system:

```python
# On startup
helpers = self._plugin_manager.get_helpers("psucontrol")
helpers["register_plugin"](self)
```

PSU Control then calls these methods based on configuration:

| PSU Control Setting | Our Method Called |
|---------------------|-------------------|
| `switchingMethod = PLUGIN, switchingPlugin = psucontrol_ewelink` | `turn_psu_on()`, `turn_psu_off()` |
| `sensingMethod = PLUGIN, sensingPlugin = psucontrol_ewelink` | `get_psu_state()` |

## 8. Development Setup

```bash
# Clone and install in editable mode
cd /path/to/OctoPrint-PSUControl-eWeLink
pip install -e .

# Restart OctoPrint
sudo service octoprint restart

# Watch logs
tail -f ~/.octoprint/logs/octoprint.log | grep -i ewelink
```

## 9. Testing eWeLink API Locally

Create a test script:

```python
import asyncio
from ewelink import EWeLink
from ewelink.types import AppCredentials, EmailUserCredentials

async def test():
    app_cred = AppCredentials(
        id="R8Oq3y0eSZSYdKccHlrQzT1ACCOUT9Gv",
        secret="1ve5Qk9GXfUhKAn1svnKwpAlxXkMarru"
    )
    user_cred = EmailUserCredentials(email="your@email.com", password="yourpass")
    app = EWeLink(app_cred=app_cred, user_cred=user_cred)
    
    login = await app.login(region="us")
    print(f"Logged in! Region: {login.region}")
    
    resp = await app._auth_request("GET", "v2/device/thing")
    for thing in resp["thingList"]:
        item = thing.get("itemData", {})
        print(f"Device: {item.get('name')} ({item.get('deviceid')}) - {'Online' if item.get('online') else 'Offline'}")
    
    await app.close()

asyncio.run(test())
```

## 10. Documentation Index

- [ARCHITECTURE.md](ARCHITECTURE.md) - Component diagram, data flow
- [SECURITY.md](SECURITY.md) - Password obfuscation details
- [API.md](API.md) - Endpoint reference
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [CHANGELOG.md](CHANGELOG.md) - Version history
