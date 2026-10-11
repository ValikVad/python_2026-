"""Тесты для classes.py."""

from classes import Point


def test_point_defaults() -> None:
    p = Point()
    assert (p.x, p.y) == (0.0, 0.0)


def test_point_field() -> None:
    p = Point(1.0, 2.0)
    assert p.x == 1.0
    assert p.y == 2.0
