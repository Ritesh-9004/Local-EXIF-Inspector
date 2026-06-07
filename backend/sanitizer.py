from __future__ import annotations
import html
from pathlib import Path
from typing import Any, Dict

from src.core.image_format import detect_image_format

# Limits
MAX_SIZE = 10 * 1024 * 1024  # 10 MB


class SanitizationError(Exception):
    pass


class UnsupportedImageFormatError(SanitizationError):
    pass


def is_valid_image(data: bytes) -> bool:
    return detect_image_format(data) != "unknown"


def check_file_size(data: bytes) -> None:
    if len(data) > MAX_SIZE:
        raise SanitizationError("File too large")


def check_magic_bytes(data: bytes) -> str:
    image_format = detect_image_format(data)
    supported_formats = {"jpeg", "png", "tiff", "webp"}
    if image_format == "unknown":
        raise UnsupportedImageFormatError(
            "Unsupported image format. Supported formats: JPEG, PNG, TIFF, WEBP."
        )
    if image_format not in supported_formats:
        raise UnsupportedImageFormatError(
            f"{image_format.upper()} files are not supported for extraction. Supported formats: JPEG, PNG, TIFF, WEBP."
        )
    return image_format


def check_filename(filename: str) -> str:
    safe_name = Path(filename).name
    if safe_name == "":
        raise SanitizationError("Invalid filename")
    return safe_name


def _sanitize_value(v: Any) -> Any:
    if isinstance(v, str):
        return html.escape(v)
    if isinstance(v, dict):
        return {k: _sanitize_value(val) for k, val in v.items()}
    if isinstance(v, list):
        return [_sanitize_value(i) for i in v]
    return v


def sanitize_exif_output(result: Dict[str, Any]) -> Dict[str, Any]:
    return _sanitize_value(result)


def sanitize(file, data: bytes) -> tuple[bytes, str]:
    check_file_size(data)
    image_format = check_magic_bytes(data[:12])
    check_filename(getattr(file, "filename", ""))
    return data, image_format
