from __future__ import annotations
import struct
from typing import Any
from src.decoders import rational as rational_decoder

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


def decode_value(byte_order: str, type_id: int, count: int, raw_bytes: bytes) -> Any:
    total_size = TYPE_SIZES.get(type_id, 0) * count
    if total_size and len(raw_bytes) < total_size:
        raise ValueError("Value bytes are shorter than expected")

    if type_id == 1:
        if count == 1:
            return raw_bytes[0]
        return list(raw_bytes[:count])

    if type_id == 2:
        value = raw_bytes[:count].rstrip(b"\x00")
        return value.decode("latin-1", errors="replace")

    if type_id == 3:
        if count == 1:
            return struct.unpack(byte_order + "H", raw_bytes[:2])[0]
        return list(struct.unpack(byte_order + f"{count}H", raw_bytes[: total_size]))

    if type_id == 4:
        if count == 1:
            return struct.unpack(byte_order + "I", raw_bytes[:4])[0]
        return list(struct.unpack(byte_order + f"{count}I", raw_bytes[: total_size]))

    if type_id == 5:
        values = []
        for index in range(count):
            start = index * 8
            numerator, denominator = struct.unpack(
                byte_order + "II", raw_bytes[start : start + 8]
            )
            values.append(rational_decoder.rational_to_float(numerator, denominator))
        return values[0] if count == 1 else values

    if type_id == 7:  # UNDEFINED
        chunk = raw_bytes[:count]
        stripped = chunk.rstrip(b"\x00")
        try:
            decoded = stripped.decode("ascii")
        except UnicodeDecodeError:
            return chunk.hex()

        if all(32 <= ord(char) < 127 for char in decoded):
            return decoded
        return chunk.hex()

    if type_id == 9:
        if count == 1:
            return struct.unpack(byte_order + "i", raw_bytes[:4])[0]
        return list(struct.unpack(byte_order + f"{count}i", raw_bytes[: total_size]))

    if type_id == 10:
        values = []
        for index in range(count):
            start = index * 8
            numerator, denominator = struct.unpack(
                byte_order + "ii", raw_bytes[start : start + 8]
            )
            values.append(rational_decoder.rational_to_float(numerator, denominator))
        return values[0] if count == 1 else values

    raise ValueError(f"Unsupported TIFF data type: {type_id}")
