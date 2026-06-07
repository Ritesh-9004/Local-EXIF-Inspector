from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional

from src.core.image_format import detect_image_format
from src.core.jpeg_parser import ExifNotFoundError, InvalidJpegError, find_exif_segment
from src.core.png_parser import parse_png_metadata
from src.core.webp_parser import ExifNotFoundInWebPError, InvalidWebPError, find_webp_exif
from src.core.ifd_parser import parse_ifd
from src.core.tiff_parser import parse_tiff_header
from src.tags.exif_tags import (
    EXIF_TAGS,
    COLOR_SPACE_VALUES,
    CONTRAST_SATURATION_SHARPNESS_VALUES,
    EXPOSURE_MODE_VALUES,
    EXPOSURE_PROGRAM_VALUES,
    FLASH_VALUES,
    GAIN_CONTROL_VALUES,
    LIGHT_SOURCE_VALUES,
    METERING_MODE_VALUES,
    SCENE_CAPTURE_TYPE_VALUES,
    SCENE_TYPE_VALUES,
    SENSING_METHOD_VALUES,
    SUBJECT_DISTANCE_RANGE_VALUES,
    WHITE_BALANCE_VALUES,
)
from src.tags.gps_tags import GPS_TAGS, GPS_ALTITUDE_REF_VALUES, GPS_SPEED_REF_VALUES
from src.tags.tiff_tags import TIFF_TAGS, ORIENTATION_VALUES, RESOLUTION_UNIT_VALUES
from src.decoders.gps_decoder import decode_gps


class EXIFExtractorError(Exception):
    pass


_EXIF_ENUM_MAP = {
    "ExposureProgram":      EXPOSURE_PROGRAM_VALUES,
    "MeteringMode":         METERING_MODE_VALUES,
    "Flash":                FLASH_VALUES,
    "ColorSpace":           COLOR_SPACE_VALUES,
    "WhiteBalance":         WHITE_BALANCE_VALUES,
    "ExposureMode":         EXPOSURE_MODE_VALUES,
    "SceneCaptureType":     SCENE_CAPTURE_TYPE_VALUES,
    "SceneType":            SCENE_TYPE_VALUES,
    "LightSource":          LIGHT_SOURCE_VALUES,
    "SensingMethod":        SENSING_METHOD_VALUES,
    "SubjectDistanceRange": SUBJECT_DISTANCE_RANGE_VALUES,
    "GainControl":          GAIN_CONTROL_VALUES,
    "Contrast":             CONTRAST_SATURATION_SHARPNESS_VALUES,
    "Saturation":           CONTRAST_SATURATION_SHARPNESS_VALUES,
    "Sharpness":            CONTRAST_SATURATION_SHARPNESS_VALUES,
}

_TIFF_ENUM_MAP = {
    "Orientation":    ORIENTATION_VALUES,
    "ResolutionUnit": RESOLUTION_UNIT_VALUES,
}

_GPS_ENUM_MAP = {
    "GPSAltitudeRef": GPS_ALTITUDE_REF_VALUES,
    "GPSSpeedRef":    GPS_SPEED_REF_VALUES,
}


def _resolve_enums(data: dict, enum_map: dict) -> dict:
    for field, lookup in enum_map.items():
        if field in data and data[field] in lookup:
            data[field] = lookup[data[field]]
    return data


def _format_exposure_time(value) -> str:
    if isinstance(value, float) and 0 < value < 1:
        return f"1/{round(1 / value)}s"
    if isinstance(value, (int, float)):
        return f"{value}s"
    return str(value)


def _format_fnumber(value) -> str:
    if isinstance(value, (int, float)):
        return f"f/{value:.1f}"
    return str(value)


def _format_focal_length(value) -> str:
    if isinstance(value, (int, float)):
        return f"{value:.1f}mm"
    return str(value)


