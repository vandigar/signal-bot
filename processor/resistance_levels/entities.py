from pydantic import BaseModel
from enum import Enum
from datetime import date

class LevelType(Enum):
    MAX = "Max"
    MIN = "Min"

class ComplexLevel(BaseModel):
    min: float
    mid: float
    max: float
    weight: int = 0

    def print(self, symbol):
        print(f"{symbol} level = [min = {self.min:.2f}, mid = {self.mid:.2f}, max = {self.max:2f}, weight = {self.weight}]")


# TODO: разобраться как сделать через getattr и setattr.
def group_level_copy(getter_obj: ComplexLevel, setter_obj: ComplexLevel):
    getter_obj.mid = setter_obj.mid
    getter_obj.max = setter_obj.max
    getter_obj.min = setter_obj.min


class SimpleLevel(BaseModel):
    price: float
    type: LevelType
    date: str
    comment: str = ""

    def is_equal(self, simple_level):
        return self.price == simple_level.price

