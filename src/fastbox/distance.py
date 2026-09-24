"""
Distance calculation utilities.
"""

import math
from typing import Sequence


def euclidean_distance(point1: Sequence[float], point2: Sequence[float]) -> float:
    """
    Calculate Euclidean straight-line distance between two 2D points.

    Formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)

    Args:
        point1: (x1, y1) coordinate pair
        point2: (x2, y2) coordinate pair

    Returns:
        float: Straight line Euclidean distance.
    """
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

