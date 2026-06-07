from __future__ import annotations
import struct
import zlib
from typing import Dict, List, Tuple

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _read_chunk(data: bytes, offset: int) -> Tuple[int, str, bytes, int]:
    length = struct.unpack(">I", data[offset : offset + 4])[0]
    chunk_type = data[offset + 4 : offset + 8].decode("ascii", errors="replace")
    chunk_data = data[offset + 8 : offset + 8 + length]
    crc = struct.unpack(">I", data[offset + 8 + length : offset + 12 + length])[0]
    return length, chunk_type, chunk_data, crc


def _parse_text_chunk(chunk_data: bytes) -> Dict[str, str]:
    if b"\x00" not in chunk_data:
        return {}
    keyword, text = chunk_data.split(b"\x00", 1)
    return {keyword.decode("latin-1", errors="replace"): text.decode("latin-1", errors="replace")}


def _parse_ztxt_chunk(chunk_data: bytes) -> Dict[str, str]:
    if b"\x00" not in chunk_data:
        return {}
    keyword, rest = chunk_data.split(b"\x00", 1)
    if len(rest) < 2:
        return {}
    compression_method = rest[0]
    compressed_text = rest[1:]
    if compression_method != 0:
        return {}
    try:
        text = zlib.decompress(compressed_text).decode("latin-1", errors="replace")
    except zlib.error:
        text = ""
    return {keyword.decode("latin-1", errors="replace"): text}


def _parse_itxt_chunk(chunk_data: bytes) -> Dict[str, str]:
    parts = chunk_data.split(b"\x00", 5)
    if len(parts) < 6:
        return {}
    keyword = parts[0].decode("latin-1", errors="replace")
    compression_flag = parts[1]
    compression_method = parts[2]
    # language_tag = parts[3]
    # translated_keyword = parts[4]
    text = parts[5]
    if compression_flag == b"\x01" and compression_method == 0:
        try:
            text = zlib.decompress(text)
        except zlib.error:
            text = b""
    return {keyword: text.decode("utf-8", errors="replace")}


def parse_png_metadata(data: bytes) -> Dict[str, object]:
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("Not a PNG file")

    offset = len(PNG_SIGNATURE)
    metadata: Dict[str, object] = {}
    while offset + 12 <= len(data):
        length, chunk_type, chunk_data, _ = _read_chunk(data, offset)
        offset += 12 + length

        if chunk_type == "tEXt":
            metadata.update(_parse_text_chunk(chunk_data))
        elif chunk_type == "zTXt":
            metadata.update(_parse_ztxt_chunk(chunk_data))
        elif chunk_type == "iTXt":
            metadata.update(_parse_itxt_chunk(chunk_data))
        elif chunk_type == "eXIf":
            metadata["EXIF"] = chunk_data.hex()
        elif chunk_type == "iCCP":
            metadata["ICC Profile"] = "present"
        elif chunk_type == "gAMA":
            if len(chunk_data) == 4:
                gamma = struct.unpack(">I", chunk_data)[0] / 100000.0
                metadata["Gamma"] = gamma
    return metadata
