import argparse
import sys
from pathlib import Path

from . import __version__
from .app import TranslatorApp
from .constants import DEFAULT_BATCH_SIZE, DEFAULT_MAX_RETRIES, DEFAULT_WORKERS
from .models import RunConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Translate Chinese quest and config files in Minecraft modpacks.",
    )
    parser.add_argument(
        "modpack_dir",
        nargs="?",
        help="Path to the modpack folder",
    )
    parser.add_argument(
        "--cache",
        type=Path,
        default=None,
        help="Path to translation cache JSON (default: translation_cache.json next to the script)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan and report changes without writing files or calling the API",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create .bak copies before overwriting files",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"Number of worker threads (default: {DEFAULT_WORKERS})",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"Translation API batch size (default: {DEFAULT_BATCH_SIZE})",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=DEFAULT_MAX_RETRIES,
        help=f"Translation retry attempts (default: {DEFAULT_MAX_RETRIES})",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print each replacement",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def resolve_modpack_dir(arg_value: str | None) -> Path:
    if arg_value:
        return Path(arg_value)

    user_input = input("Enter modpack path: ").strip().strip('"')
    return Path(user_input)


def resolve_cache_file(cache_arg: Path | None) -> Path:
    if cache_arg is not None:
        return cache_arg

    project_root = Path(__file__).resolve().parent.parent
    return project_root / "translation_cache.json"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    modpack_dir = resolve_modpack_dir(args.modpack_dir)
    if not modpack_dir.exists():
        print(f"Error: path not found: {modpack_dir}", file=sys.stderr)
        return 1

    config = RunConfig(
        modpack_dir=modpack_dir.resolve(),
        cache_file=resolve_cache_file(args.cache).resolve(),
        dry_run=args.dry_run,
        backup=args.backup,
        workers=max(1, args.workers),
        batch_size=max(1, args.batch_size),
        max_retries=max(1, args.max_retries),
        verbose=args.verbose,
    )

    TranslatorApp(config).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())