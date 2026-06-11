from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

from .cache import load_cache, save_cache
from .models import RunConfig, RunStats
from .processor import FileProcessor
from .scanner import collect_chinese_texts, iter_modpack_files
from .translator import TranslationService


class TranslatorApp:
    def __init__(self, config: RunConfig):
        self.config = config
        self.cache = load_cache(config.cache_file)
        self.translation_service = TranslationService(config)

    def run(self) -> RunStats:
        stats = RunStats()

        print("Scanning for Chinese text...")
        chinese_texts = collect_chinese_texts(self.config.modpack_dir)
        stats.strings_translated = self.translation_service.translate_missing(
            chinese_texts,
            self.cache,
        )

        if stats.strings_translated and not self.config.dry_run:
            save_cache(self.config.cache_file, self.cache)

        files = iter_modpack_files(self.config.modpack_dir)
        stats.files_processed = len(files)

        if not files:
            print("No supported files found.")
            return stats

        print(f"Processing {len(files)} files with {self.config.workers} workers...")
        processor = FileProcessor(self.config, self.cache)

        with ThreadPoolExecutor(max_workers=self.config.workers) as pool:
            futures = {pool.submit(processor.process, path): path for path in files}

            for future in tqdm(as_completed(futures), total=len(futures), desc="Rewriting files"):
                result = future.result()
                if result.modified:
                    stats.files_modified += 1
                stats.strings_replaced += result.strings_replaced

        self._print_summary(stats)
        return stats

    def _print_summary(self, stats: RunStats) -> None:
        print("\n===== SUMMARY =====")
        print(f"Files processed: {stats.files_processed}")
        print(f"Files modified: {stats.files_modified}")
        print(f"New API translations: {stats.strings_translated}")
        print(f"Strings replaced: {stats.strings_replaced}")
        if self.config.dry_run:
            print("Dry run: no files were written.")
        print("===================")