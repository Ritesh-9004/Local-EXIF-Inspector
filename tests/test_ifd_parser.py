import struct
import unittest

from src.core.ifd_parser import parse_ifd


class TestIFDParser(unittest.TestCase):
    def test_parse_ifd_with_inline_short(self):
        tiff_bytes = b"II" + struct.pack("<H", 42) + struct.pack("<I", 8)
        entries = struct.pack("<H", 1)
        entry = struct.pack("<HHII", 0x0112, 3, 1, 0x00000001)
        entries += entry + struct.pack("<I", 0)
        data = tiff_bytes + entries

        parsed_entries, next_offset = parse_ifd(data, 8, "<")
        self.assertEqual(next_offset, 0)
        self.assertEqual(parsed_entries[0]["tag_id"], 0x0112)
        self.assertEqual(parsed_entries[0]["value"], 1)

    def test_parse_ifd_with_offset_string(self):
        tiff_bytes = b"II" + struct.pack("<H", 42) + struct.pack("<I", 8)
        entries = struct.pack("<H", 1)
        ascii_offset = 8 + 2 + 12 + 4
        entry = struct.pack("<HHII", 0x010F, 2, 6, ascii_offset)
        entries += entry + struct.pack("<I", 0)
        entries += b"Canon\x00"
        data = tiff_bytes + entries

        parsed_entries, next_offset = parse_ifd(data, 8, "<")
        self.assertEqual(parsed_entries[0]["tag_id"], 0x010F)
        self.assertEqual(parsed_entries[0]["value"], "Canon")
        self.assertEqual(next_offset, 0)


if __name__ == "__main__":
    unittest.main()
