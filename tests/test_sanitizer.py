import unittest

from backend.sanitizer import (
    UnsupportedImageFormatError,
    detect_image_format,
    sanitize,
)


class DummyFile:
    def __init__(self, filename: str):
        self.filename = filename


class TestSanitizer(unittest.TestCase):
    def test_detect_jpeg(self):
        self.assertEqual(detect_image_format(b"\xff\xd8\xff\x00\x10"), "jpeg")

    def test_detect_png(self):
        self.assertEqual(detect_image_format(b"\x89PNG\r\n\x1a\n" + b"rest"), "png")

    def test_detect_tiff(self):
        self.assertEqual(detect_image_format(b"II*\x00" + b"rest"), "tiff")

    def test_sanitize_accepts_png(self):
        file = DummyFile("test.png")
        data, image_format = sanitize(file, b"\x89PNG\r\n\x1a\nhello")
        self.assertEqual(image_format, "png")
        self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_sanitize_accepts_jpeg(self):
        file = DummyFile("test.jpg")
        data, image_format = sanitize(file, b"\xff\xd8\xff\x00\x10")
        self.assertEqual(image_format, "jpeg")
        self.assertEqual(data[:3], b"\xff\xd8\xff")

    def test_sanitize_accepts_webp(self):
        file = DummyFile("test.webp")
        data, image_format = sanitize(file, b"RIFF" + b"\x00\x00\x00\x00" + b"WEBP" + b"data")
        self.assertEqual(image_format, "webp")
        self.assertTrue(data.startswith(b"RIFF"))


if __name__ == "__main__":
    unittest.main()
