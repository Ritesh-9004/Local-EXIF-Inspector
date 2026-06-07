from __future__ import annotations
import struct
from typing import Tuple

class InvalidJpegError(Exception):
    pass

class ExifNotFoundError(Exception):
    pass


def find_exif_segment(path: str) -> bytes:
    """Read a JPEG file and return the raw TIFF block for the first valid EXIF APP1 segment."""
    with open(path, "rb") as file:
        data = file.read()

    if len(data) < 4 or data[0:2] != b"\xff\xd8":
        raise InvalidJpegError("File is not a valid JPEG image")

    offset = 2
    while offset + 4 <= len(data):
        if data[offset] != 0xFF:
            offset += 1
            continue

        marker = data[offset : offset + 2]
        offset += 2

        if marker == b"\xff\xd9":
            break

        if marker == b"\xff\x01":
            continue

        if offset + 2 > len(data):
            break

        segment_length = struct.unpack(">H", data[offset : offset + 2])[0]
        if segment_length < 2:
            raise InvalidJpegError("Invalid JPEG segment length")

        payload_start = offset + 2
        payload_end = payload_start + segment_length - 2

        if payload_end > len(data):
            if marker == b"\xff\xe1":
                raise InvalidJpegError("JPEG file is truncated or malformed")
            payload_end = len(data)

        if marker == b"\xff\xe1":
            payload = data[payload_start:payload_end]
            if payload.startswith(b"Exif\x00\x00"):
                return payload[6:]

        offset = payload_end

    raise ExifNotFoundError("No EXIF APP1 segment found in JPEG file")
