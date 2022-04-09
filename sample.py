from sheetcake import Cell, Array, zeros
from sheetcake.src.arrays.array import array_sum


def accounting(amount, pennies=True, symbol=False, width=14):
    """accounting format default: (1,234,567.89)"""
    sym = "$" if symbol else ""
    digits = 2 if pennies else 0
    if amount < 0:
        output_string = sym + "({:>" + str(width) + ",." + str(digits) + "f})"
        return output_string.format(-1 * amount)
    else:
        output_string = sym + " {:>" + str(width) + ",." + str(digits) + "f} "
        return output_string.format(amount)


duration = 3
rev = zeros(duration, name="Rev", fmt=accounting)
exp = zeros(duration, name="Exp", fmt=accounting)

# Method 1: use + operator
# noi = rev + exp
# noi.name = "NOI"

# Method 2: use array_sum()
noi = array_sum((rev, exp), "NOI", accounting)
rev.set_values((100, 200, 300))
exp.set_values((-50, -50, -50))
noi.print()

cell = noi[2]
# print(repr(cell))
# print(cell.formula)
# print(cell.formula_audit)
# for ops in cell.operations:
#     print(ops, " | ", ops[1].name)
ops = cell.operations[0]
print("Formula: ", ops[1].formula)

a = Cell(5, "a")
b = Cell(3, "b")
# c = a + b
c = sum((a, b))
c.name = "Cell C"
print(repr(c))
c.print()
print("c.operations: ", c.operations)
print("c.formula: ", c.formula)
print("c.formula_audit: ", c.formula_audit)
