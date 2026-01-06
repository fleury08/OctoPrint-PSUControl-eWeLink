#
# Test Suite for OctoPrint-PSUControl-eWeLink
#
# PURPOSE:
# This file contains "Unit Tests". These are automated checks to verify that 
# the plugin's logic works correctly in isolation. 
#
# IS THIS REQUIRED?
# No. The plugin will function perfectly fine on a printer without this file.
# However, it is HIGHLY RECOMMENDED for developers. It ensures that future changes
# (like updates or bug fixes) don't accidentally break existing features.
#
# HOW IT WORKS:
# Since we are running these tests on a computer that might not be a real OctoPrint server,
# we have to "Mock" (fake) the OctoPrint and eWeLink dependencies.
#

import sys
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import types
import asyncio

# Mock flask before any import
# OctoPrint uses Flask for its web server. We mock it here so we don't need a real web server running.
mock_flask = MagicMock()
sys.modules["flask"] = mock_flask

# Create dummy modules
# We create fake 'octoprint' and 'octoprint.plugin' modules so that when the plugin imports them,
# it gets our empty mock objects instead of failing with "ImportError".
mock_octoprint = types.ModuleType("octoprint")
sys.modules["octoprint"] = mock_octoprint

mock_op_plugin = types.ModuleType("octoprint.plugin")
sys.modules["octoprint.plugin"] = mock_op_plugin
mock_octoprint.plugin = mock_op_plugin


# Define base classes
class MockStartupPlugin(object):
    def on_after_startup(self):
        pass


class MockShutdownPlugin(object):
    def on_shutdown(self):
        pass


class MockTemplatePlugin(object):
    def get_template_configs(self):
        return []


class MockSettingsPlugin(object):
    def get_settings_defaults(self):
        return {}

    def on_settings_save(self, data):
        pass


class MockSimpleApiPlugin(object):
    def get_api_commands(self):
        return {}

    def on_api_command(self, command, data):
        pass


class MockAssetPlugin(object):
    def get_assets(self):
        return {}


class MockRestartNeedingPlugin(object):
    pass


mock_op_plugin.StartupPlugin = MockStartupPlugin
mock_op_plugin.ShutdownPlugin = MockShutdownPlugin
mock_op_plugin.TemplatePlugin = MockTemplatePlugin
mock_op_plugin.SettingsPlugin = MockSettingsPlugin
mock_op_plugin.SimpleApiPlugin = MockSimpleApiPlugin
mock_op_plugin.AssetPlugin = MockAssetPlugin
mock_op_plugin.RestartNeedingPlugin = MockRestartNeedingPlugin

# Mock ewelink module
# The real eWeLink library makes actual network calls to the cloud.
# We mock it here so our tests run instantly and don't actually toggle your real devices.
mock_ewelink_lib = MagicMock()
mock_ewelink_types = MagicMock()
sys.modules["ewelink"] = mock_ewelink_lib
sys.modules["ewelink.types"] = mock_ewelink_types
mock_ewelink_lib.types = mock_ewelink_types

# Now valid to import the plugin
# We need to add the parent directory to sys.path to find the plugin package
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from octoprint_psucontrol_ewelink import PSUControlEWeLinkPlugin, __plugin_load__


