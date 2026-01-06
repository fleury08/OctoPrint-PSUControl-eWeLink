/*
 * View model for OctoPrint-PSUControl-eWeLink
 *
 * Author: Christos Miniotis
 * License: MIT
 */
$(function () {
    function PSUControlEWeLinkSettingsViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];

        // Use onBeforeBinding to ensure we receive the settings object after initialization
        // and mask the password
        self.onBeforeBinding = function () {
            self.settings = self.settingsViewModel.settings;
            var pluginSettings = self.settings.plugins.psucontrol_ewelink;

            // Initial Masking
            if (pluginSettings.password()) {
                pluginSettings.password("********");
            }

            // Watch for updates (e.g. after save) to re-mask if ENC string comes back
            pluginSettings.password.subscribe(function (newValue) {
                if (newValue && newValue.indexOf("ENC:") === 0) {
                    pluginSettings.password("********");
                }
            });
        };

        self.deviceList = ko.observableArray([]);
        self.scanning = ko.observable(false);
        self.scanError = ko.observable("");
        self.scanSuccess = ko.observable("");

        self.isPSUControlInstalled = ko.pureComputed(function () {
            return self.settingsViewModel.settings &&
                self.settingsViewModel.settings.plugins &&
                self.settingsViewModel.settings.plugins.psucontrol;
        });

        self.isPSUControlConfigured = ko.pureComputed(function () {
            // Safety check: ensure settings and psucontrol plugin settings exist
            if (!self.isPSUControlInstalled()) {
                return true; // Don't show warning if we can't verify (or if PSUControl missing) -- handled by isPSUControlInstalled warning
            }

            var psu = self.settingsViewModel.settings.plugins.psucontrol;

            // Safety check for observables
            if (!psu.switchingMethod || !psu.switchingPlugin) {
                return true;
            }

            var switchingOk = psu.switchingMethod() === "PLUGIN" && psu.switchingPlugin() === "psucontrol_ewelink";

            // For sensing, also check if configured (optional but recommended)
            var sensingOk = true;
            if (psu.sensingMethod && psu.sensingPlugin) {
                // Only check if sensing is set to PLUGIN
                if (psu.sensingMethod() === "PLUGIN") {
                    sensingOk = psu.sensingPlugin() === "psucontrol_ewelink";
                }
            }

            return switchingOk && sensingOk;
        });

        self.isSensingConfigured = ko.pureComputed(function () {
            if (!self.settingsViewModel.settings ||
                !self.settingsViewModel.settings.plugins ||
                !self.settingsViewModel.settings.plugins.psucontrol) {
                return true;
            }
            var psu = self.settingsViewModel.settings.plugins.psucontrol;
            if (!psu.sensingMethod || !psu.sensingPlugin) {
                return true;
            }
            return psu.sensingMethod() === "PLUGIN" && psu.sensingPlugin() === "psucontrol_ewelink";
        });

        self.testConnection = function () {
            self.scanning(true);
            self.scanError("");
            self.scanSuccess("");
            self.deviceList([]);

            // safely access settings
            var pluginSettings = self.settingsViewModel.settings.plugins.psucontrol_ewelink;
            var email = pluginSettings.email();
            var password = pluginSettings.password();

            // Handle mask: if password is mask, send empty string to use stored password
            if (password === "********") {
                password = "";
            }

            if (!email || (!password && !pluginSettings.password())) { // Check logic: if password empty AND stored logic fails (masked)
                // Actually if password is "" and original was mask, we are fine. 
                // We just need to check if user has entered nothing AND it was not masked
                // But simplified:
            }

            if (!email) {
                var err = "Please enter Email.";
                self.scanError(err);
                self.scanning(false);
                new PNotify({ title: 'Error', text: err, type: 'error' });
                return;
            }

            if (!password && pluginSettings.password() !== "********") {
                // Logic check: if password is empty string, it might be fallback. 
                // But wait, we set password="" above if it was mask.
                // So if password is "" here, it means we want backend fallback.
                // But if the user CLEARED the box, password is "". 
                // If the box was empty to begin with? 
                // Let's rely on backend check or simple check here.
            }

            // Correct Logic:
            // If password is still empty string here, it means it was mask (so we send empty) OR user typed nothing.
            // If user typed nothing, backend will try stored. If stored is empty, backend fails.
            // So we can send it freely.

            if (!email || (!password && pluginSettings.password() !== "********" && !pluginSettings.password())) {
                // This check is getting complex. Let's simplify and let backend valid.
                // Actually, if we just check for email, that's enough, because password might be stored.
            }

            OctoPrint.simpleApiCommand("psucontrol_ewelink", "get_devices", {
                email: email,
                password: password
            })
                .done(function (response) {
                    if (response.error) {
                        self.scanError(response.error);
                        new PNotify({
                            title: 'eWeLink Error',
                            text: response.error,
                            type: 'error',
                            hide: false
                        });
                    } else if (response.devices) {
                        self.deviceList(response.devices);
                        var successMsg = "Found " + response.devices.length + " devices!";
                        self.scanSuccess(successMsg);
                        new PNotify({
                            title: 'eWeLink Connected',
                            text: successMsg,
                            type: 'success'
                        });
                    }
                })
                .fail(function (xhr) {
                    var msg = "API Request failed";
                    if (xhr.responseJSON && xhr.responseJSON.error) {
                        msg = xhr.responseJSON.error;
                    }
                    self.scanError(msg);
                    new PNotify({
                        title: 'Connection Failed',
                        text: msg,
                        type: 'error',
                        hide: false
                    });
                })
                .always(function () {
                    self.scanning(false);
                });
        };

        self.selectDevice = function (device) {
            self.settingsViewModel.settings.plugins.psucontrol_ewelink.device_id(device.deviceid);
            // Optionally verify selection
            new PNotify({
                title: 'Device Selected',
                text: 'Selected ' + device.name + ' (' + device.deviceid + ')',
                type: 'info'
            });
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: PSUControlEWeLinkSettingsViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#settings_plugin_psucontrol_ewelink"]
    });
});
