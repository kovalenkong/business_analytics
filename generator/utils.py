from enum import Enum
from typing import Any, List

import numpy as np


class P(Enum):
    NORMAL = 'normal'
    RANDOM = 'random'


def choose_random(arr: List[Any], n: int, p: P = P.NORMAL) -> List[Any]:
    if p == P.NORMAL:
        div, rem = n // len(arr), n % len(arr)
        indexes = np.concatenate((np.repeat(arr, div), arr[:rem]))
        np.random.shuffle(indexes)
    else:
        indexes = np.random.choice(arr, n)
    return indexes


def parse_geo_points(points: str):
    return [parse_point(point) for point in points.split(';')]


def parse_point(point: str) -> List[float]:
    return list(map(float, point.split(',')))
