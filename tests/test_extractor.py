import os
import struct
import tempfile
import unittest
import zlib

from src.extractor import EXIFExtractor


def build_png_chunk(chunk_type: bytes, chunk_data: bytes) -> bytes:
    length = struct.pack(">I", len(chunk_data))
    chunk = length + chunk_type + chunk_data
    crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
    return chunk + struct.pack(">I", crc)


class TestExtractor(unittest.TestCase):
    def test_extract_tiff_file(self):
        # Minimal TIFF with an empty IFD0 table
        tiff_bytes = b"II*\x00" + struct.pack("<I", 8) + b"\x00\x00" + b"\x00\x00\x00\x00"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tiff") as tmp:
            tmp.write(tiff_bytes)
            tmp_path = tmp.name

        try:
            extractor = EXIFExtractor(tmp_path)
            metadata = extractor.extract()
            self.assertEqual(metadata["ifd0"], {})
            self.assertEqual(metadata["exif"], {})
            self.assertEqual(metadata["gps"], {})
        finally:
            os.unlink(tmp_path)

    def test_extract_png_text_and_exif(self):
        png_signature = b"\x89PNG\r\n\x1a\n"
        text_chunk = build_png_chunk(b"tEXt", b"Comment\x00Hello PNG")
        exif_chunk_data = b"Exif\x00\x00" + b"II*\x00" + struct.pack("<I", 8) + b"\x00\x00" + b"\x00\x00\x00\x00"
        exif_chunk = build_png_chunk(b"eXIf", exif_chunk_data)
        iend_chunk = build_png_chunk(b"IEND", b"")
        png_data = png_signature + text_chunk + exif_chunk + iend_chunk

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(png_data)
            tmp_path = tmp.name

        try:
            extractor = EXIFExtractor(tmp_path)
            metadata = extractor.extract()
            self.assertIn("png", metadata)
            self.assertEqual(metadata["png"]["Comment"], "Hello PNG")
            self.assertIn("EXIF", metadata["png"])
            self.assertEqual(metadata["png"]["EXIF"]["ifd0"], {})
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
