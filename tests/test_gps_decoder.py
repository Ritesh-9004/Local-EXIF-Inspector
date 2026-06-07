import unittest

from src.decoders.gps_decoder import dms_to_decimal, decode_gps, format_timestamp


class TestGPSDecoder(unittest.TestCase):
    def test_dms_to_decimal(self):
        lat = dms_to_decimal([37, 46, 30], "N")
        lon = dms_to_decimal([122, 25, 9], "W")
        self.assertAlmostEqual(lat, 37.775, places=5)
        self.assertAlmostEqual(lon, -122.41916666, places=5)

    def test_format_timestamp(self):
        self.assertEqual(format_timestamp([14, 32, 0]), "14:32:00 UTC")

    def test_decode_gps(self):
        gps_values = {
            "GPSLatitudeRef": "N",
            "GPSLatitude": [37, 46, 30],
            "GPSLongitudeRef": "W",
            "GPSLongitude": [122, 25, 9],
            "GPSAltitudeRef": 0,
            "GPSAltitude": 52.3,
            "GPSTimeStamp": [14, 32, 0],
            "GPSDateStamp": "2024:06:01",
        }
        decoded = decode_gps(gps_values)
        self.assertAlmostEqual(decoded["latitude"], 37.775, places=5)
        self.assertAlmostEqual(decoded["longitude"], -122.41916666, places=5)
        self.assertEqual(decoded["altitude"], 52.3)
        self.assertEqual(decoded["timestamp"], "2024:06:01 14:32:00 UTC")


if __name__ == "__main__":
    unittest.main()
