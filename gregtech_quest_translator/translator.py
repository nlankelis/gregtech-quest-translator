import random
import time

from googletrans import Translator
from tqdm import tqdm

from .models import RunConfig


class TranslationService:
    def __init__(self, config: RunConfig):
        self.config = config
        self._translator = Translator()

    def translate_missing(self, texts: list[str], cache: dict[str, str]) -> int:
        new_texts = [text for text in texts if text not in cache]
        if not new_texts:
            print("All strings found in cache. Skipping API translation.")
            return 0

        if self.config.dry_run:
            print(
                f"Dry run: {len(new_texts)} strings would be translated via API."
            )
            return 0

        print(f"Translating {len(new_texts)} new unique strings...")
        translations = self._batch_translate(new_texts)

        for original, translated in zip(new_texts, translations):
            cache[original] = translated

        return len(new_texts)

    def _batch_translate(self, texts: list[str]) -> list[str]:
        translated: list[str] = []
        batch_size = self.config.batch_size

        for index in tqdm(
            range(0, len(texts), batch_size),
            desc="Translating batches",
        ):
            if index > 0:
                time.sleep(random.uniform(0.5, 1.5))

            batch = texts[index : index + batch_size]
            translated.extend(self._translate_with_retry(batch))

        return translated

    def _translate_with_retry(self, texts: list[str]) -> list[str]:
        for attempt in range(self.config.max_retries):
            try:
                return [
                    self._translator.translate(text, dest="en").text
                    for text in texts
                ]
            except Exception as exc:
                print(f"Translation failed (attempt {attempt + 1}): {exc}")

        print("Giving up on current batch; leaving originals unchanged.")
        return texts