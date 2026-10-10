"""Тесты для functions.py."""

from functions import make_counter, sum_all


def test_counter() -> None:
    c = make_counter()
    assert c() == 1
    assert c() == 2
    assert c() == 3


def test_sum_all() -> None:
    assert sum_all() == 0
    assert sum_all(1, 2, 3) == 6
