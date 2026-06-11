import nbtlib
from nbtlib import parse_nbt

from .constants import CHINESE_CHAR_RE


def translate_snbt_text(snbt_string: str, cache: dict[str, str]) -> tuple[str, int]:
    try:
        nbt_data = parse_nbt(snbt_string)
    except Exception:
        return snbt_string, 0

    replaced = 0

    def recursive_translate(node) -> None:
        nonlocal replaced

        if isinstance(node, nbtlib.Compound):
            for key, value in node.items():
                if isinstance(value, nbtlib.String):
                    original = str(value)
                    if CHINESE_CHAR_RE.search(original) and original in cache:
                        node[key] = nbtlib.String(cache[original])
                        replaced += 1
                else:
                    recursive_translate(value)
        elif isinstance(node, list):
            for index, item in enumerate(node):
                if isinstance(item, nbtlib.String):
                    original = str(item)
                    if CHINESE_CHAR_RE.search(original) and original in cache:
                        node[index] = nbtlib.String(cache[original])
                        replaced += 1
                else:
                    recursive_translate(item)

    recursive_translate(nbt_data)
    return str(nbt_data), replaced