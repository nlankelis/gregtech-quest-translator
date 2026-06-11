import json
from pathlib import Path

from .constants import CHINESE_CHAR_RE, PROCESS_EXTENSIONS, QUOTED_CHINESE_RE


def is_processable_file(file_path: Path) -> bool:
    return file_path.suffix.lower() in PROCESS_EXTENSIONS


def iter_modpack_files(modpack_dir: Path) -> list[Path]:
    files = [
        path
        for path in modpack_dir.rglob("*")
        if path.is_file() and is_processable_file(path)
    ]
    return sorted(files)


def _extract_chinese_from_json(obj, found: set[str]) -> None:
    if isinstance(obj, dict):
        for value in obj.values():
            _extract_chinese_from_json(value, found)
    elif isinstance(obj, list):
        for item in obj:
            _extract_chinese_from_json(item, found)
    elif isinstance(obj, str) and CHINESE_CHAR_RE.search(obj):
        found.add(obj)


def _extract_chinese_from_text(text: str, found: set[str]) -> None:
    for match in QUOTED_CHINESE_RE.findall(text):
        found.add(match)

    for match in CHINESE_CHAR_RE.findall(text):
        found.add(match)


def collect_chinese_texts(modpack_dir: Path) -> list[str]:
    found: set[str] = set()

    for file_path in iter_modpack_files(modpack_dir):
        try:
            if file_path.suffix.lower() == ".json":
                with file_path.open("r", encoding="utf-8") as handle:
                    data = json.load(handle)
                _extract_chinese_from_json(data, found)
            else:
                with file_path.open("r", encoding="utf-8") as handle:
                    _extract_chinese_from_text(handle.read(), found)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Failed to scan {file_path}: {exc}")

    return sorted(found)