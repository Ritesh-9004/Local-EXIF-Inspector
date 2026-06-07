from __future__ import annotations
import struct
from typing import Tuple

class TiffHeaderError(Exception):
    pass


def parse_tiff_header(tiff_bytes: bytes) -> Tuple[str, int]:
    if len(tiff_bytes) < 8:
        raise TiffHeaderError("TIFF header is too short")

    if tiff_bytes[0:2] == b"II":
        byte_order = "<"
    elif tiff_bytes[0:2] == b"MM":
        byte_order = ">"
    else:
        raise TiffHeaderError("Invalid TIFF byte order")

    magic = struct.unpack(byte_order + "H", tiff_bytes[2:4])[0]
    if magic != 42:
        raise TiffHeaderError("Invalid TIFF magic number")

    ifd0_offset = struct.unpack(byte_order + "I", tiff_bytes[4:8])[0]
    return byte_order, ifd0_offset