class TestPSUControlEWeLinkPlugin(unittest.TestCase):
    """
    The main test class. Each method starting with 'test_' becomes a separate check.
    """

    def setUp(self):
        """
        Runs before EACH test method.
        Creates a fresh instance of the plugin and replaces its internal components 
        (logger, settings, manager) with Mocks so we can track how they are used.
        """
        self.plugin = PSUControlEWeLinkPlugin()
        self.plugin._logger = MagicMock()
        self.plugin._settings = MagicMock()
        self.plugin._plugin_manager = MagicMock()
        self.plugin._plugin_version = "1.0.0"
        # Mock the data folder for encryption tests
        self.plugin.get_plugin_data_folder = MagicMock(
            return_value="/tmp/test_plugin_data"
        )

    def test_startup_registration(self):
        """Test that plugin registers with PSU Control on startup"""
        # Setup helpers
        mock_helpers = {"register_plugin": MagicMock()}
        self.plugin._plugin_manager.get_helpers.return_value = mock_helpers
        self.plugin._settings.get.return_value = None  # No credentials configured

        # Mock _start_loop to avoid async issues
        self.plugin._start_loop = MagicMock()
        self.plugin._init_ewelink = MagicMock()

        # Call startup
        self.plugin.on_after_startup()

        # Check registration
        self.plugin._plugin_manager.get_helpers.assert_called_with("psucontrol")
        mock_helpers["register_plugin"].assert_called_with(self.plugin)

    def test_settings_defaults(self):
        """Test default settings structure"""
        defaults = self.plugin.get_settings_defaults()
        self.assertIn("email", defaults)
        self.assertIn("password", defaults)
        self.assertIn("device_id", defaults)
        self.assertEqual(defaults["email"], "")
        self.assertEqual(defaults["password"], "")
        self.assertEqual(defaults["device_id"], "")

    def test_password_encryption(self):
        """Test password encryption and decryption"""
        # Create a temporary salt file
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            self.plugin.get_plugin_data_folder = MagicMock(return_value=tmpdir)
            self.plugin._salt = None  # Reset salt

            test_password = "mySecretPassword123"

            # Encrypt
            encrypted = self.plugin._encrypt_password(test_password)
            self.assertTrue(encrypted.startswith("ENC:"))
            self.assertNotEqual(encrypted, test_password)

            # Decrypt
            decrypted = self.plugin._decrypt_password(encrypted)
            self.assertEqual(decrypted, test_password)

    def test_password_encryption_idempotent(self):
        """Test that encrypting already encrypted password returns as-is"""
        encrypted = "ENC:abc123"
        result = self.plugin._encrypt_password(encrypted)
        self.assertEqual(result, encrypted)

    def test_password_decryption_plaintext(self):
        """Test that decrypting plaintext returns as-is"""
        plaintext = "notEncrypted"
        result = self.plugin._decrypt_password(plaintext)
        self.assertEqual(result, plaintext)

    def test_turn_psu_on_no_connection(self):
        """Test turn_psu_on when not connected logs warning"""
        self.plugin._ewelink_app = None
        self.plugin._settings.get.return_value = "device123"

        self.plugin.turn_psu_on()

        self.plugin._logger.warning.assert_called()

    def test_turn_psu_off_no_connection(self):
        """Test turn_psu_off when not connected logs warning"""
        self.plugin._ewelink_app = None
        self.plugin._settings.get.return_value = "device123"

        self.plugin.turn_psu_off()

        self.plugin._logger.warning.assert_called()

    def test_get_psu_state_no_connection(self):
        """Test get_psu_state returns False when not connected"""
        self.plugin._ewelink_app = None

        result = self.plugin.get_psu_state()

        self.assertFalse(result)

    def test_get_update_information(self):
        """Test software update hook returns correct info"""
        info = self.plugin.get_update_information()

        self.assertIn("psucontrol_ewelink", info)
        update_info = info["psucontrol_ewelink"]
        self.assertEqual(update_info["type"], "github_release")
        self.assertEqual(update_info["user"], "chrismin13")
        self.assertEqual(update_info["repo"], "OctoPrint-PSUControl-eWeLink")

    def test_get_template_configs(self):
        """Test template configuration"""
        configs = self.plugin.get_template_configs()

        self.assertEqual(len(configs), 1)
        self.assertEqual(configs[0]["type"], "settings")
        self.assertTrue(configs[0]["custom_bindings"])

    def test_get_assets(self):
        """Test asset registration"""
        assets = self.plugin.get_assets()

        self.assertIn("js", assets)
        self.assertIn("js/psucontrol_ewelink.js", assets["js"])

    def test_api_commands(self):
        """Test API command registration"""
        commands = self.plugin.get_api_commands()

        self.assertIn("get_devices", commands)

    def test_on_settings_save_masks_password(self):
        """Test that masked password is not saved"""
        data = {"email": "test@test.com", "password": "********"}

        # Mock parent save
        with patch.object(
            mock_op_plugin.SettingsPlugin, "on_settings_save"
        ) as mock_save:
            self.plugin._init_ewelink = MagicMock()
            self.plugin.on_settings_save(data)

            # Password should be removed from data
            self.assertNotIn("password", data)

    def test_on_settings_save_encrypts_new_password(self):
        """Test that new password gets encrypted"""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            self.plugin.get_plugin_data_folder = MagicMock(return_value=tmpdir)
            self.plugin._salt = None

            data = {"email": "test@test.com", "password": "newPassword123"}

            with patch.object(
                mock_op_plugin.SettingsPlugin, "on_settings_save"
            ) as mock_save:
                self.plugin._init_ewelink = MagicMock()
                self.plugin.on_settings_save(data)

                # Password should be encrypted
                self.assertTrue(data["password"].startswith("ENC:"))


    def test_on_api_command_get_devices_fallback(self):
        """Test API get_devices uses stored credentials if not provided"""
        # Data with empty password (simulating masked UI)
        data = {"email": "", "password": ""}
        
        # Mock settings to return stored credentials
        # side_effect: first call (email), second call (password)
        def get_side_effect(args):
            if args == ["email"]: return "stored@email.com"
            if args == ["password"]: return "ENC:stored_pass"
            return None
        self.plugin._settings.get.side_effect = get_side_effect
        
        # Mock decrypt
        self.plugin._decrypt_password = MagicMock(return_value="stored_pass")
        
        # Mock async runner and fetcher
        self.plugin._run_coro = MagicMock(return_value=[{"name": "TestDevice"}])
        self.plugin._async_fetch_devices = MagicMock()
        
        # Call command
        response = self.plugin.on_api_command("get_devices", data)
        
        # Verify
        self.plugin._async_fetch_devices.assert_called_with("stored@email.com", "stored_pass")
        self.plugin._run_coro.assert_called()

    def test_turn_psu_on_success(self):
        """Test turn_psu_on calls toggle_device when connected"""
        self.plugin._ewelink_app = MagicMock() # Connected
        self.plugin._settings.get.return_value = "device123"
        
        self.plugin._run_coro = MagicMock()
        self.plugin._toggle_device = MagicMock()
        
        self.plugin.turn_psu_on()
        
        self.plugin._toggle_device.assert_called_with("device123", "on")
        self.plugin._run_coro.assert_called()


class TestPluginLoad(unittest.TestCase):

    def test_plugin_load(self):
        """Test __plugin_load__ creates implementation and hooks"""
        __plugin_load__()

        # Check that globals are set (they're set in the module)
        from octoprint_psucontrol_ewelink import (
            __plugin_implementation__,
            __plugin_hooks__,
        )

        self.assertIsInstance(__plugin_implementation__, PSUControlEWeLinkPlugin)
        self.assertIn(
            "octoprint.plugin.softwareupdate.check_config", __plugin_hooks__
        )


if __name__ == "__main__":
    unittest.main()
