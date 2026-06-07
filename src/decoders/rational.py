from __future__ import annotations
from typing import Optional


def rational_to_float(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return float(numerator) / float(denominator)


def signed_rational_to_float(numerator: int, denominator: int) -> float:
    return rational_to_float(numerator, denominator)
