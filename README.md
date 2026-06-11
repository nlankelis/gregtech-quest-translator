# GregTech Quest Translator

Translates Chinese quest and config text in Minecraft modpack folders to English.

```bash
python -m pip install -e .
gtqt-translate "C:\path\to\modpack"
```

On Windows, prefer `python -m pip` over `pip` — the Python installer does not always add `pip` to PATH.

Python 3.13+ removes the stdlib `cgi` module. This project pulls in `legacy-cgi` on those versions because `googletrans` depends on an older `httpx` that still imports it.

See `pyproject.toml` for dependencies and `tests/` for usage examples.