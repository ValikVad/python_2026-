"""Запускаемые примеры к разделу 1.5–1.9 теории ООП в Python.

Запуск:  uv run python ооп-примеры.py
Сначала подумай, что выведется, потом запусти и сверься.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, replace
from typing import Protocol


def header(t: str) -> None:
    print(f"\n=== {t} ===")


# --- 1.5 property --------------------------------------------------------
header("1.5 @property")


class Temperature:
    def __init__(self, c: float = 0.0) -> None:
        self._c = c

    @property
    def celsius(self) -> float:
        return self._c

    @celsius.setter
    def celsius(self, v: float) -> None:
        if v < -273.15:
            raise ValueError("ниже абсолютного нуля!")
        self._c = v


t = Temperature()
t.celsius = 25
print("t.celsius =", t.celsius)
try:
    t.celsius = -300
except ValueError as e:
    print("поймали ValueError:", e)


# --- 1.6 ABC и миксины ---------------------------------------------------
header("1.6 ABC + миксин")


class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...


class Square(Shape):
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side**2

    def perimeter(self) -> float:
        return 4 * self.side


class SerializableMixin:
    def to_dict(self) -> dict[str, object]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


class User(SerializableMixin):
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


sq = Square(4)
print("Square(4).area() =", sq.area())
print("User.to_dict() =", User("Аня", 20).to_dict())
try:
    Shape()  # type: ignore[abstract]  # намеренно: ABC нельзя инстанцировать
except TypeError as e:
    print("Shape() не создать:", str(e)[:40], "...")


# --- 1.7 dataclass -------------------------------------------------------
header("1.7 dataclass")


@dataclass(frozen=True)
class Point:
    x: float
    y: float = 0.0


@dataclass
class Inventory:
    name: str
    items: list[str] = field(default_factory=list)


p = Point(1.0, 2.0)
print("Point repr:", p)
print("Point == копия:", p == Point(1.0, 2.0))
print("asdict:", asdict(p))
print("replace:", replace(p, x=99.0))
try:
    p.x = 5.0  # type: ignore[misc]  # намеренно: frozen нельзя мутировать
except Exception as e:
    print("frozen нельзя мутировать:", type(e).__name__)

inv = Inventory("склад")
inv.items.append("молоток")
print("Inventory.items:", inv.items)


# --- 1.8 Protocol --------------------------------------------------------
header("1.8 Protocol")


class Named(Protocol):
    name: str

    def greet(self) -> str: ...


def hello(x: Named) -> str:
    return f"Привет, {x.name}: {x.greet()}"


class Dog:
    name = "Шарик"

    def greet(self) -> str:
        return "Гав!"


class Robot:
    name = "R2D2"

    def greet(self) -> str:
        return "beep"


print(hello(Dog()))
print(hello(Robot()))


# --- 1.9 магические методы ------------------------------------------------
header("1.9 __dunder__")


class Vec:
    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y

    def __add__(self, other: Vec) -> Vec:
        return Vec(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __len__(self) -> int:
        return 2

    def __repr__(self) -> str:
        return f"Vec({self.x}, {self.y})"


v1, v2 = Vec(1, 2), Vec(3, 4)
print("v1 + v2 =", v1 + v2)
print("v1 == Vec(1,2):", v1 == Vec(1, 2))
print("len(v1):", len(v1))
