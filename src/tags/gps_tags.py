GPS_TAGS = {
    0x0000: "GPSVersionID",
    0x0001: "GPSLatitudeRef",
    0x0002: "GPSLatitude",
    0x0003: "GPSLongitudeRef",
    0x0004: "GPSLongitude",
    0x0005: "GPSAltitudeRef",
    0x0006: "GPSAltitude",
    0x0007: "GPSTimeStamp",
    0x0008: "GPSSatellites",
    0x0009: "GPSStatus",
    0x000A: "GPSMeasureMode",
    0x000B: "GPSDOP",
    0x000C: "GPSSpeedRef",
    0x000D: "GPSSpeed",
    0x000E: "GPSTrackRef",
    0x000F: "GPSTrack",
    0x0010: "GPSImgDirectionRef",
    0x0011: "GPSImgDirection",
    0x0012: "GPSMapDatum",
    0x0013: "GPSDestLatitudeRef",
    0x0014: "GPSDestLatitude",
    0x0015: "GPSDestLongitudeRef",
    0x0016: "GPSDestLongitude",
    0x0017: "GPSDestBearingRef",
    0x0018: "GPSDestBearing",
    0x0019: "GPSDestDistanceRef",
    0x001A: "GPSDestDistance",
    0x001B: "GPSProcessingMethod",
    0x001C: "GPSAreaInformation",
    0x001D: "GPSDateStamp",
    0x001E: "GPSDifferential",
    0x001F: "GPSHPositioningError",
}

# Human-readable GPS enum values
GPS_ALTITUDE_REF_VALUES = {
    0: "Above sea level",
    1: "Below sea level",
}

GPS_STATUS_VALUES = {
    "A": "Measurement in progress",
    "V": "Measurement interrupted",
}

GPS_MEASURE_MODE_VALUES = {
    "2": "2D measurement",
    "3": "3D measurement",
}

GPS_SPEED_REF_VALUES = {
    "K": "km/h",
    "M": "mph",
    "N": "knots",
}

GPS_DIRECTION_REF_VALUES = {
    "T": "True direction",
    "M": "Magnetic direction",
}
