# Translation Guide

This plugin supports Internationalization (i18n) to make it accessible to users worldwide. We use [Babel](http://babel.pocoo.org/) for extracting and managing translations from Python, JavaScript, and Jinja2 templates.

## Prerequisites

To work with translations, you need the development dependencies installed:

```bash
pip install -e .[develop]
```

We also recommend using [Task](https://taskfile.dev/) (known as `go-task`) to run the automated commands defined in `Taskfile.yml`. If you don't have `task`, you can run the `pybabel` commands manually (see `Taskfile.yml` for exact commands).

## Directory Structure

*   `babel.cfg`: Configuration file telling Babel how to extract strings from source files.
*   `Taskfile.yml`: Definitions for translation commands.
*   `translations/`: Source directory for translation files.
    *   `messages.pot`: The template file containing all extracted strings (DO NOT edit this manually).
    *   `<locale>/LC_MESSAGES/messages.po`: The specific translation file for a language (e.g., `el` for Greek).
*   `octoprint_psucontrol_ewelink/translations/`: The destination for **compiled** translation files (`.mo`) used by the plugin at runtime.

## Workflow for Developers

### 1. Marking Strings for Translation

When adding new user-facing text, you must mark it so Babel can find it.

*   **Python (`.py`)**:
    ```python
    from flask_babel import gettext
    
    # NOTE: Error message when API fails
    raise Exception(gettext("Connection failed"))
    ```

*   **JavaScript (`.js`)**:
    ```javascript
    // NOTE: Title of error notification
    var title = gettext("Connection Failed");
    ```

*   **Jinja2 Templates (`.jinja2`)**:
    ```jinja2
    {# NOTE: Label for the email input field #}
    <label>{{ _('Email') }}</label>
    ```

> **Context Comments**: Always add a comment starting with `NOTE:` immediately before the translation call. This helps translators understand the context (e.g., is "Online" a status label or a button?).

### 2. Extracting Strings

After adding or modifying marked strings, update the template (`.pot`) file:

```bash
task babel-extract
```

This commands scans the codebase and updates `translations/messages.pot`.

### 3. Updating Translation Files

Propagate the changes from `messages.pot` to all existing language files (`.po`):

```bash
task babel-update
```

### 4. Compiling and Bundling

To test translations locally or prepare for release, compile them into machine-readable `.mo` files and copy them to the plugin package:

```bash
task babel-compile
task babel-bundle
```

## Adding a New Language

To add support for a new language (e.g., Spanish `es`):

1.  **Initialize the language**:
    ```bash
    task babel-new -- es
    ```
    This creates `translations/es/LC_MESSAGES/messages.po`.

2.  **Add to Taskfile**:
    Open `Taskfile.yml` and add `"es"` to the `LOCALES` list:
    ```yaml
    env:
      LOCALES: ["el", "es"]
    ```

3.  **Translate**: Open the new `.po` file and start translating!

## Workflow for Translators

1.  Open the `.po` file for your language (e.g., `translations/el/LC_MESSAGES/messages.po`).
2.  Find lines with `msgid` (the English source) and add the translation to `msgstr`.
3.  **Context**: Look for lines starting with `#. NOTE:` above the `msgid`. These provide important context.
4.  **Fuzzy**: If a translation is marked with `#, fuzzy`, it means the source string changed slightly. Review the translation, update it, and remove the `#, fuzzy` line.

### Tools
You can edit `.po` files with a text editor, or use specialized tools like:
*   [Poedit](https://poedit.net/)
*   [Evolve](https://github.com/Start9Labs/evolve-ui)
*   VS Code extensions (e.g., "gettext")

## Updating Translations

If the source code changes, you need to sync your translation file:

1.  Run `task babel-refresh` (which runs extract + update).
2.  Check for new strings (empty `msgstr`) or fuzzy matches.
3.  Fill in the missing translations.
4.  Compile and verify in OctoPrint.


## 📦 Release Preparation

> [!CAUTION]
> **TRANSLATIONS WILL BREAK IF YOU SKIP THIS!**
> GitHub releases pull the Source Code zip directly. If you do not commit the **compiled** `messages.mo` files, users will see English (or broken placeholders).

Before creating a release (or pushing a release tag):

1.  **Compile & Bundle**:
    Run this to generate the `.mo` files and copy them to the package folder:
    ```bash
    task babel-compile babel-bundle
    ```

2.  **COMMIT EVERYTHING**:
    The compiled files are binaries inside `octoprint_psucontrol_ewelink/translations/`. You **MUST** force `git` to see them if they aren't tracked yet, or just use `git add .`:
    ```bash
    git add .
    git commit -m "chore: Update translations for release"
    ```

3.  **Push**:
    ```bash
    git push origin main
    ```
    (Then proceed with bumping version/changelog if not already done).

---

**More docs:** [README](../README.md) · [Troubleshooting](TROUBLESHOOTING.md) · [Security](SECURITY.md) · [API Reference](API.md) · [Architecture](ARCHITECTURE.md) · [Development](DEVELOPMENT.md) · [Changelog](CHANGELOG.md)
