from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

from src.extractor import EXIFExtractor, EXIFExtractorError
from src.output.formatter import format_data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Pure Python EXIF metadata extractor for JPEG, PNG, and TIFF images."
    )
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument(
        "--format",
        choices=["json", "text", "table"],
        default="json",
        help="Output format",
    )
    parser.add_argument(
        "--only",
        choices=["all", "ifd0", "exif", "gps"],
        default="all",
        help="Only show a subset of metadata",
    )
    parser.add_argument(
        "--outfile",
        help="Write output to a file instead of stdout",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    image_path = Path(args.image)

    if not image_path.exists():
        print(f"Error: file does not exist: {image_path}", file=sys.stderr)
        return 1

    try:
        extractor = EXIFExtractor(str(image_path))
        metadata = extractor.extract()
    except EXIFExtractorError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    output = format_data(metadata, args.format, args.only)
    if args.outfile:
        Path(args.outfile).write_text(output, encoding="utf-8")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
