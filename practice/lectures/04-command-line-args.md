# Аргументы командной строки в Python. Модуль argparse

> Стандартный модуль `argparse`. Не нужен `pip install` — уже в Python.
> Автоматически генерирует `--help`, сообщения об ошибках и проверяет типы.

---

## 1. Зачем нужны аргументы?

### Проблема `input()`

Стандартный ввод требует присутствия человека у клавиатуры — скрипт останавливается и ждёт. Это делает невозможным автоматический запуск: нельзя поставить такую программу в cron, в CI/CD-пайплайн или вызвать её из другого скрипта без дополнительных ухищрений.

### Решение через терминал

Аргументы командной строки позволяют передать все настройки в момент старта программы. Пользователь не нужен — скрипт сразу получает всё необходимое и выполняется без остановок. Это идеально для автоматизации, серверов и планировщиков задач.

### Пример запуска с аргументами

```bash
$ python main.py Кирилл -t 4
```

- `main.py` — сам скрипт
- `Кирилл` — основной (позиционный) аргумент
- `-t 4` — аргумент-флаг: повторить 4 раза

Главный принцип: **код один раз, данные — каждый раз новые из терминала**.

---

## 2. Базовый подход: `sys.argv`

`sys.argv` — встроенный список из модуля `sys`. Он хранит всё, что было написано в терминале при запуске, разбитое по пробелам.

```python
# $ python main.py 42 --user admin
import sys

print(sys.argv)
# ['main.py', '42', '--user', 'admin']
```

Особенности `sys.argv`:

- `sys.argv[0]` — всегда имя запущенного скрипта
- **Тип данных: исключительно строки.** Числа нужно преобразовывать вручную: `int(sys.argv[1])`
- Проверка длины и корректности лежит на программисте — риск `IndexError` и `ValueError`
- Нет справки, нет значений по умолчанию, нет понятных ошибок

**Аналогия:** `sys.argv` — мешок с записками. `argparse` — официант, который разложит всё по полочкам и проверит заказ.

---

## 3. Почему используют `argparse`?

- Сам генерирует понятную справку по флагу `-h`
- Автоматически конвертирует строки в числа, файлы и другие типы
- Позволяет задавать значения по умолчанию
- Выдаёт информативные ошибки при неверном вводе
- Входит в стандартную библиотеку Python — `pip install` не нужен

---

## 4. Три шага работы с `argparse`

```python
import argparse

# Шаг 1 — создать парсер
parser = argparse.ArgumentParser(description="Описание программы")

# Шаг 2 — описать аргументы
parser.add_argument("name", help="Твоё имя")
parser.add_argument("--times", type=int, default=1, help="Сколько раз повторить")

# Шаг 3 — разобрать команду
args = parser.parse_args()

for _ in range(args.times):
    print(f"Привет, {args.name}!")
```

| Шаг | Метод | Что делает |
|-----|-------|------------|
| 1 | `ArgumentParser()` | Создаёт объект парсера. Можно указать `description` |
| 2 | `add_argument()` | Описывает ожидаемые данные. Вызывается для каждого аргумента |
| 3 | `parse_args()` | Читает команду, валидирует и возвращает объект `Namespace` |

```bash
$ python main.py Кирилл --times 3
Привет, Кирилл!
Привет, Кирилл!
Привет, Кирилл!
```

---

## 5. Виды аргументов

| Вид | Синтаксис | Обязательный? | Пример |
|-----|-----------|---------------|--------|
| Позиционный | `add_argument("name")` | Да | `script.py Аня` |
| Опциональный | `add_argument("--times")` | Нет (есть `default`) | `script.py --times 3` |
| Флаг | `action="store_true"` | Нет | `script.py --debug` |
| Короткая форма | `"-t", "--times"` | Нет | `script.py -t 3` |

### Позиционные

Пишутся без дефисов, пользователь **обязан** их передать, порядок строго важен. Подходят для главного входного значения: имя файла, запрос и т.д.

### Опциональные

Идентифицируются по префиксу `-` или `--`. Можно пропускать, можно указывать в любом порядке; `-t` и `--times` — одно и то же.

### Флаги

Работают как переключатель: указан → `True`, не указан → `False`.

```python
parser.add_argument("--verbose", action="store_true", help="детальный вывод")
parser.add_argument("--count", type=int, default=1, help="сколько раз")
parser.add_argument("-o", "--output", help="путь к файлу")
```

---

## 6. Основные функции модуля

| Функция | Для чего |
|---------|----------|
| `ArgumentParser()` | Создать парсер. Принимает `description` |
| `add_argument()` | Добавить аргумент. Вызывается для каждого отдельно |
| `parse_args()` | Разобрать команду и вернуть объект `Namespace` |
| `print_help()` | Вывести справку — ту же, что по флагу `-h` |
| `error()` | Вывести ошибку в стиле `argparse` и завершить программу |
| `add_mutually_exclusive_group()` | Группа опций, которые нельзя указать вместе |
| `add_subparsers()` | Подкоманды, как `git add`, `git commit`, `git push` |

**Первые три нужны почти всегда. Остальные — по мере необходимости.**

---

## 7. Полезные параметры `add_argument()`

