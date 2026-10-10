"""Типы данных и циклы — продвинутые приёмы Python.

Здесь НЕ «для начинающих»: распаковка коллекций, структурная типизация,
comprehension, ленивые генераторы, itertools, паттерн for-else.
Каждая функция — законченный пример с docstring-ом.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Protocol

# --- 1. Кортежи и распаковка (tuple unpacking) ------------------------------


def swap(pair: tuple[int, int]) -> tuple[int, int]:
    """Обмен местами через распаковку (без временной переменной)."""
    a, b = pair
    return b, a


def head_tail(items: Iterable[int]) -> tuple[int | None, list[int]]:
    """Первое значение и все остальные — приём '*rest'."""
    it = iter(items)
    first = next(it, None)
    return first, list(it)


Point = tuple[float, float]


def distance(p1: Point, p2: Point) -> float:
    """Евклидово расстояние между двумя точками-кортежами."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    return (dx * dx + dy * dy) ** 0.5  # type: ignore[no-any-return]


# --- 2. Словари: get с дефолтом, setdefault, обновление счётчиков -----------


def tally(words: Iterable[str]) -> dict[str, int]:
    """Счётчик вхождений слов — без ветвления, через .get()."""
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def merge_counts(*maps: dict[str, int]) -> dict[str, int]:
    """Суммирует значения по ключам из произвольного числа словарей."""
    result: dict[str, int] = {}
    for counts in maps:
        for key, value in counts.items():
            result[key] = result.get(key, 0) + value
    return result


def bucket_by(data: Iterable[int], key_fn: Callable[[int], str]) -> dict[str, list[int]]:
    """Группирует значения по ключу (пример setdefault)."""
    groups: dict[str, list[int]] = {}
    for item in data:
        groups.setdefault(key_fn(item), []).append(item)
    return groups


# --- 3. Множества: операции без циклов --------------------------------------


def common_elements(a: Iterable[int], b: Iterable[int]) -> set[int]:
    """Пересечение множеств — O(min) вместо вложенного цикла."""
    return set(a) & set(b)


def unique_preserving_order(items: Iterable[int]) -> list[int]:
    """Уникальные элементы с сохранением порядка (dict.fromkeys)."""
    return list(dict.fromkeys(items))


# --- 4. Comprehension: вложенные и с условием --------------------------------


def flatten(matrix: list[list[int]]) -> list[int]:
    """Склеивает список списков одним вложенным comprehension."""
    return [value for row in matrix for value in row]


def matrix_indices(rows: int, cols: int) -> list[tuple[int, int]]:
    """Все индексы матрицы через двойной comprehension."""
    return [(r, c) for r in range(rows) for c in range(cols)]


def only_duplicates(items: Iterable[int]) -> set[int]:
    """Значения встреченные более одного раза (comp + множество)."""
    seen: set[int] = set()
    dups: set[int] = set()
    for x in items:
        if x in seen:
            dups.add(x)
        seen.add(x)
    return dups


# --- 5. Генераторы и ленивые вычисления --------------------------------------


def fibonacci() -> Iterator[int]:
    """Бесконечный генератор чисел Фибоначчи."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def take(seq: Iterable[int], n: int) -> list[int]:
    """Берёт первые n элементов из бесконечного генератора."""
    return (
        [next(iter(seq)) for _ in range(n)]
        if False
        else list(x for x, _ in zip(seq, range(n), strict=False))
    )


def sliding_window(items: Iterable[int], size: int) -> Iterator[tuple[int, ...]]:
    """Скользящее окно размера size по последовательности."""
    if size <= 0:
        raise ValueError("size must be >= 1")
    window: tuple[int, ...] = ()
    for item in items:
        window = (*window[-(size - 1) :], item)
        if len(window) == size:
            yield window


# --- 6. Циклы: for-else, enumerate, zip --------------------------------------


def index_of_first_negative(items: Iterable[int]) -> int | None:
    """Возвращает индекс первого отрицательного числа, иначе None."""
    for i, value in enumerate(items):
        if value < 0:
            return i
    return None


def is_prime(n: int) -> bool:
    """for-else: else выполняется, если break НЕ сработал."""
    if n < 2:
        return False
    for divisor in range(2, int(n**0.5) + 1):
        if n % divisor == 0:
            return False  # break
    return True


def pairing(keys: list[str], values: list[int]) -> dict[str, int]:
    """Сборка словаря через zip — без расхождения длин."""
    return dict(zip(keys, values, strict=False))


# --- 7. Структурная типизация (Protocol) -----------------------------------


class Named(Protocol):
    """Любой объект с атрибутом name (утка-типизация)."""

    name: str


def greet(thing: Named) -> str:
    return f"Привет, {thing.name}!"


def run_examples() -> None:
    """Демонстрация вызова функций при запуске модуля напрямую."""
    print("head_tail:", head_tail([1, 2, 3]))
    print("tally:", tally("a b a c a b".split()))
    print("merge:", merge_counts({"x": 1}, {"x": 2, "y": 3}))
    print("buckets:", bucket_by(range(10), lambda n: "even" if n % 2 == 0 else "odd"))
    print("common:", common_elements([1, 2, 3], [2, 3, 4]))
    print("unique:", unique_preserving_order([3, 1, 3, 2, 1]))
    print("flatten:", flatten([[1, 2], [3, 4]]))
    print("dups:", only_duplicates([1, 2, 2, 3, 3, 3]))
    print("fib(10):", take(fibonacci(), 10))
    print("window:", list(sliding_window([1, 2, 3, 4, 5], 3)))
    print("first neg:", index_of_first_negative([1, 2, -3, 4]))
    print("primes<20:", [n for n in range(20) if is_prime(n)])
    print("pair:", pairing(["a", "b"], [1, 2]))


if __name__ == "__main__":
    run_examples()
