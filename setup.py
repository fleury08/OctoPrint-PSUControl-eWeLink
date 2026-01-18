# coding=utf-8

########################################################################################################################
### Do not forget to adjust the following variables to your own plugin.

# The plugin's identifier, has to be unique
plugin_identifier = "psucontrol_ewelink"

# The plugin's python package, should be "octoprint_<plugin identifier>", has to be unique
plugin_package = "octoprint_psucontrol_ewelink"

# The plugin's human readable name. Can be overwritten within OctoPrint's internal data via __plugin_name__ in the
# plugin module
plugin_name = "PSU Control - eWeLink"

# The plugin's version. Can be overwritten within OctoPrint's internal data via __plugin_version__ in the plugin module
plugin_version = "1.0.5"

# The plugin's description. Can be overwritten within OctoPrint's internal data via __plugin_description__ in the plugin
# module
plugin_description = """Integrates eWeLink smart switches with OctoPrint PSU Control"""

# The plugin's author. Can be overwritten within OctoPrint's internal data via __plugin_author__ in the plugin module
plugin_author = "Christos Miniotis"

# The plugin's author's mail address.
plugin_author_email = "chrismin13@gmail.com"

# The plugin's homepage URL. Can be overwritten within OctoPrint's internal data via __plugin_url__ in the plugin module
plugin_url = "https://github.com/chrismin13/OctoPrint-PSUControl-eWeLink"

# The plugin's license. Can be overwritten within OctoPrint's internal data via __plugin_license__ in the plugin module
plugin_license = "MIT"

# Any additional requirements besides OctoPrint should be listed here
plugin_requires = ["ewelink>=0.2.1"]

### --------------------------------------------------------------------------------------------------------------------
### More advanced options that you usually shouldn't have to touch follow after this.
### --------------------------------------------------------------------------------------------------------------------

from setuptools import setup

def params():
    name = plugin_name
    version = plugin_version
    return dict(
        name=name,
        version=version,
        description=plugin_description,
        author=plugin_author,
        author_email=plugin_author_email,
        url=plugin_url,
        license=plugin_license,
        packages=[plugin_package],
        include_package_data=True,
        package_data={plugin_package: ["templates/*", "static/js/*"]},
        zip_safe=False,
        python_requires=">=3.9,<4",
        install_requires=plugin_requires,
        entry_points={
            "octoprint.plugin": [
                "{} = {}".format(plugin_identifier, plugin_package)
            ]
        },
    )

if __name__ == "__main__":
    setup(**params())
