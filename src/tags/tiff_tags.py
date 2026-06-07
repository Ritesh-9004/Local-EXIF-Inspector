TIFF_TAGS = {
    # Image dimensions
    0x0100: "ImageWidth",
    0x0101: "ImageLength",
    0x0102: "BitsPerSample",
    0x0103: "Compression",
    0x0106: "PhotometricInterpretation",
    0x010E: "ImageDescription",
    0x010F: "Make",
    0x0110: "Model",
    0x0111: "StripOffsets",
    0x0112: "Orientation",
    0x0115: "SamplesPerPixel",
    0x0116: "RowsPerStrip",
    0x0117: "StripByteCounts",
    0x011A: "XResolution",
    0x011B: "YResolution",
    0x011C: "PlanarConfiguration",
    0x0128: "ResolutionUnit",
    0x012D: "TransferFunction",
    0x0131: "Software",
    0x0132: "DateTime",
    0x013B: "Artist",
    0x013E: "WhitePoint",
    0x013F: "PrimaryChromaticities",
    0x0201: "JPEGInterchangeFormat",
    0x0202: "JPEGInterchangeFormatLength",
    0x0211: "YCbCrCoefficients",
    0x0212: "YCbCrSubSampling",
    0x0213: "YCbCrPositioning",
    0x0214: "ReferenceBlackWhite",
    0x8298: "Copyright",
    0x8769: "ExifIFDPointer",
    0x8825: "GPSInfoIFDPointer",
}

# Human-readable orientation values
ORIENTATION_VALUES = {
    1: "Horizontal (normal)",
    2: "Mirror horizontal",
    3: "Rotate 180°",
    4: "Mirror vertical",
    5: "Mirror horizontal, rotate 270° CW",
    6: "Rotate 90° CW",
    7: "Mirror horizontal, rotate 90° CW",
    8: "Rotate 270° CW",
}

# Human-readable resolution unit values
RESOLUTION_UNIT_VALUES = {
    1: "No unit",
    2: "inch",
    3: "centimeter",
}
