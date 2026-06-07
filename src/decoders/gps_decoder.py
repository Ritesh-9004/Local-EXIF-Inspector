from __future__ import annotations
from typing import Dict, List, Optional, Sequence, Union

Number = Union[int, float]


def dms_to_decimal(dms: Sequence[Number], ref: Optional[str]) -> Optional[float]:
    if not dms or len(dms) != 3 or ref is None:
        return None
    degrees, minutes, seconds = dms
    try:
        decimal = float(degrees) + float(minutes) / 60.0 + float(seconds) / 3600.0
    except (TypeError, ValueError):
        return None

    if ref.upper() in {"S", "W"}:
        decimal = -decimal
    return decimal


def format_timestamp(timestamp: Sequence[Number]) -> Optional[str]:
    if not timestamp or len(timestamp) != 3:
        return None
    hours, minutes, seconds = timestamp
    try:
        return "{:02d}:{:02d}:{:02d} UTC".format(
            int(hours), int(minutes), int(round(float(seconds)))
        )
    except (TypeError, ValueError):
        return None


def decode_gps(gps_values: Dict[str, object]) -> Dict[str, object]:
    latitude = dms_to_decimal(
        gps_values.get("GPSLatitude", []), gps_values.get("GPSLatitudeRef")
    )
    longitude = dms_to_decimal(
        gps_values.get("GPSLongitude", []), gps_values.get("GPSLongitudeRef")
    )

    altitude = None
    alt_ref = gps_values.get("GPSAltitudeRef")
    raw_alt = gps_values.get("GPSAltitude")
    if raw_alt is not None:
        try:
            altitude = float(raw_alt)
            if int(alt_ref or 0) == 1:
                altitude = -altitude
        except (TypeError, ValueError):
            altitude = None

    timestamp = format_timestamp(gps_values.get("GPSTimeStamp", []))
    datestamp = gps_values.get("GPSDateStamp")
    if timestamp and datestamp:
        timestamp = f"{datestamp} {timestamp}"

    result: Dict[str, object] = {}
    if latitude is not None:
        result["latitude"] = latitude
    if longitude is not None:
        result["longitude"] = longitude
    if altitude is not None:
        result["altitude"] = altitude
    if timestamp is not None:
        result["timestamp"] = timestamp

    return result
