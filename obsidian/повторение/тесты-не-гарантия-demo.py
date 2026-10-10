"""Демонстрация: зелёные тесты НЕ гарантируют отсутствия багов.

Сценарий: в методе clear_rows() спрятан тонкий баг — классика
"мутация списка во время итерации по индексу".
Тесты ниже ВСЕ ЗЕЛЁНЫЕ. Но есть случай, который они НЕ покрывают.

Запуск:  uv run python тесты-не-гарантия-demo.py
"""

from __future__ import annotations

WIDTH = 10

# Только метод clear_rows() — самый минимум, чтобы показать идею.


def clear_rows_buggy(grid: list[list[str | None]]) -> int:
    """❌ Версия с багом: удаляем ряды через while, но индекс ВСЕГДА сдвигаем.

    Когда два полных ряда стоят подряд, после удаления первого второй ряд
    «всплывает» на его место, а индекс уже перешёл дальше — второй ряд
    ПРОПУСКАЕТСЯ и НЕ исчезает. Ошибка «молчаливая»: функция возвращает
    меньше, чем нужно, ничего не падает.
    """
    cleared = 0
    y = 0
    while y < len(grid):
        if all(c is not None for c in grid[y]):
            del grid[y]  # удалили ряд — следующий встаёт на то же место
            cleared += 1
        y += 1  # ❌ БАГ: надо бы НЕ сдвигать индекс после удаления
    # Добиваем новыми пустыми рядами сверху (в небытие ушло `cleared` штук).
    for _ in range(cleared):
        grid.insert(0, [None] * WIDTH)
    return cleared


def make_grid(rows: list[list[str | None]]) -> list[list[str | None]]:
    return [row[:] for row in rows]


FULL: list[str | None] = ["X"] * WIDTH  # полностью заполненный ряд
EMPTY: list[str | None] = [None] * WIDTH  # пустой ряд


# ================= ТЕСТЫ (все проходят!) =================

def test_clear_one_full_row() -> None:
    grid = make_grid([EMPTY, EMPTY, FULL])  # 1 полный ряд снизу
    assert clear_rows_buggy(grid) == 1


def test_empty_grid_no_rows_cleared() -> None:
    grid = make_grid([EMPTY, EMPTY, EMPTY])
    assert clear_rows_buggy(grid) == 0


def test_clear_one_full_row_removes_it() -> None:
    grid = make_grid([EMPTY, EMPTY, FULL])
    clear_rows_buggy(grid)
    assert len(grid) == 3  # размер поля не изменился
    assert grid[2] == [None] * WIDTH  # низ снова пустой


# ================= СЛУЧАЙ, КОТОРЫЙ ТЕСТЫ НЕ ПОКРЫВАЮТ =================

def test_TWO_consecutive_full_rows() -> None:
    """Два полных ряда ПОДРЯД. Это баг: должен вернуть 2 и убрать оба,
    но из-за логики возвращается 1 и второй ряд остаётся."""
    grid = make_grid([EMPTY, FULL, FULL])  # 2 полных ряда подряд
    result = clear_rows_buggy(grid)
    # Ожидали: очищено 2 ряда. А получили 1 — второй «не исчез».
    assert result == 2, f"БАГ! Очищено {result}, а должно быть 2"


# ================= ЗАПУСК =================

def main() -> None:
    print("Запускаем ТЕ ЖЕ тесты, что у студента...\n")
    failures = 0
    for test in (
        test_clear_one_full_row,
        test_empty_grid_no_rows_cleared,
        test_clear_one_full_row_removes_it,
    ):
        try:
            test()
            print(f"  ✅ {test.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"  ❌ {test.__name__}: {e}")

    print("\nОбычные тесты зелёные. А теперь проверим пропущенный случай:\n")
    try:
        test_TWO_consecutive_full_rows()
        print("  ✅ два подряд — ОК (теста нет, бага не видно)")
    except AssertionError as e:
        print(f"  🔴 {e}\n")

    if failures == 0:
        print(
            "ИТОГ: все стандартные тесты зелёные, НО баг существует — "
            "его просто никто не проверил.\n"
            "Тесты — это страховка, а не гарантия. Им нужно ПОКРЫТИЕ гран. случаев."
        )


if __name__ == "__main__":
    main()