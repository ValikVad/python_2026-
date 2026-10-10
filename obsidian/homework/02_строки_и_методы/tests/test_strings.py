"""Тесты для strings.py."""

from strings import count_words, to_slug


def test_count_words_empty() -> None:
    assert count_words("") == 0


def test_count_words_simple() -> None:
    assert count_words("one two three") == 3


def test_to_slug() -> None:
    assert to_slug("Python Курс 2026") == "python-курс-2026"
