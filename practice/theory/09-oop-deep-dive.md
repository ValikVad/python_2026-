# Глубже · 1.5–1.9: property, наследование+ABC, dataclass, Protocol, магические методы

> Подробный разбор пяти «фишек» ООП в Python. Рядом — запускаемый код `ооп-примеры.py`.

---

## 1.5. Свойства (`@property`) — умный доступ к атрибутам

### Зачем
В Java вы пишете `getCelsius()` / `setCelsius()`, чтобы контролировать доступ.
В Python это выглядит как обычный атрибут, но за ним стоит метод:

```python
class Temperature:
    def __init__(self, c=0):
        self._c = c  # "приватный" по соглашению

    @property  # геттер
    def celsius(self):
        return self._c

    @celsius.setter  # сеттер
    def celsius(self, v):
        if v < -273.15:
            raise ValueError("ниже абсолютного нуля нет!")
        self._c = v

    @celsius.deleter  # deleter (редко нужен)
    def celsius(self):
        del self._c


t = Temperature()
t.celsius = 25  # выглядит как поле, но вызывает setter
print(t.celsius)  # 25 — геттер
try:
    t.celsius = -300  # ValueError!
except ValueError as e:
    print("поймали:", e)
```

### Три части
| Декоратор | Когда вызывается |
|---|---|
| `@property` | чтение `obj.attr` |
| `@name.setter` | запись `obj.attr = value` |
| `@name.deleter` | `del obj.attr` |

### Нюансы
- **Обратная совместимость:** можно начать с обычного атрибута, потом обернуть
  в `@property` — внешний код `t.celsius` не меняется, а логика добавилась.
- Свойство **нельзя переопределить в наследнике «атрибутом»** — это то же имя,
  значит забыть `@property` там = сломать.
- Для ЛИШЬ-чтения: геттер без сеттера.
- Альтернатива для простых вычисляемых полей — не нужна; `property` незаменим там,
  где нужна **валидация при записи** или **вычисление при чтении**.

---

## 1.6. Наследование, ABC, миксины

### Жёсткое наследование (one-parent)
`class FigureI(Figure)` — один родитель. Python разрешает и несколько, но это
сложно (см. MRO). На практике чаще: **один родитель + миксины**.

### Абстрактные базовые классы (ABC) — «скелет с обязательными методами»
Если знать, что базу нельзя создавать напрямую, а наследник ОБЯЗАН реализовать часть — ABC:

```python
from abc import ABC, abstractmethod


class Shape(ABC):  # ABC — нельзя инстанцировать
    @abstractmethod
    def area(self) -> float:
        """Обязательно у наследников."""
        ...

    @abstractmethod
    def perimeter(self) -> float: ...


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side**2

    def perimeter(self):
        return 4 * self.side


# s = Shape()  # TypeError! нельзя
sq = Square(4)
print(sq.area(), sq.perimeter())  # 16 16
```

Ключевое: **без `area()`/`perimeter()` `Square` сам станет абстрактным**
и создать его не выйдет — компилятор/интерпретатор не даст. Это возвращает строгость,
потерянную из-за динамики.

### Миксины — повторное использование без «семейных» связей
Миксин — класс без смысла «быть» кем-то, просто набор методов. Наследуют вместе
с основным классом (множественное наследование):

```python
class SerializableMixin:
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


class User(SerializableMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age


u = User("Аня", 20)
print(u.to_dict())  # {'name': 'Аня', 'age': 20}
```
Миксин не описывает «кем является», а добавляет **поведение**.

### Порядок MRO — почему множественное наследование сложное
```python
class A:
    def who(self):
        return "A"


class B(A):
    pass


class C(A):
    def who(self):
        return "C"


class D(B, C):
    pass


print(D.mro())  # [D, B, C, A, object]
print(D().who())  # 'C' — берётся из C (первый в MRO, кто умеет)
```
`super()` идёт по этому порядку. Понять без практики сложно, поэтому миксины
делают **простыми и без `__init__`** — чтобы не лезть в MRO-головоломки.

---

## 1.7. `dataclass` — классы для данных без шаблонного кода

### Проблема
Обычный класс данных требует тонны шаблона (init/repr/eq). `dataclass` пишет это **за тебя**:

```python
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
print(p1)  # Point(x=1.0, y=2.0)  — __repr__
print(p1 == p2)  # True                 — __eq__ по полям
```

### Ключевые параметры `@dataclass`
| Параметр | Что делает |
|---|---|
| `@dataclass` | `__init__`, `__repr__`, `__eq__` |
| `@dataclass(order=True)` | + `__lt__`, `__le__`, `__gt__`, `__ge__` |
| `@dataclass(frozen=True)` | поля **неизменяемы** (аналог immutаble) |
| `@dataclass(slots=True)` | экономия памяти |

