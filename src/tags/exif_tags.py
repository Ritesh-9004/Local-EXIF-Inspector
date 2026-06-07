EXIF_TAGS = {
    # Exposure
    0x829A: "ExposureTime",
    0x829D: "FNumber",
    0x8822: "ExposureProgram",
    0x8824: "SpectralSensitivity",
    0x8827: "ISOSpeedRatings",
    0x8828: "OECF",
    0x8830: "SensitivityType",
    0x8831: "StandardOutputSensitivity",
    0x8832: "RecommendedExposureIndex",

    # Version
    0x9000: "ExifVersion",
    0x9003: "DateTimeOriginal",
    0x9004: "DateTimeDigitized",
    0x9010: "OffsetTime",
    0x9011: "OffsetTimeOriginal",
    0x9012: "OffsetTimeDigitized",

    # Image config
    0x9101: "ComponentsConfiguration",
    0x9102: "CompressedBitsPerPixel",

    # Shutter / aperture / brightness
    0x9201: "ShutterSpeedValue",
    0x9202: "ApertureValue",
    0x9203: "BrightnessValue",
    0x9204: "ExposureBiasValue",
    0x9205: "MaxApertureValue",
    0x9206: "SubjectDistance",
    0x9207: "MeteringMode",
    0x9208: "LightSource",
    0x9209: "Flash",
    0x920A: "FocalLength",
    0x9214: "SubjectArea",

    # Vendor
    0x927C: "MakerNote",
    0x9286: "UserComment",

    # Subsecond timestamps
    0x9290: "SubSecTime",
    0x9291: "SubSecTimeOriginal",
    0x9292: "SubSecTimeDigitized",

    # Color
    0xA001: "ColorSpace",
    0xA002: "PixelXDimension",
    0xA003: "PixelYDimension",
    0xA004: "RelatedSoundFile",

    # Interoperability
    0xA005: "InteroperabilityIFDPointer",

    # Flash energy / spatial frequency
    0xA20B: "FlashEnergy",
    0xA20C: "SpatialFrequencyResponse",
    0xA20E: "FocalPlaneXResolution",
    0xA20F: "FocalPlaneYResolution",
    0xA210: "FocalPlaneResolutionUnit",
    0xA214: "SubjectLocation",
    0xA215: "ExposureIndex",
    0xA217: "SensingMethod",

    # Scene / source
    0xA300: "FileSource",
    0xA301: "SceneType",
    0xA302: "CFAPattern",

    # Custom rendered / exposure mode
    0xA401: "CustomRendered",
    0xA402: "ExposureMode",
    0xA403: "WhiteBalance",
    0xA404: "DigitalZoomRatio",
    0xA405: "FocalLengthIn35mmFilm",
    0xA406: "SceneCaptureType",
    0xA407: "GainControl",
    0xA408: "Contrast",
    0xA409: "Saturation",
    0xA40A: "Sharpness",
    0xA40B: "DeviceSettingDescription",
    0xA40C: "SubjectDistanceRange",

    # Unique ID
    0xA420: "ImageUniqueID",
    0xA430: "CameraOwnerName",
    0xA431: "BodySerialNumber",
    0xA432: "LensSpecification",
    0xA433: "LensMake",
    0xA434: "LensModel",
    0xA435: "LensSerialNumber",
}

# Human-readable enum mappings
EXPOSURE_PROGRAM_VALUES = {
    0: "Not defined", 1: "Manual", 2: "Normal program",
    3: "Aperture priority", 4: "Shutter priority",
    5: "Creative", 6: "Action", 7: "Portrait", 8: "Landscape",
}

METERING_MODE_VALUES = {
    0: "Unknown", 1: "Average", 2: "Center-weighted average",
    3: "Spot", 4: "Multi-spot", 5: "Pattern", 6: "Partial", 255: "Other",
}

FLASH_VALUES = {
    0x00: "No flash", 0x01: "Flash fired",
    0x05: "Flash fired, no strobe return",
    0x07: "Flash fired, strobe return",
    0x09: "Flash fired, compulsory",
    0x0D: "Flash fired, compulsory, no strobe return",
    0x0F: "Flash fired, compulsory, strobe return",
    0x10: "Flash did not fire, compulsory",
    0x18: "Flash did not fire, auto",
    0x19: "Flash fired, auto",
    0x1D: "Flash fired, auto, no strobe return",
    0x1F: "Flash fired, auto, strobe return",
    0x20: "No flash function",
    0x41: "Flash fired, red-eye reduction",
    0x45: "Flash fired, red-eye reduction, no strobe return",
    0x47: "Flash fired, red-eye reduction, strobe return",
    0x49: "Flash fired, compulsory, red-eye reduction",
    0x4F: "Flash fired, compulsory, red-eye reduction, strobe return",
    0x59: "Flash fired, auto, red-eye reduction",
    0x5D: "Flash fired, auto, no strobe return, red-eye reduction",
    0x5F: "Flash fired, auto, strobe return, red-eye reduction",
}

COLOR_SPACE_VALUES = {
    1: "sRGB", 65535: "Uncalibrated",
}

WHITE_BALANCE_VALUES = {
    0: "Auto", 1: "Manual",
}

EXPOSURE_MODE_VALUES = {
    0: "Auto", 1: "Manual", 2: "Auto bracket",
}

SCENE_CAPTURE_TYPE_VALUES = {
    0: "Standard", 1: "Landscape", 2: "Portrait", 3: "Night scene",
}

SCENE_TYPE_VALUES = {
    1: "Directly photographed",
}

LIGHT_SOURCE_VALUES = {
    0: "Unknown", 1: "Daylight", 2: "Fluorescent", 3: "Tungsten",
    4: "Flash", 9: "Fine weather", 10: "Cloudy", 11: "Shade",
    17: "Standard A", 18: "Standard B", 19: "Standard C",
    20: "D55", 21: "D65", 22: "D75", 23: "D50",
    24: "ISO studio tungsten", 255: "Other",
}

SENSING_METHOD_VALUES = {
    1: "Not defined", 2: "One-chip color area",
    3: "Two-chip color area", 4: "Three-chip color area",
    5: "Color sequential area", 7: "Trilinear",
    8: "Color sequential linear",
}

SUBJECT_DISTANCE_RANGE_VALUES = {
    0: "Unknown", 1: "Macro", 2: "Close view", 3: "Distant view",
}

GAIN_CONTROL_VALUES = {
    0: "None", 1: "Low gain up", 2: "High gain up",
    3: "Low gain down", 4: "High gain down",
}

CONTRAST_SATURATION_SHARPNESS_VALUES = {
    0: "Normal", 1: "Soft/Low", 2: "Hard/High",
}
