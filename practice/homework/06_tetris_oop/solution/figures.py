"""Фигуры Тетриса на ООП — ЭТАЛОННОЕ РЕШЕНИЕ.

Базовый класс `Figure` содержит ОБЩУЮ логику (поворот, клетки, сравнение),
а семь наследников задают только свои ДАННЫЕ: форму (DEFAULT), цвет (COLOR)
и символ (SYMBOL).

Принципы ООП, которые тут воплощены:
  - базовый класс: общий код в Figure;
  - наследование: наследники переиспользуют методы базы;
  - супер: super().__init__() делегирует конструктору родителя;
  - полиморфизм: rotated() возвращает экземпляр того же подкласса (type(self)).
"""

from __future__ import annotations

import random

Cell = tuple[int, int]


class Figure:
    """Базовый класс: общая логика поворота и формы.

    Не создаётся напрямую (schema), служит скелетом для наследников.
    """

    COLOR: str = "?"
    SYMBOL: str = "?"

    def __init__(self, matrix: list[list[int]] | None = None) -> None:
        # Копия матрицы — чтобы не сломать общий шаблон наследника.
        self._matrix = [row[:] for row in (matrix if matrix is not None else [[0]])]

    @property
    def matrix(self) -> list[list[int]]:
        return self._matrix

    @property
    def cells(self) -> list[Cell]:
        """Координаты занятых клеток (row, col) внутри матрицы."""
        return [(r, c) for r, row in enumerate(self._matrix) for c, val in enumerate(row) if val]

    @property
    def size(self) -> int:
        return len(self._matrix)

    def rotated(self) -> Figure:
        """Новая фигура с матрицей, повёрнутой на 90° вправо.

        Полиморфизм: type(self) — вернём экземпляр ТОГО ЖЕ подкласса.
        """
        m = self._matrix
        n = len(m)
        rotated_mx: list[list[int]] = [[0] * n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                rotated_mx[c][n - 1 - r] = m[r][c]
        return type(self)(rotated_mx)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Figure):
            return NotImplemented
        return self._matrix == other._matrix

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class FigureI(Figure):
    """Палочка (Line)."""

    DEFAULT = [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]
    COLOR = "Cyan"
    SYMBOL = "I"

    def __init__(self, matrix: list[list[int]] | None = None) -> None:
        super().__init__(matrix if matrix is not None else self.DEFAULT)


class FigureO(Figure):
    """Квадрат 2x2 (симметричный — поворот не меняет форму)."""

    DEFAULT = [[1, 1], [1, 1]]
    COLOR = "Yellow"
    SYMBOL = "O"

    def __init__(self, matrix: list[list[int]] | None = None) -> None:
        super().__init__(matrix if matrix is not None else self.DEFAULT)


class FigureT(Figure):
    """«Тэшка»."""

    DEFAULT = [[0, 1, 0], [1, 1, 1], [0, 0, 0]]
    COLOR = "Purple"
    SYMBOL = "T"

    def __init__(self, matrix: list[list[int]] | None = None) -> None:
        super().__init__(matrix if matrix is not None else self.DEFAULT)


class FigureS(Figure):
    """S-образная."""

    DEFAULT = [[0, 1, 1], [1, 1, 0], [0, 0, 0]]
    COLOR = "Green"
    SYMBOL = "S"

    def __init__(self, matrix: list[list[int]] | None = None) -> None:
        super().__init__(matrix if matrix is not None else self.DEFAULT)


class FigureZ(Figure):
    """Z-образная."""

    DEFAULT = [[1, 1, 0], [0, 1, 1], [0, 0, 0]]
    COLOR = "Red"
    SYMBOL = "Z"

    def __init__(self, matrix: list[list[int]] | None = None) -> None:
        super().__init__(matrix if matrix is not None else self.DEFAULT)


class FigureJ(Figure):
    """J-образная (крюк влево)."""

    DEFAULT = [[1, 0, 0], [1, 1, 1], [0, 0, 0]]
    COLOR = "Blue"
    SYMBOL = "J"

    def __init__(self, matrix: list[list[int]] | None = None) -> None:
        super().__init__(matrix if matrix is not None else self.DEFAULT)


class FigureL(Figure):
    """L-образная (крюк вправо)."""

    DEFAULT = [[0, 0, 1], [1, 1, 1], [0, 0, 0]]
    COLOR = "Orange"
    SYMBOL = "L"

    def __init__(self, matrix: list[list[int]] | None = None) -> None:
        super().__init__(matrix if matrix is not None else self.DEFAULT)


# Все семь наследников — для фабрики random_figure().
ALL_FIGURES: tuple[type[Figure], ...] = (
    FigureI,
    FigureO,
    FigureT,
    FigureS,
    FigureZ,
    FigureJ,
    FigureL,
)


def random_figure() -> Figure:
    """Случайная фигура из всех наследников (фабрика)."""
    return random.choice(ALL_FIGURES)()
