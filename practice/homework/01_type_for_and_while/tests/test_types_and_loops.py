"""Тесты для types_and_loops.py — pytest.

Запуск:  pytest  (в корне проекта)
"""

from types_and_loops import (
    bucket_by,
    common_elements,
    distance,
    fibonacci,
    flatten,
    greet,
    head_tail,
    index_of_first_negative,
    is_prime,
    merge_counts,
    only_duplicates,
    pairing,
    sliding_window,
    swap,
    take,
    tally,
    unique_preserving_order,
)


class TestTuple:
    def test_swap(self) -> None:
        assert swap((1, 2)) == (2, 1)

    def test_head_tail(self) -> None:
        assert head_tail([9, 8, 7]) == (9, [8, 7])
        assert head_tail([]) == (None, [])

    def test_distance_pythagorean(self) -> None:
        assert distance((0, 0), (3, 4)) == 5.0


class TestDict:
    def test_tally(self) -> None:
        assert tally("a b a".split()) == {"a": 2, "b": 1}

    def test_merge_count(self) -> None:
        assert merge_counts({"x": 1}, {"x": 2, "y": 3}) == {"x": 3, "y": 3}

    def test_bucket(self) -> None:
        groups = bucket_by(range(6), lambda n: n % 2)
        assert groups[0] == [0, 2, 4]
        assert groups[1] == [1, 3, 5]


class TestSet:
    def test_common(self) -> None:
        assert common_elements([1, 2, 3], [2, 3, 4]) == {2, 3}

    def test_unique_order(self) -> None:
        assert unique_preserving_order([3, 1, 3, 2, 1]) == [3, 1, 2]


class TestComprehension:
    def test_flatten(self) -> None:
        assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    def test_duplicates(self) -> None:
        assert only_duplicates([1, 2, 2, 3, 3, 3]) == {2, 3}


class TestGenerators:
    def test_fibonacci(self) -> None:
        assert take(fibonacci(), 10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_sliding_window(self) -> None:
        assert list(sliding_window([1, 2, 3, 4, 5], 3)) == [
            (1, 2, 3),
            (2, 3, 4),
            (3, 4, 5),
        ]

    def test_sliding_window_bad_size(self) -> None:
        try:
            value = list(sliding_window([1, 2], 0))
            assert value == [], "expected ValueError on bad size"
        except ValueError:
            pass


class TestLoops:
    def test_first_negative(self) -> None:
        assert index_of_first_negative([1, 2, -3]) == 2
        assert index_of_first_negative([1, 2]) is None

    def test_primes(self) -> None:
        assert [n for n in range(20) if is_prime(n)] == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_pairing(self) -> None:
        assert pairing(["a", "b"], [1, 2]) == {"a": 1, "b": 2}


class TestProtocol:
    def test_greet(self) -> None:
        class User:
            name = "Вася"

        assert greet(User()) == "Привет, Вася!"
