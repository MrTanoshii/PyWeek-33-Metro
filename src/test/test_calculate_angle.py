import unittest

from src.lib import calculate_angle


class TestSum(unittest.TestCase):

    def test_calculate_angle(self):
        self.assertAlmostEqual(calculate_angle(0, 0, 0, 0), 0.00000, 5, "Should be 0.00000")
        self.assertAlmostEqual(calculate_angle(1, 2, 3, 4), 45.00000, 5, "Should be 45.00000")
        self.assertAlmostEqual(calculate_angle(-1, -2, -3, -4), 45.00000, 5, "Should be 45.00000")


if __name__ == '__main__':
    unittest.main()
