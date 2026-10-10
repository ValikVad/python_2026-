"""Тесты для фигур Тетриса — figures.py.

Главное, что проверяется: наследование и полиморфизм.
"""

from figures import (
    ALL_FIGURES,
    Figure,
    FigureI,
    FigureL,
    FigureO,
    FigureT,
    random_figure,
)

# --- Наследование -------------------------------------------------------


def test_all_figures_are_subclasses_of_Figure() -> None:
    for cls in ALL_FIGURES:
        assert issubclass(cls, Figure)


def test_base_orientations() -> None:
    """Базовый Figure наследуют все, а его поворот работает у каждого."""
    for cls in ALL_FIGURES:
        fig = cls()
        rotated = fig.rotated()
        assert isinstance(rotated, cls)  # полиморфизм: тип сохраняется


def test_random_figure_returns_figure() -> None:
    assert isinstance(random_figure(), Figure)


# --- Формы --------------------------------------------------------------


def test_figureO_has_4_cells() -> None:
    assert len(FigureO().cells) == 4


def test_figureT_has_4_cells() -> None:
    assert len(FigureT().cells) == 4


def test_figureO_rotation_is_same() -> None:
    """Квадрат 2x2 симметричен: поворот не меняет форму."""
    o = FigureO()
    assert o.rotated() == o


def test_figureI_rotation_changes_shape() -> None:
    """Палочка при повороте меняет ориентацию."""
    i = FigureI()
    assert i.rotated() != i


# --- Цвет и символ ------------------------------------------------------


def test_figures_have_color_and_symbol() -> None:
    for cls in ALL_FIGURES:
        assert cls.COLOR != "?"
        assert cls.SYMBOL != "?"
        assert len(cls.SYMBOL) == 1


def test_symbols_are_unique() -> None:
    symbols = [cls.SYMBOL for cls in ALL_FIGURES]
    assert len(set(symbols)) == len(symbols)  # все 7 разные


# --- Равенство ----------------------------------------------------------


def test_same_figure_type_is_equal() -> None:
    assert FigureT() == FigureT()


def test_different_figure_types_are_not_equal() -> None:
    assert FigureT() != FigureL()


# --- Детальные формы ----------------------------------------------------


def test_figureI_horizontal() -> None:
    i = FigureI()
    # палочка занимает всю среднюю строку 4x4
    assert i.cells == [(1, 0), (1, 1), (1, 2), (1, 3)]


def test_figureI_vertical_after_rotation() -> None:
    i = FigureI().rotated()
    # вертикальная палочка (в колонке 2 матрицы 4x4)
    assert i.cells == [(0, 2), (1, 2), (2, 2), (3, 2)]
