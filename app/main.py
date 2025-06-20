from abc import ABC, abstractmethod
from typing import Any, Optional, Type, Sequence


class Validator(ABC):
    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, obj: Type[Any],
                objtype: Optional[Type[Any]] = None) -> int:
        value = getattr(obj, self.protected_name, None)
        return value

    def __set__(self, obj: Type[Any], value: int) -> None:
        if self.validate(value):
            setattr(obj, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> bool:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> bool:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value} and greater than "
                             f"{self.max_value}.")
        return True


class OneOf(Validator):
    def __init__(self, options: Sequence[str]) -> None:
        self.options = tuple(options)

    def validate(self, value: Any) -> bool:
        if not (value in self.options):
            raise ValueError(f"Expected {value} to be one of {self.options}.")
        return True


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(["ketchup", "mayo", "burger"])

    def __init__(self, buns: int,
                 cheese: int,
                 tomatoes: int,
                 cutlets: int,
                 eggs: int,
                 sauce: str )-> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
