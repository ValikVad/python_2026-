# Python 2026 — учебный курс

Репозиторий-курс по Python: **Obsidian-vault с конспектами** (`practice/`), пакеты
домашних заданий с тестами и современный тулинг (uv, ruff, mypy, pytest, pre-commit,
GitHub Actions).

## Быстрый старт

```bash
# 1. Создать окружение и поставить зависимости (включая dev-группу)
uv sync

# 2. Прогнать все тесты курса
uv run pytest

# 3. Линт + типизация (код-уроки)
uv run ruff check practice/homework
uv run mypy practice/homework

# 4. Локальная проверка перед коммитом
uv run pre-commit run --all-files
```

> Всё делается через `uv run` — активировать `venv` вручную не нужно.

## Требования

- Python ≥ 3.10
- [uv](https://docs.astral.sh/uv/) (рекомендуется)

## Структура

```
├── README.md                      ← ты здесь (стартовый экран)
├── pyproject.toml                 ← метаданные + ruff/mypy/pytest/uv
├── requirements*.txt              ← классические списки
├── .pre-commit-config.yaml        ← линт+типизация перед commit
├── .github/workflows/ci.yml       ← CI: ruff+mypy+pytest на каждый push
│
└── practice/                      ← ⭐ Obsidian-vault (открой эту папку в Obsidian)
    ├── homework/                  ← код-уроки (каждый = мини-проект)
    │   ├── 01_type_for_and_while/ ← типы, циклы, comprehension
    │   ├── 03_function/           ← функции, замыкания
    │   ├── 04_class/              ← классы, ООП
    │   ├── 06_tetris_oop/         ← ООП через Тетрис (solution/ + student/)
    │   └── 07_lab_1/              ← итоговая лабораторная (ТЗ + TASK.md)
    ├── lectures/                  ← конспекты-доклады по темам
    ├── theory/                    ← материалы повторения, тесты-викторины, демо
    ├── notes/                     ← заметки, черновики, варианты заданий
    └── marks/                     ← оценки (в GitHub НЕ пушится, в .gitignore)
```

## Как открыть курс в Obsidian

1. **Open folder as vault** → выбери папку `practice/`.
2. Открой корневой `README.md` — стартовый экран курса.
3. Конспекты линкуются между собой (`[[]]`).

## Как проходит урок (паттерн)

1. Студент читает конспект темы (`lectures/NN-*.md`).
2. Открывает пакет `homework/NN_...` — код + тесты.
3. Для ООП (урок 06): в `student/`  stub-функции, готовое решение в `solution/`.
4. Реализует, прогоняет `uv run pytest` — тесты в `.../tests/` проверяют решение.

## CI / pre-commit

- **pre-commit** (локально): ruff (линь + формат), mypy, гигиена файлов.
- **GitHub Actions** (`.github/workflows/ci.yml`): ruff, mypy, pytest на каждый push.
- Папка `06_tetris_oop/student/` исключена из CI (недописанный код не должен ломать сборку).

## Итоговая работа

ТЗ итоговой лабораторной — `practice/homework/07_lab_1/TASK.md` (дедлайн 07.11,
треки Data Science и DevOps, на выбор одна тема).

---
*Курс Python 2026 · доклады студентов собраны в конспекты.*