| Параметр | Что делает | Пример |
|----------|------------|--------|
| `help` | Подсказка в справке `--help` | `help="ваше имя"` |
| `type` | Перевести строку в тип | `type=int` |
| `default` | Значение, если аргумент не указан | `default=1` |
| `choices` | Список допустимых значений | `choices=["add","sub"]` |
| `required` | Сделать опцию обязательной | `required=True` |
| `action` | Что сделать с аргументом | `"store_true"` |
| `nargs` | Сколько значений принять | `"+"` |
| `dest` | Имя атрибута в объекте `args` | `dest="output"` |

```python
parser.add_argument(
    "-o",
    "--output",
    type=str,
    default="result.txt",
    help="Путь к выходному файлу",
    dest="output_file",
)
# args.output_file → "result.txt" по умолчанию
```

---

## 8. Управление поведением: `action` и `nargs`

### Параметр `action`

| Значение | Поведение |
|----------|-----------|
| `"store"` | Сохранить значение (по умолчанию) |
| `"store_true"` | Флаг: указан → `True`, нет → `False` |
| `"store_false"` | Флаг наоборот: указан → `False` |
| `"count"` | Считать количество указаний: `-vvv` → `3` |
| `"append"` | Повторы в список: `--tag a --tag b` → `["a","b"]` |
| `"version"` | Вывести версию программы и выйти |

```python
parser.add_argument("--verbose", action="store_true")
parser.add_argument("-v", action="count", default=0)
parser.add_argument("--tag", action="append")
# -vvv              → args.v == 3
# --tag a --tag b   → args.tag == ["a", "b"]
```

### Параметр `nargs`

| Значение | Сколько | Результат |
|----------|---------|-----------|
| `N` (число) | Ровно N | список из N элементов |
| `"?"` | 0 или 1 | значение или `None` |
| `"*"` | 0 и больше | список (может быть пустым) |
| `"+"` | 1 и больше | список (0 — ошибка) |

```python
parser.add_argument("--files", nargs="+")
parser.add_argument("--point", nargs=2, type=int)
# --files a.txt b.txt c.txt   → ["a.txt","b.txt","c.txt"]
# --point 3 4                 → [3, 4]
```

> **Важно:** при `nargs` результат — всегда список, даже если передано одно значение.

---

## 9. Подкоманды (subcommands) — как у реальных CLI

```python
parser = argparse.ArgumentParser(prog="app")
sub = parser.add_subparsers(dest="command", required=True)

sub_hello = sub.add_parser("hello", help="поздороваться")
sub_hello.add_argument("name")

sub_add = sub.add_parser("add", help="сложить два числа")
sub_add.add_argument("a", type=int)
sub_add.add_argument("b", type=int)

args = parser.parse_args()

if args.command == "hello":
    print(f"Привет, {args.name}")
elif args.command == "add":
    print(args.a + args.b)
```

```bash
python app.py add 3 4      # -> 7
python app.py hello Ира    # -> Привет, Ира
```

---

## 10. Получение результата: `Namespace`

Метод `parse_args()` возвращает объект `Namespace`. Все объявленные аргументы становятся его атрибутами.

```python
args = parser.parse_args()
print("Файл:", args.filename)
if args.max_size > 100:
    print("Файл слишком большой")
```

Особенности:

- Обращение через точку: `args.filename`, `args.times`
- Дефисы в именах флагов (`--file-name`) автоматически заменяются на подчёркивания: `args.file_name`
- `vars(args)` превращает `Namespace` в обычный словарь

```python
print(vars(args))
# {'filename': 'data.txt', 'max_size': 50}
```

---

## 11. Готовый шаблон для реального скрипта

```python
import argparse
from typing import Sequence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="tool",
        description="Пример CLI с несколькими способами ввода",
    )
    parser.add_argument("files", nargs="+", help="файлы для обработки")
    parser.add_argument("-o", "--output", default="result.txt")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument("--limit", type=int, default=None)
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()
    if args.verbose:
        print(f"files={args.files}, output={args.output}, limit={args.limit}")


if __name__ == "__main__":
    main()
```

---

## 12. Выводы

- **Аргументы командной строки** — данные, которые программа получает при запуске, без правки кода
- **`sys.argv`** хранит их как сырой список строк — просто, но неудобно для чего-то сложнее 1–2 аргументов
- **`argparse`** — стандартный модуль Python, устанавливать не нужно
- Три шага: `ArgumentParser` → `add_argument` → `parse_args`
- `argparse` сам делает справку, проверки типов и понятные ошибки

| Инструмент | Когда использовать |
|------------|-------------------|
| `sys.argv` | Простые скрипты, 1–2 аргумента |
| `argparse` | Почти всегда: встроен в Python |
| `click`, `typer` | Большие консольные приложения (нужен `pip install`) |

---

## Шпаргалка

- Позиционный аргумент — имя без `--`.
- Значение по умолчанию — `default=`.
- Проверка типа — `type=int`.
- Флаг-переключатель — `action="store_true"`.
- Несколько значений — `nargs="+"`.
- Счётчик повторов — `action="count"`.
- Подкоманды — `add_subparsers(dest="command")`.
- Справку не пиши сам — её генерирует `--help`.

*Документация: [docs.python.org/3/library/argparse.html](https://docs.python.org/3/library/argparse.html)*
