from __future__ import annotations
import struct
from typing import Any, Dict, List, Tuple
from src.core.value_reader import decode_value

TYPE_SIZES = {
    1: 1,
    2: 1,
    3: 2,
    4: 4,
    5: 8,
    7: 1,
    9: 4,
    10: 8,
}


def parse_ifd(tiff_bytes: bytes, offset: int, byte_order: str) -> Tuple[List[Dict[str, Any]], int]:
    if offset < 0 or offset + 2 > len(tiff_bytes):
        raise ValueError("IFD offset is outside TIFF data")

    entry_count = struct.unpack(byte_order + "H", tiff_bytes[offset : offset + 2])[0]
    cursor = offset + 2
    entries: List[Dict[str, Any]] = []

    for _ in range(entry_count):
        if cursor + 12 > len(tiff_bytes):
            raise ValueError("IFD entry extends beyond TIFF data")

        tag_id, type_id, count, value_or_offset = struct.unpack(
            byte_order + "HHII", tiff_bytes[cursor : cursor + 12]
        )
        cursor += 12

        type_size = TYPE_SIZES.get(type_id)
        if type_size is None:
            raise ValueError(f"Unsupported TIFF data type: {type_id}")

        value_length = type_size * count
        if value_length <= 4:
            raw_value = tiff_bytes[cursor - 4 : cursor - 4 + value_length]
        else:
            if value_or_offset + value_length > len(tiff_bytes):
                raise ValueError("IFD value offset extends beyond TIFF data")
            raw_value = tiff_bytes[value_or_offset : value_or_offset + value_length]

        decoded_value = decode_value(byte_order, type_id, count, raw_value)
        entries.append(
            {
                "tag_id": tag_id,
                "type_id": type_id,
                "count": count,
                "value": decoded_value,
            }
        )

    if cursor + 4 > len(tiff_bytes):
        next_ifd_offset = 0
    else:
        next_ifd_offset = struct.unpack(byte_order + "I", tiff_bytes[cursor : cursor + 4])[0]

    return entries, next_ifd_offset
