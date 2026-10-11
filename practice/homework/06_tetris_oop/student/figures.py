"""Фигуры Тетриса на ООП — VERSION ДЛЯ СТУДЕНТА.

❌ НЕДОПИСАНА. Твоя задача — восстановить код так, чтобы:
    1. `Figure` был базовым классом с ОБЩЕЙ логикой;
    2. семь наследников (I, O, T, S, Z, J, L) задавали ТОЛЬКО свои данные;
    3. поворот работал для ВСЕХ фигур через один метод базы (полиморфизм);
    4. тесты в `tests/` проходили.

Правила:
    • НИЧЕГО не удалять и не переименовывать уже написанное.
    • Дополни пропущенные части: тело методов, большие дикты, наследование.
    • Места для вставки отмечены  TODO(студент).
"""

from __future__ import annotations


class Figure:
    """Базовый класс: общая логика поворота и формы.

    В базе живёт то, что ОБЩЕЕ для всех фигур. Наследники переопределяют
    только данные (матрицу-форму и цвет).
    """

    # TODO(студент): задай атрибуты класса по умолчанию.
    COLOR: str = "?"
    SYMBOL: str = "?"

    def __init__(self, matrix: list[list[int]] | None = None) -> None:
        # Копируем матрицу, чтобы не сломать общий шаблон наследника.
        # TODO(студент): если matrix is None — используй пустую [[0]].
        self._matrix = [row[:] for row in matrix]

    @property
    def matrix(self) -> list[list[int]]:
        return self._matrix

    @property
    def cells(self) -> list[tuple[int, int]]:
        """Координаты занятых клеток (row, col) внутри матрицы.

        TODO(студент): верни список пар (r, c), где в матрице стоит 1.
        """
        # Подсказка: двойное comprehension по enumerate(matrix).
        ...

    @property
    def size(self) -> int:
        return len(self._matrix)

    def rotated(self) -> Figure:
        """Новая фигура с матрицей, повёрнутой на 90° вправо.

        TODO(студент): реализуй поворот. Возвращай ЭКЗЕМПЛЯР ТОГО ЖЕ
        подкласса (через type(self)(rotated_matrix)) — это полиморфизм.
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


# TODO(студент): это ТОЛЬКО ПРИМЕР. Сделай так же для остальных шести (O, T, Z, J, L).
# Наследник вызывает super().__init__(matrix or self.DEFAULT) и задаёт COLOR/SYMBOL.
class FigureI(Figure):
    """Горизонтальная палочка (Line)."""

    DEFAULT = [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]
    COLOR = "Cyan"
    SYMBOL = "I"

    def __init__(self, matrix: list[list[int]] | None = None) -> None:
        super().__init__(matrix if matrix is not None else self.DEFAULT)


# TODO(студент): реализуй оставшиеся шестнадцать строчек:
#   FigureO:  DEFAULT = [[1,1],[1,1]]; COLOR Yellow; symbol O
#   FigureT:  DEFAULT = [[0,1,0],[1,1,1],[0,0,0]]; Purple; T
#   FigureS:  DEFAULT = [[0,1,1],[1,1,0],[0,0,0]]; Green; S
#   FigureZ:  DEFAULT = [[1,1,0],[0,1,1],[0,0,0]]; Red; Z
#   FigureJ:  DEFAULT = [[1,0,0],[1,1,1],[0,0,0]]; Blue; J
#   FigureL:  DEFAULT = [[0,0,1],[1,1,1],[0,0,0]]; Orange; L


# TODO(студент): собери ВСЕ классы в этот кортеж (используй type[Figure]).
ALL_FIGURES: tuple[type[Figure], ...] = (
    FigureI,
)


def random_figure() -> Figure:
    """Случайная фигура из всех наследников (фабрика).

    TODO(студент): верни random.choice(ALL_FIGURES)().
    """
    import random

    return random.choice(ALL_FIGURES)() if False else None  # заглушка