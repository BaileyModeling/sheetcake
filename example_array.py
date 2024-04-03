from sheetcake import Cell, Array, fmt

# array = Array.from_values([1000, 2000, 3000, 400000], "Array", fmt=fmt.accounting)

a = Array.from_values([1, 2, 3, 4], "a", fmt=fmt.accounting)
b = Array.from_values([10, 20, 30, 40], "b", fmt=fmt.accounting)
# c = Array.from_values([100, 200, 300, 400], "c", fmt=fmt.accounting)
x = Array.from_values([50, 100, 150, 200], "x", fmt=fmt.accounting)
y = Array.from_values([50, 100, 150, 200], "y", fmt=fmt.accounting)
c = Array.sum([x, y], "c", fmt=fmt.accounting)

array = Array.sum([a, b, c], "Array Sum", fmt=fmt.accounting)
array.print()
print("="*80)
array.print_cells()
print("="*80)
array.print_row()
print("="*80)
array.print_formulas(deep=True)
print("="*80)
array.print_value_audit(deep=True)
