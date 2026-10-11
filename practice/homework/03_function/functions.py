"""Функции и области видимости — учебный модуль 03.

Эталонные решения: функции реализованы. Студент может сверить свой код.
"""

from collections.abc import Callable


def make_counter() -> Callable[[], int]:
    """Вернуть замыкание-счётчик: каждый вызов увеличивает число на 1."""

    n = 0

    def counter() -> int:
        nonlocal n
        n += 1
        return n

    return counter


def sum_all(*nums: int) -> int:
    """Сумма произвольного числа аргументов."""
    return sum(nums)
