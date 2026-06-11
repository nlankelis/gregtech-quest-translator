import json
from pathlib import Path


def load_cache(cache_file: Path) -> dict[str, str]:
    if not cache_file.is_file():
        return {}

    try:
        with cache_file.open("r", encoding="utf-8") as handle:
            print(f"Loading cache from {cache_file}...")
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error loading cache from {cache_file}: {exc}")
        return {}


def save_cache(cache_file: Path, cache_data: dict[str, str]) -> None:
    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        with cache_file.open("w", encoding="utf-8") as handle:
            json.dump(cache_data, handle, ensure_ascii=False, indent=2)
    except OSError as exc:
        print(f"Error saving cache to {cache_file}: {exc}")