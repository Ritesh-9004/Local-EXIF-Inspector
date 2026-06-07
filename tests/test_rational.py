import unittest

from src.decoders.rational import rational_to_float, signed_rational_to_float


class TestRationalDecoder(unittest.TestCase):
    def test_rational_to_float(self):
        self.assertEqual(rational_to_float(1, 2), 0.5)
        self.assertEqual(rational_to_float(10, 4), 2.5)

    def test_rational_zero_denominator(self):
        self.assertEqual(rational_to_float(1, 0), 0.0)

    def test_signed_rational_to_float(self):
        self.assertEqual(signed_rational_to_float(-1, 2), -0.5)


if __name__ == "__main__":
    unittest.main()
