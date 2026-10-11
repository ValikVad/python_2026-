"""Conftest: добавляет папку студента в sys.path.

Нужен, чтобы студент мог запускать тесты локально из своей папки:

    cd practice/homework/06_tetris_oop/student
    uv run python -m pytest -q

(Папка исключена из общего CI курса через pyproject.toml.)
"""

import os
import sys

HERE = os.path.dirname(__file__)
if HERE not in sys.path:
    sys.path.insert(0, HERE)