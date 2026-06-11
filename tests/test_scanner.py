import json
from pathlib import Path

from gregtech_quest_translator.scanner import collect_chinese_texts, iter_modpack_files


def test_iter_modpack_files_finds_supported_extensions(tmp_path: Path):
    (tmp_path / "quests").mkdir()
    (tmp_path / "config").mkdir()
    (tmp_path / "quests" / "chapter.json").write_text("{}", encoding="utf-8")
    (tmp_path / "config" / "test.cfg").write_text("x=1", encoding="utf-8")
    (tmp_path / "readme.md").write_text("ignore", encoding="utf-8")

    files = iter_modpack_files(tmp_path)
    names = {path.name for path in files}

    assert names == {"chapter.json", "test.cfg"}


def test_collect_chinese_texts_from_json_and_text(tmp_path: Path):
    quest_dir = tmp_path / "quests"
    quest_dir.mkdir()
    quest_file = quest_dir / "chapter.json"
    quest_file.write_text(
        json.dumps({"title": "测试任务", "note": "plain english"}, ensure_ascii=False),
        encoding="utf-8",
    )
    (tmp_path / "config.cfg").write_text(
        'message="欢迎来到服务器!"',
        encoding="utf-8",
    )

    texts = collect_chinese_texts(tmp_path)

    assert "测试任务" in texts
    assert "欢迎来到服务器!" in texts