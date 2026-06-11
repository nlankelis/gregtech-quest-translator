import re

CHINESE_CHAR_RE = re.compile(r"[\u4e00-\u9fff]+")
QUOTED_CHINESE_RE = re.compile(r'"([^"]*[\u4e00-\u9fff][^"]*)"')

TEXT_EXTENSIONS = {".cfg", ".zs", ".kubejs", ".txt", ".mcfunction", ".snbt"}
PROCESS_EXTENSIONS = TEXT_EXTENSIONS | {".json", ".toml"}

DEFAULT_BATCH_SIZE = 20
DEFAULT_MAX_RETRIES = 3
DEFAULT_WORKERS = 4