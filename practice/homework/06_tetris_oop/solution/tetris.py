"""Консольный Тетрис на ООП — ЭТАЛОННОЕ РЕШЕНИЕ.

Запуск:
    cd practice/homework/06_tetris_oop/solution
    uv run python tetris.py

Управление: ← → ↓ = движение, ↑ = поворот, пробел = пауза, q = выход.
Поле перерисовывается на месте (ANSI), не спамит в терминал.

Эта версия полностью рабочая. Работает на классах фигур из `figures.py`
(базовый Figure + наследники). Используется как справка и эталон проверки.
"""

from __future__ import annotations

import os
import random
import select
import sys
import termios
import time
import tty
from collections.abc import Iterator
from contextlib import contextmanager

from figures import ALL_FIGURES, Figure

WIDTH = 10
HEIGHT = 20


@contextmanager
def raw_mode() -> Iterator[None]:
    """Raw-режим для ВВОДА (клавиши сразу), выход-обработку не трогаем."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[tty.IFLAG] &= ~(termios.IXON | termios.ICRNL | termios.BRKINT)
    new[tty.LFLAG] &= ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)
    new[tty.CC][termios.VMIN] = 1
    new[tty.CC][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSANOW, new)
    try:
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old)


def read_key(timeout: float = 0.05) -> str:
    """Читает один символ напрямую из ОС (минуя буфер stdin)."""
    fd = sys.stdin.fileno()
    r, _, _ = select.select([fd], [], [], timeout)
    if not r:
        return ""
    return os.read(fd, 1).decode("utf-8", errors="ignore")


def read_input(timeout: float = 0.05) -> str | None:
    key = read_key(timeout)
    if not key:
        return None
    if key == "\x1b":
        seq = key
        for _ in range(3):
            nxt = read_key(0.002)
            if not nxt:
                break
            seq += nxt
        mapping = {
            "\x1b[A": "up",
            "\x1b[B": "down",
            "\x1b[C": "right",
            "\x1b[D": "left",
        }
        return mapping.get(seq)
    if key in ("q", " "):
        return key
    return None


class Board:
    """Игровое поле WIDTH×HEIGHT. НЕ ПОНИМАЕТ, какая фигура падает —
    просто работает с её общим интерфейсом (cells, symс), что и есть
    полиморфизм: неважно FigureI или FigureT — вызов одинаков."""

    def __init__(self) -> None:
        self.grid: list[list[str | None]] = [[None] * WIDTH for _ in range(HEIGHT)]

    def collides(self, figure: Figure, x: int, y: int) -> bool:
        for r, c in figure.cells:
            nx, ny = c + x, r + y
            if nx < 0 or nx >= WIDTH or ny >= HEIGHT:
                return True
            if ny >= 0 and self.grid[ny][nx] is not None:
                return True
        return False

    def lock(self, figure: Figure, x: int, y: int) -> None:
        for r, c in figure.cells:
            ny, nx = r + y, c + x
            if 0 <= ny < HEIGHT and 0 <= nx < WIDTH:
                self.grid[ny][nx] = figure.SYMBOL

    def clear_rows(self) -> int:
        empty_row: list[str | None] = [None] * WIDTH
        remaining: list[list[str | None]] = [
            row for row in self.grid if any(c is None for c in row)
        ]
        cleared = HEIGHT - len(remaining)
        self.grid = [empty_row.copy() for _ in range(cleared)] + remaining
        return cleared


class Tetris:
    def __init__(self, tick_rate: float = 0.5) -> None:
        self.board = Board()
        self.current: Figure = self._spawn()
        self.x = (WIDTH - self.current.size) // 2
        self.y = 0
        self.tick = tick_rate
        self.score = 0
        self.paused = False
        self.running = True

    def _spawn(self) -> Figure:
        # Фабрика: не знаем ЗАРАНЕЕ, какая фигура выпадет.
        return random.choice(ALL_FIGURES)()

    def _drop_ms(self) -> int:
        return max(80, int(self.tick * 1000) - self.score * 5)

    def can_move(self, dx: int, dy: int, figure: Figure | None = None) -> bool:
        fig = figure or self.current
        return not self.board.collides(fig, self.x + dx, self.y + dy)

    def move_left(self) -> None:
        if self.can_move(-1, 0):
            self.x -= 1

    def move_right(self) -> None:
        if self.can_move(1, 0):
            self.x += 1

    def move_down(self) -> bool:
        if self.can_move(0, 1):
            self.y += 1
            return True
        self.lock_current()
        return False

    def hard_move_down(self) -> None:
        while self.move_down():
            pass

    def rotate(self) -> None:
        rotated = self.current.rotated()  # полиморфизм: один метод для всех
        if not self.board.collides(rotated, self.x, self.y):
            self.current = rotated

    def lock_current(self) -> None:
        self.board.lock(self.current, self.x, self.y)
        rows = self.board.clear_rows()
        self.score += rows * 10
        self.current = self._spawn()
        self.x = (WIDTH - self.current.size) // 2
        self.y = 0
        if self.board.collides(self.current, self.x, self.y):
            self.running = False

    def toggle_pause(self) -> None:
        self.paused = not self.paused

    def render(self) -> str:
        s = "\033[2J\033[H"
        lines: list[str] = []
        for y in range(HEIGHT):
            row = []
            for x in range(WIDTH):
                cell = self.board.grid[y][x]
                row.append(cell if cell is not None else ".")
            lines.append("".join(row))
        for r, c in self.current.cells:
            ny, nx = r + self.y, c + self.x
            if 0 <= ny < HEIGHT and 0 <= nx < WIDTH:
                lines[ny] = lines[ny][:nx] + self.current.SYMBOL + lines[ny][nx + 1 :]
        s += "\r\n".join(lines)
        s += f"\r\nОчки: {self.score}   Пауза: {'ДА' if self.paused else 'нет'}"
        s += "\r\n←→↓↑ = движение, пробел = пауза, q = выход"
        return s

    def run(self) -> None:
        last = time.time()
        print("\033[2J", end="")
        sys.stdout.flush()
        try:
            with raw_mode():
                while self.running:
                    key = read_input()
                    while key is not None and self.running:
                        if key == "q":
                            self.running = False
                        elif key == " ":
                            self.toggle_pause()
                        elif key == "left":
                            self.move_left()
                        elif key == "right":
                            self.move_right()
                        elif key == "down":
                            if self.move_down():
                                last = time.time()
                        elif key == "up":
                            self.rotate()
                        key = read_input(0.001)
                    if not self.paused and time.time() - last >= self._drop_ms() / 1000:
                        last = time.time()
                        self.move_down()
                    print(self.render(), end="")
                    sys.stdout.flush()
                    time.sleep(0.02)
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            print("\033[2J\033[HИгра окончена. Очки:", self.score)
            os._exit(0)


def main() -> None:
    game = Tetris()
    game.run()


if __name__ == "__main__":
    main()
