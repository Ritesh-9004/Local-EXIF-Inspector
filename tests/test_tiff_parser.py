import struct
import unittest

from src.core.tiff_parser import TiffHeaderError, parse_tiff_header


class TestTiffParser(unittest.TestCase):
    def test_parse_little_endian_header(self):
        header = b"II" + struct.pack("<H", 42) + struct.pack("<I", 8)
        byte_order, offset = parse_tiff_header(header)
        self.assertEqual(byte_order, "<")
        self.assertEqual(offset, 8)

    def test_parse_big_endian_header(self):
        header = b"MM" + struct.pack(">H", 42) + struct.pack(">I", 8)
        byte_order, offset = parse_tiff_header(header)
        self.assertEqual(byte_order, ">")
        self.assertEqual(offset, 8)

    def test_invalid_magic_raises(self):
        header = b"II" + struct.pack("<H", 43) + struct.pack("<I", 8)
        with self.assertRaises(TiffHeaderError):
            parse_tiff_header(header)


if __name__ == "__main__":
    unittest.main()
