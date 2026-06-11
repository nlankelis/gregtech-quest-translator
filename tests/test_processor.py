import json
from pathlib import Path

from gregtech_quest_translator.models import RunConfig
from gregtech_quest_translator.processor import FileProcessor


def make_config(tmp_path: Path, **overrides) -> RunConfig:
    defaults = {
        "modpack_dir": tmp_path,
        "cache_file": tmp_path / "cache.json",
        "dry_run": False,
        "backup": False,
        "workers": 1,
    }
    defaults.update(overrides)
    return RunConfig(**defaults)


def test_process_json_replaces_cached_strings(tmp_path: Path):
    quest_file = tmp_path / "quests.json"
    quest_file.write_text(
        json.dumps({"title": "测试任务"}, ensure_ascii=False),
        encoding="utf-8",
    )

    cache = {"测试任务": "Test Task"}
    processor = FileProcessor(make_config(tmp_path), cache)
    result = processor.process(quest_file)

    assert result.modified is True
    assert result.strings_replaced == 1

    data = json.loads(quest_file.read_text(encoding="utf-8"))
    assert data["title"] == "Test Task"


def test_process_json_dry_run_does_not_write(tmp_path: Path):
    quest_file = tmp_path / "quests.json"
    original = json.dumps({"title": "测试任务"}, ensure_ascii=False)
    quest_file.write_text(original, encoding="utf-8")

    cache = {"测试任务": "Test Task"}
    processor = FileProcessor(make_config(tmp_path, dry_run=True), cache)
    result = processor.process(quest_file)

    assert result.modified is True
    assert quest_file.read_text(encoding="utf-8") == original


def test_process_text_replaces_longest_matches_first(tmp_path: Path):
    text_file = tmp_path / "message.cfg"
    text_file.write_text('msg="测试任务"', encoding="utf-8")

    cache = {"测试": "Test", "测试任务": "Test Task"}
    processor = FileProcessor(make_config(tmp_path), cache)
    result = processor.process(text_file)

    assert result.modified is True
    assert 'msg="Test Task"' in text_file.read_text(encoding="utf-8")