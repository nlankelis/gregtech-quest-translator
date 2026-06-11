import json
import shutil
from pathlib import Path

from .constants import CHINESE_CHAR_RE, TEXT_EXTENSIONS
from .models import FileResult, RunConfig
from .snbt import translate_snbt_text


class FileProcessor:
    def __init__(self, config: RunConfig, cache: dict[str, str]):
        self.config = config
        self.cache = cache

    def process(self, file_path: Path) -> FileResult:
        suffix = file_path.suffix.lower()

        try:
            if suffix == ".json":
                return self._process_json(file_path)
            if suffix == ".snbt":
                return self._process_snbt(file_path)
            if suffix in TEXT_EXTENSIONS:
                return self._process_text(file_path)
            if suffix == ".toml":
                return self._process_text(file_path)
        except OSError as exc:
            print(f"Failed to process {file_path}: {exc}")

        return FileResult()

    def _process_json(self, file_path: Path) -> FileResult:
        try:
            with file_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError as exc:
            print(f"Skipping invalid JSON {file_path}: {exc}")
            return FileResult()

        translated_data, replaced = self._translate_json_values(data)
        if replaced == 0:
            return FileResult()

        if not self.config.dry_run:
            self._write_file(file_path, json.dumps(translated_data, ensure_ascii=False, indent=2))

        if self.config.verbose:
            print(f"Translated JSON: {file_path}")

        return FileResult(modified=True, strings_replaced=replaced)

    def _translate_json_values(self, value):
        if isinstance(value, dict):
            translated = {}
            replaced = 0
            for key, item in value.items():
                new_value, item_replaced = self._translate_json_values(item)
                translated[key] = new_value
                replaced += item_replaced
            return translated, replaced

        if isinstance(value, list):
            translated = []
            replaced = 0
            for item in value:
                new_value, item_replaced = self._translate_json_values(item)
                translated.append(new_value)
                replaced += item_replaced
            return translated, replaced

        if isinstance(value, str) and value in self.cache:
            return self.cache[value], 1

        return value, 0

    def _process_snbt(self, file_path: Path) -> FileResult:
        with file_path.open("r", encoding="utf-8") as handle:
            original = handle.read()

        translated, replaced = translate_snbt_text(original, self.cache)
        if replaced == 0:
            translated, replaced = self._replace_text_segments(original)

        if replaced == 0:
            return FileResult()

        if not self.config.dry_run:
            self._write_file(file_path, translated)

        if self.config.verbose:
            print(f"Translated SNBT: {file_path}")

        return FileResult(modified=True, strings_replaced=replaced)

    def _process_text(self, file_path: Path) -> FileResult:
        with file_path.open("r", encoding="utf-8") as handle:
            original = handle.read()

        translated, replaced = self._replace_text_segments(original)
        if replaced == 0:
            return FileResult()

        if not self.config.dry_run:
            self._write_file(file_path, translated)

        if self.config.verbose:
            print(f"Translated text: {file_path}")

        return FileResult(modified=True, strings_replaced=replaced)

    def _replace_text_segments(self, text: str) -> tuple[str, int]:
        replaced = 0
        updated = text

        for match in sorted(set(CHINESE_CHAR_RE.findall(text)), key=len, reverse=True):
            if match not in self.cache:
                continue

            updated = updated.replace(match, self.cache[match])
            replaced += 1

            if self.config.verbose:
                print(f"  {match!r} -> {self.cache[match]!r}")

        return updated, replaced

    def _write_file(self, file_path: Path, content: str) -> None:
        if self.config.backup and file_path.exists():
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            shutil.copy2(file_path, backup_path)

        with file_path.open("w", encoding="utf-8", newline="") as handle:
            handle.write(content)