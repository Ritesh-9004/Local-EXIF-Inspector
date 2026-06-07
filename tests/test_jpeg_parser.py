import os
import struct
import tempfile
import unittest

from src.core.jpeg_parser import ExifNotFoundError, InvalidJpegError, find_exif_segment


class TestJPEGParser(unittest.TestCase):
    def create_temp_jpeg(self, payload: bytes) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(b"\xff\xd8")
            tmp.write(b"\xff\xe1")
            tmp.write(struct.pack(">H", len(payload) + 2))
            tmp.write(payload)
            tmp.write(b"\xff\xd9")
            return tmp.name

    def test_find_exif_segment_returns_tiff_block(self):
        payload = b"Exif\x00\x00" + b"II*\x00\x08\x00\x00\x00"
        path = self.create_temp_jpeg(payload)
        try:
            tiff_block = find_exif_segment(path)
            self.assertEqual(tiff_block, b"II*\x00\x08\x00\x00\x00")
        finally:
            os.unlink(path)

    def test_invalid_jpeg_raises(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(b"NOTJPEG")
            path = tmp.name
        try:
            with self.assertRaises(InvalidJpegError):
                find_exif_segment(path)
        finally:
            os.unlink(path)

    def test_missing_exif_raises(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(b"\xff\xd8")
            tmp.write(b"\xff\xd9")
            path = tmp.name
        try:
            with self.assertRaises(ExifNotFoundError):
                find_exif_segment(path)
        finally:
            os.unlink(path)

    def test_find_exif_segment_after_app0(self):
        app0_payload = b"JFIF\x00\x01\x02"
        exif_payload = b"Exif\x00\x00" + b"II*\x00" + struct.pack("<I", 8) + b"\x00\x00" + b"\x00\x00\x00\x00"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(b"\xff\xd8")
            tmp.write(b"\xff\xe0")
            tmp.write(struct.pack(">H", len(app0_payload) + 2))
            tmp.write(app0_payload)
            tmp.write(b"\xff\xe1")
            tmp.write(struct.pack(">H", len(exif_payload) + 2))
            tmp.write(exif_payload)
            tmp.write(b"\xff\xd9")
            path = tmp.name
        try:
            tiff_block = find_exif_segment(path)
            self.assertEqual(tiff_block, b"II*\x00" + struct.pack("<I", 8) + b"\x00\x00" + b"\x00\x00\x00\x00")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