@dataclass
class EXIFExtractor:
    path: str

    def _parse_tiff_bytes(self, tiff_bytes: bytes) -> Dict[str, object]:
        byte_order, ifd0_offset = parse_tiff_header(tiff_bytes)
        ifd0_entries, _ = parse_ifd(tiff_bytes, ifd0_offset, byte_order)

        result = {"ifd0": {}, "exif": {}, "gps": {}}

        exif_ifd_offset: Optional[int] = None
        gps_ifd_offset: Optional[int] = None

        for entry in ifd0_entries:
            tag_id = entry["tag_id"]
            value = entry["value"]
            name = TIFF_TAGS.get(tag_id, f"Tag_{tag_id:04X}")
            result["ifd0"][name] = value

            if tag_id == 0x8769:
                exif_ifd_offset = int(value)
            elif tag_id == 0x8825:
                gps_ifd_offset = int(value)

        result["ifd0"].pop("ExifIFDPointer", None)
        result["ifd0"].pop("GPSInfoIFDPointer", None)
        result["ifd0"] = _resolve_enums(result["ifd0"], _TIFF_ENUM_MAP)

        if exif_ifd_offset is not None:
            exif_entries, _ = parse_ifd(tiff_bytes, exif_ifd_offset, byte_order)
            for entry in exif_entries:
                name = EXIF_TAGS.get(entry["tag_id"], f"Tag_{entry['tag_id']:04X}")
                result["exif"][name] = entry["value"]

            result["exif"] = _resolve_enums(result["exif"], _EXIF_ENUM_MAP)

            if "ExposureTime" in result["exif"]:
                result["exif"]["ExposureTime"] = _format_exposure_time(result["exif"]["ExposureTime"])
            if "FNumber" in result["exif"]:
                result["exif"]["FNumber"] = _format_fnumber(result["exif"]["FNumber"])
            if "FocalLength" in result["exif"]:
                result["exif"]["FocalLength"] = _format_focal_length(result["exif"]["FocalLength"])
            if "FocalLengthIn35mmFilm" in result["exif"]:
                result["exif"]["FocalLengthIn35mmFilm"] = f"{result['exif']['FocalLengthIn35mmFilm']}mm"

        if gps_ifd_offset is not None:
            gps_entries, _ = parse_ifd(tiff_bytes, gps_ifd_offset, byte_order)
            gps_values = {}
            for entry in gps_entries:
                name = GPS_TAGS.get(entry["tag_id"], f"Tag_{entry['tag_id']:04X}")
                gps_values[name] = entry["value"]
            result["gps"] = decode_gps(gps_values)
            result["gps"] = _resolve_enums(result["gps"], _GPS_ENUM_MAP)

        return result

    def extract(self) -> Dict[str, object]:
        with open(self.path, "rb") as file:
            data = file.read()

        image_format = detect_image_format(data)

        if image_format == "jpeg":
            try:
                tiff_bytes = find_exif_segment(self.path)
            except (ExifNotFoundError, InvalidJpegError) as exc:
                raise EXIFExtractorError(str(exc))
            return self._parse_tiff_bytes(tiff_bytes)

        if image_format == "tiff":
            try:
                return self._parse_tiff_bytes(data)
            except Exception as exc:
                raise EXIFExtractorError(str(exc))

        if image_format == "png":
            try:
                png_metadata = parse_png_metadata(data)
                if "EXIF" in png_metadata:
                    exif_payload = bytes.fromhex(png_metadata["EXIF"])
                    if exif_payload.startswith(b"Exif\x00\x00"):
                        exif_payload = exif_payload[6:]
                    png_metadata["EXIF"] = self._parse_tiff_bytes(exif_payload)
                return {"png": png_metadata}
            except Exception as exc:
                raise EXIFExtractorError(str(exc))

        if image_format == "webp":
            try:
                tiff_bytes = find_webp_exif(data)
                return self._parse_tiff_bytes(tiff_bytes)
            except ExifNotFoundInWebPError:
                raise EXIFExtractorError("No EXIF data found in this WEBP file.")
            except InvalidWebPError as exc:
                raise EXIFExtractorError(str(exc))
            except Exception as exc:
                raise EXIFExtractorError(str(exc))

        raise EXIFExtractorError(
            "Unsupported image format. Supported formats: JPEG, PNG, TIFF, WEBP."
        )
