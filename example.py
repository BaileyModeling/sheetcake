from sheetcake2 import Cell, MaxCell, RoundCell
from typing import List


# cell = Cell(1, "Name")
# print(cell)
a = Cell(2, "a")
b = Cell(3, "b")
d = Cell(4, "d")
e = Cell(5, "e")
# c = a + b
# c = Cell(None, "c").sum(a, b)
# a.value = 10
# c.equal(a)
# c.add(b)

# result = b * (10 * a)
# result = Cell(0, "result")
# result = result.equal(b).mult(10 * a)
# result = 10 * a
# result.sum(a, b, d, e)

# result.sum(a, b, d)
# result.mult(e)

# print(result.formula)
# print(result)

"""
class CustomCell(Cell):
    def __init__(self, a: Cell, b: Cell, d: Cell, e: Cell):
        super().__init__(value = None, name = "CustomCell")
        self.a = a
        self.b = b
        self.d = d
        self.e = e
        for cell in [a, b, d, e]:
            cell.changed.connect(self.update)
        self.update()

    @property
    def formula(self):
        return "( a + b + d ) * e"
    
    def calculate(self):
        return (self.a.value + self.b.value + self.d.value) * self.e.value


result = CustomCell(a, b, d, e)
e.value = 10
print(result.formula)
print(result)

result = MaxCell([a, b, d, e])
a.value = 100
print(result.formula)
print(result)

rnd = RoundCell(1.23456, 2, "rnd")
# print(rnd.operations)
print(rnd)
rnd.print()
print(rnd.formula())

print("="*80)
a = Cell(1.23456, "a")
rnd = RoundCell(a, 2, "rnd")
print(rnd)
rnd.print()
print(rnd.formula())
"""

# from sheetcake2 import Array
# import numpy as np

# a = Array.from_values(values=(4, 9, 16), name='a')
# b = np.array((2, 3, 4))
# c = a / b
# print(type(c))
# c = b / a
# print(type(c))


empty = Cell()
five = Cell(5)
c = five // empty
