from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RunConfig:
    modpack_dir: Path
    cache_file: Path
    dry_run: bool = False
    backup: bool = False
    workers: int = 4
    batch_size: int = 20
    max_retries: int = 3
    verbose: bool = False


@dataclass
class RunStats:
    files_processed: int = 0
    files_modified: int = 0
    strings_replaced: int = 0
    strings_translated: int = 0

    def merge(self, other: "RunStats") -> None:
        self.files_processed += other.files_processed
        self.files_modified += other.files_modified
        self.strings_replaced += other.strings_replaced
        self.strings_translated += other.strings_translated


@dataclass
class FileResult:
    modified: bool = False
    strings_replaced: int = 0