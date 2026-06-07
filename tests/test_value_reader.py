import unittest

from src.core.value_reader import decode_value


class TestValueReader(unittest.TestCase):
    def test_undefined_ascii_printable(self):
        raw_bytes = b"TEST\x00"
        value = decode_value("<", 7, 5, raw_bytes)
        self.assertEqual(value, "TEST")

    def test_undefined_non_printable_returns_hex(self):
        raw_bytes = b"\x01\x02\x03\x00"
        value = decode_value("<", 7, 4, raw_bytes)
        self.assertEqual(value, "01020300")


if __name__ == "__main__":
    unittest.main()
