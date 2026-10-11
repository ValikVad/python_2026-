# Доклад · Типы данных, изменяемость/копирование, циклы, распаковка, comprehension, генераторы

> Повторение и систематизация темы №1 ядра языка. Всё, что нужно знать наизусть — здесь.

---

## 1. В Python всё — объект

Переменная — это **имя-ярлык**, приклеенное к объекту в памяти. Тип определяется **значением**, а не именем переменной. Проверка типа: `type(x)` или `isinstance(x, T)`.

```python
x = 5  # x указывает на int
x = "hello"  # теперь на str — Python разрешает
```

## 2. Базовые типы

| Тип | Пример | Неизменяемый? | Важно |
|-----|--------|---------------|-------|
| `int` | `42` | ✅ | Битов не ограничен |
| `float` | `3.14` | ✅ | `0.1 + 0.2 != 0.3` |
| `complex` | `1+2j` | ✅ | |
| `str` | `"abc"` | ✅ | Элементы менять нельзя |
| `bytes` | `b"abc"` | ✅ | |
| `bool` | `True` | ✅ | Подкласс `int` |
| `NoneType` | `None` | ✅ | Одно значение |
| `list` | `[1,2]` | ❌ | |
| `dict` | `{"a":1}` | ❌ | |
| `set` | `{1,2}` | ❌ | |
| `bytearray` | `bytearray(b"a")` | ❌ | |

## 3. Изменяемость (mutable / immutable)

- **Изменяемые:** `list`, `dict`, `set`, `bytearray`, объекты пользовательских классов.
- **Неизменяемые:** `int`, `float`, `str`, `bytes`, `tuple`, `frozenset`, `bool`, `None`.

**Почему важно:** изменяемый объект можно менять «in place». Если передать его в функцию — изменения увидит и вызывающий код. Неизменяемый — только скопировать.

## 4. Копирование: ссылка vs копия vs глубокая копия

```python
a = [1, 2, 3]
b = a  # ССЫЛКА — тот же объект
c = a.copy()  # ПОВЕРХНОСТНАЯ копия — новый список, но вложенные — ссылки
import copy

d = copy.deepcopy(a)  # ГЛУБОКАЯ — копирует всё вложенное

b.append(4)
print(a)  # [1, 2, 3, 4]  — поменялось!
print(c)  # [1, 2, 3]     — цел
```

**Ловушка с вложенными объектами:**
```python
a = [[1], [2]]
c = a.copy()  # поверхностная
c[0].append(99)  # меняет вложенный list
print(a)  # [[1, 99], [2]]  — вложенный объект общий!
```

**Изменяемый объект как дефолт — антипаттерн:**
```python
def add(item, lst=[]):  # НЕ ДЕЛАЙ так
    lst.append(item)
    return lst


# дефолтный список создаётся ОДИН раз и переиспользуется!
```

## 5. Циклы

### `for` + `range`
```python
for i in range(5):        # 0..4
for i in range(2, 8, 2):  # 2,4,6
```

### `for-else`
`else` выполняется, если цикл прошёл **без** `break`:
```python
for d in range(2, int(n**0.5) + 1):
    if n % d == 0:
        print("составное")
        break
else:
    print("простое")
```

### `enumerate` — индекс + значение
```python
for i, ch in enumerate("abcd"):
    print(i, ch)  # 0 a, 1 b, ...
```

### `zip` — параллельный обход
```python
for name, age in zip(["Аня", "Боря"], [20, 22]):
    ...
```
У `zip` есть `strict=True` (3.10+) — бросит ошибку при разной длине.

### `while`
```python
while condition:
    ...
```

## 6. Распаковка (unpacking)

```python
a, b = (1, 2)  # кортеж
x, y = y, x  # своп без временной переменной
first, *rest = [1, 2, 3]  # first=1, rest=[2,3]
head, *mid, tail = [1, 2, 3, 4]  # 1, [2,3], 4

# распаковка словаря (3.5+)
d = {**{"a": 1}, **{"b": 2}}  # {"a":1,"b":2}
lst = [*[1, 2], *[3, 4]]  # [1,2,3,4]
```

## 7. Comprehension (генераторы списков)

```python
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
# вложенный
flat = [y for row in matrix for y in row]

# другие виды
d = {k: v for k, v in pairs}  # dict comprehension
s = {x for x in items}  # set comprehension
g = (x for x in items)  # generator comprehension (лениво!)
```

## 8. Генераторы и ленивость

- **Генератор** создаётся с `yield` или генераторным выражением `(x for x in ...)`.
- **Ленивый:** значения вычисляются на лету, не хранятся все сразу.
- Годится для бесконечных последовательностей и больших данных.

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


fib = fibonacci()
print(next(fib), next(fib), next(fib))  # 0 1 1
```

**`itertools`** — золото для итераторов: `islice`, `takewhile`, `cycle`, `repeat`, `chain`, `groupby`.

## 9. `collections` — готовые структуры

```python
from collections import Counter, defaultdict, namedtuple, deque

Counter("aab")  # {'a':2,'b':1}
defaultdict(list)  # нет KeyError
namedtuple("P", "x y")  # лёгкий класс-кортеж
deque([1, 2])  # быстрые append/pop с обоих концов
```

---

## Шпаргалка «15 фактов наизусть»

1. Всё — объект; тип определяет значение.
2. `str`, `tuple`, `int` — неизменяемые; `list`, `dict`, `set` — изменяемые.
3. `b = a` — ссылка, `b = a.copy()` — копия, `deepcopy` — глубокая.
4. Нельзя использовать изменяемый объект как дефолт аргумента.
5. `for-else` срабатывает при отсутствии `break`.
6. `enumerate` даёт индекс, `zip` — параллель, `strict=True` проверяет длину.
7. `first, *rest = ...` — звёздочка собирает «остаток».
8. `dict(zip(keys, values))` — словарь из двух списков.
9. Comprehension читается: «создай X для каждого Y, если Z».
10. `(x for x in ...)` — ленивый генератор, не список.
11. `yield` превращает функцию в генератор.
12. `bool` — подкласс `int` (`True == 1`).
13. `float("3.5")` нельзя напрямую `int()` — сначала float.
14. `None` — единственное значение `NoneType`; `is None` вместо `== None`.
15. `collections.Counter` считает за строку.