### Поля и дефолты
```python
@dataclass
class Point:
    x: float
    y: float = 0.0  # дефолт — после обязательных!
    label: str = "punt"
```

### `field()` — тонкая настройка
```python
from dataclasses import dataclass, field


@dataclass
class Inventory:
    name: str
    items: list[str] = field(default_factory=list)  # НЕ изменяемый дефолт!
```
⚠️ **Никогда** не ставь `items: list = []` напрямую в dataclass — это тот же баг
«изменяемый дефолт», `default_factory` решает его.

### `frozen=True` — вариант «инкапсуляции»
```python
@dataclass(frozen=True)
class Config:
    host: str
    port: int


c = Config("localhost", 5432)
# c.port = 9000  # FrozenInstanceError!
```
Не полная защита, но помогает от случайного изменения конфига.

### `asdict` / `replace`
```python
from dataclasses import asdict, replace
Point(x=1, y=2) -> {"x":1,"y":2}   # asdict
pointb = replace(p, x=99)          # копия с новым значением
```

---

## 1.8. `Protocol` — структурная (утиная) подтипизация

### Проблема
Duck typing работает в рантайме, но `mypy` не знает, что за объект. `Protocol`
говорит статическому анализатору: «подойдёт ЛЮБОЙ с такими полями/методами».

```python
from typing import Protocol


class Named(Protocol):
    name: str

    def greet(self) -> str: ...


def hello(x: Named) -> str:
    return f"Привет, {x.name}. {x.greet()}"
```

`Named` — **не** родитель. `Dog` не наследуется от него, но **структурно** подходит:
```python
class Dog:
    name = "Шарик"

    def greet(self):
        return "Гав!"


class Robot:
    name = "R2D2"

    def greet(self):
        return "beep"


print(hello(Dog()))  # ок для mypy
print(hello(Robot()))  # ок для mypy
```
`mypy` проверяет, что передаваемый объект **имеет `name` и `greet()`** —
без требования наследования. Это «контракт по форме», а не по родству.

### `runtime_checkable` — проверка в рантайме
```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Sized(Protocol):
    def __len__(self) -> int: ...
```
Позволяет `isinstance(x, Sized)` — но проверяет ТОЛЬКО наличие методов, не типы.

### Зачем
- Явный контракт для `mypy` без привязки к классу-родителю.
- Идеален для **плагинов/интерфейсов**: «мне нужны вот такие методы».

---

## 1.9. Магические (dunder) методы — операторы через методы

Каждый оператор Python за кулисами вызывает `__dunder__`-метод.

| Оператор/функция | Метод |
|---|---|
| `a + b` | `__add__` |
| `a - b` | `__sub__` |
| `a * b` | `__mul__` |
| `x[i]` | `__getitem__` |
| `len(x)` | `__len__` |
| `str(x)` / `print` | `__str__` |
| `repr(x)` | `__repr__` |
| `x == y` | `__eq__` |
| `x < y` | `__lt__` |
| `bool(x)` | `__bool__` |
| `x in coll` | `__contains__` |
| `iter(x)` | `__iter__` |
| `call(x)` (x(...)) | `__call__` |
| `with x` | `__enter__` / `__exit__` |

### Пример — свой класс-вектор с операторами
```python
class Vec:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vec({self.x}, {self.y})"

    def __len__(self):
        return 2


v1 = Vec(1, 2)
v2 = Vec(3, 4)
print(v1 + v2)  # Vec(4, 6)   ← __add__ + __repr__
print(v1 == Vec(1, 2))  # True   ← __eq__
print(len(v1))  # 2           ← __len__
```

### `__repr__` vs `__str__`
- `__str__` — «для человека» (`print`, `str()`).
- `__repr__` — «для разработчика» (`repr()`, консоль). Желательно однозначно
  воспроизводимый (`Point(x=1, y=2)`).
- Если `__str__` нет — используется `__repr__`.

### Всё «магическое» сводится к обычным методам
Дуадеры — не волшебство, просто методы с фиксированными именами, которые интерпретатор
вызывает неявно. Понимание `__eq__` → понимаешь, как работает `==`.

---

## Шпаргалка «что запомнить»

1. `@property` — геттер и валидация на запись, без `get/set`-методов.
2. `ABC` + `@abstractmethod` — нельзя создать базу и забыть обязательные методы.
3. Миксин — дополнение поведения, наследуется вместе с основным классом.
4. `dataclass` — автоматические init/repr/eq; `frozen=True` и `default_factory`.
5. `Protocol` — статический «интерфейс по форме» для mypy.
6. Dunder-методы = операторы: `__add__` → `+`, `__eq__` → `==`, и т.д.