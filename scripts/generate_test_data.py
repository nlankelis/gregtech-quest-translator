import json
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_FOLDER = PROJECT_ROOT / "mock_modpack"


def create_mock_data() -> None:
    if TEST_FOLDER.exists():
        shutil.rmtree(TEST_FOLDER)

    TEST_FOLDER.mkdir()
    (TEST_FOLDER / "config").mkdir()
    (TEST_FOLDER / "quests").mkdir()
    (TEST_FOLDER / "kubejs" / "server_scripts").mkdir(parents=True)

    print(f"Creating mock environment in '{TEST_FOLDER}'...")

    quest_data = {
        "title": "测试任务",
        "description": [
            "这是一个测试。",
            "你需要收集 64 个石头。",
        ],
        "rewards": {"item": "minecraft:diamond"},
    }
    with (TEST_FOLDER / "quests" / "chapter1.json").open("w", encoding="utf-8") as handle:
        json.dump(quest_data, handle, indent=2, ensure_ascii=False)
    print(" - Created quests/chapter1.json")

    cfg_content = """
    # Configuration File
    general {
        S:modName="GregTech"
        S:welcomeMessage="欢迎来到服务器!"
        B:isEnabled=true
    }
    """
    with (TEST_FOLDER / "config" / "test.cfg").open("w", encoding="utf-8") as handle:
        handle.write(cfg_content)
    print(" - Created config/test.cfg")

    snbt_content = '{display:{Name:"\\"神剑\\""}, Lore:["\\"这把剑非常锋利\\""]}'
    with (TEST_FOLDER / "kubejs" / "server_scripts" / "items.snbt").open("w", encoding="utf-8") as handle:
        handle.write(snbt_content)
    print(" - Created kubejs/server_scripts/items.snbt")

    print(f"Mock modpack generated: {TEST_FOLDER}")


if __name__ == "__main__":
    create_mock_data()