"""Классы и ООП — учебный модуль 04."""

from dataclasses import dataclass


@dataclass
class Point:
    """Точка на плоскости с координатами x, y."""

    x: float = 0.0
    y: float = 0.0
