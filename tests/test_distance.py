"""
Unit tests for distance calculations.
"""

import math
from src.fastbox.distance import euclidean_distance


def test_zero_distance():
    assert euclidean_distance((0, 0), (0, 0)) == 0.0
    assert euclidean_distance((50, 50), (50, 50)) == 0.0


def test_standard_3_4_5_triangle():
    assert math.isclose(euclidean_distance((0, 0), (3, 4)), 5.0)


def test_known_coordinates():
    # Between (0,0) and (5,5) = sqrt(25 + 25) = sqrt(50) ~= 7.071
    d = euclidean_distance((0, 0), (5, 5))
    assert math.isclose(d, math.sqrt(50), rel_tol=1e-5)


if __name__ == "__main__":
    test_zero_distance()
    test_standard_3_4_5_triangle()
    test_known_coordinates()
    print("✓ All distance tests passed!")

