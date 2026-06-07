from __future__ import annotations


class InvalidWebPError(Exception):
    pass


class ExifNotFoundInWebPError(Exception):
    pass


def find_webp_exif(data: bytes) -> bytes:
    """
    Parse a WEBP file's RIFF container and return the raw TIFF block
    from the EXIF chunk if present.

    WEBP structure:
        [RIFF] [file size: 4B LE] [WEBP] [chunks...]

    Each chunk:
        [chunk id: 4B] [chunk size: 4B LE] [chunk data: N bytes] [padding if odd size]
    """
    if len(data) < 12:
        raise InvalidWebPError("File too small to be a valid WEBP")

    if data[:4] != b"RIFF":
        raise InvalidWebPError("Not a RIFF file")

    if data[8:12] != b"WEBP":
        raise InvalidWebPError("Not a WEBP file")

    offset = 12  # skip RIFF header (4) + file size (4) + WEBP (4)

    while offset + 8 <= len(data):
        chunk_id = data[offset : offset + 4]
        chunk_size = int.from_bytes(data[offset + 4 : offset + 8], "little")
        chunk_data_start = offset + 8
        chunk_data_end = chunk_data_start + chunk_size

        if chunk_data_end > len(data):
            # clamp — don't hard fail on last chunk
            chunk_data_end = len(data)

        if chunk_id == b"EXIF":
            exif_data = data[chunk_data_start:chunk_data_end]

            # Strip "Exif\x00\x00" header if present
            if exif_data.startswith(b"Exif\x00\x00"):
                return exif_data[6:]

            # Raw TIFF block
            return exif_data

        # Chunks are word-aligned — skip padding byte if chunk size is odd
        offset += 8 + chunk_size + (chunk_size % 2)

    raise ExifNotFoundInWebPError("No EXIF chunk found in WEBP file")
