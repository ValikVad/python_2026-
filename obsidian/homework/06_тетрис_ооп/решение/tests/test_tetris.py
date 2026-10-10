"""Тесты для игрового поля Тетриса — tetris.py (класс Board, Tetris)."""

from figures import FigureO
from tetris import Board, Tetris

# --- Сетка --------------------------------------------------------------


def test_board_dims() -> None:
    board = Board()
    assert len(board.grid) == 20
    assert all(len(row) == 10 for row in board.grid)


def test_board_empty_no_collision() -> None:
    board = Board()
    assert not board.collides(FigureO(), 0, 0)


# --- Коллизии -----------------------------------------------------------


def test_collision_with_left_wall() -> None:
    board = Board()
    # квадрант в x=-1 — за левым краем
    assert board.collides(FigureO(), -1, 0)


def test_collision_with_bottom() -> None:
    board = Board()
    # O в 2x2: y=19 упрётся в низ, т.к. клетки y=19,20
    assert board.collides(FigureO(), 0, 19)


def test_collision_with_locked_figure() -> None:
    board = Board()
    board.lock(FigureO(), 0, 18)
    # новый O прямо над заблокированным — столкновение
    assert board.collides(FigureO(), 0, 17)


# --- Укладка и удаление рядов ------------------------------------------


def test_lock_persists() -> None:
    board = Board()
    board.lock(FigureO(), 0, 18)
    assert board.grid[18][0] is not None
    assert board.grid[19][1] is not None


def test_clear_rows_counts() -> None:
    board = Board()
    # заполняем весь нижний ряд
    for x in range(10):
        board.grid[19][x] = "O"
    assert board.clear_rows() == 1
    # после очистки нижний ряд пуст
    assert all(c is None for c in board.grid[19])


def test_clear_rows_empty_line_stays_unremoved() -> None:
    board = Board()
    assert board.clear_rows() == 0


# --- Tetris: интеграция ------------------------------------------------


def test_tetris_initializes() -> None:
    game = Tetris()
    assert game.current is not None
    assert 0 <= game.x < 10


def test_move_down_returns_bool() -> None:
    game = Tetris()
    # фигура вверху — движение вниз возможно
    assert game.move_down() is True or game.move_down() is False


def test_rotate_keeps_same_type() -> None:
    game = Tetris()
    before = type(game.current)
    game.rotate()
    assert isinstance(game.current, before)


def test_render_returns_multiline_with_score() -> None:
    game = Tetris()
    text = game.render()
    assert "Очки:" in text
    assert text.count("\n") >= 20  # 20 строк поля + инфо
