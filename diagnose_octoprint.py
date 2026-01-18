
import sys
import octoprint
import octoprint.plugin

print(f"OctoPrint Version: {octoprint.__version__}")
print(f"Python Version: {sys.version}")
print("\n--- octoprint.plugin attributes ---")
try:
    for attr in dir(octoprint.plugin):
        print(attr)
except Exception as e:
    print(f"Error listing attributes: {e}")

print("\n--- TranslationPlugin check ---")
if hasattr(octoprint.plugin, 'TranslationPlugin'):
    print("TranslationPlugin FOUND in octoprint.plugin")
else:
    print("TranslationPlugin NOT FOUND in octoprint.plugin")

import inspect
print("\n--- Inspecting octoprint.plugin source file ---")
print(inspect.getfile(octoprint.plugin))
