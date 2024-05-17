from typing import Callable, List, Tuple, Dict
from decimal import Decimal
from sheetcake import Signal, fmt
from sheetcake.src.utils import is_number, get_value


class Cell:

    def __init__(
        self,
        value = None,
        name: str = "<Cell>",
        tolerance = 0.0,
        fmt: Callable = fmt.comma2,
        callback: Callable = None,
        locked: bool = False,
        validation_rules: List[Callable] = None,
        meta_data: Dict = None,
    ) -> None:
        """
        callback: callback function to update GUI upon change
        """
        self.operations: List[Tuple[str, Cell]] = []
        self.validation_rules = validation_rules or []
        self.changed = Signal()
        self.name = name
        self.tolerance = tolerance
        self.fmt = fmt
        self.callback = callback
        self._value = value
        self.locked = locked
        self.meta_data = meta_data or {}

        if isinstance(value, Cell):
            self._value = value.value
            self.equal_item(value)
        elif value is not None:
            self.equal_item(value)

        self.validate()

    def __str__(self) -> str:
        return self.fmt(self._value)

    def __repr__(self) -> str:
        fmt = self.fmt.__name__
        if self.callback is not None and hasattr(self.callback, '__name__'):
            callback = self.callback.__name__
        else:
            callback = None
        validation_rules = repr(self.validation_rules)
        return f"Cell({self._value}, name='{self.name}', tolerance={self.tolerance}, fmt={fmt}, callback={callback}, locked={self.locked}, validation_rules={validation_rules}, meta_data={repr(self.meta_data)})"

    def print(self, width: int = 15):
        result = f'{self.name:<{width}}: {self.fmt(self._value)}'
        print(result)

    def formula(self, deep: bool = False):
        if not self.operations:
            return self.name
        elif len(self.operations) == 1 and self.operations[0][0] == "=" and is_number(self.operations[0][1]):
            return self.name

        result = ""
        for operation, arg in self.operations:
            if result:
                result += f' {operation} '

            if deep and hasattr(arg, 'formula'):
                result += arg.formula(deep=deep)
            elif hasattr(arg, 'name'):
                result += arg.name
            else:
                result += str(arg)
        if len(self.operations) > 1:
            result = f"( {result} )"
        return result

    def value_audit(self, deep: bool = False):
        if not self.operations:
            return self.fmt(self._value)

        result = ""
        for operation, arg in self.operations:
            if result:
                result += f' {operation} '

            if deep and hasattr(arg, 'value_audit'):
                result += arg.value_audit()
            else:
                result += str(arg)
        if len(self.operations) > 1:
            result = f"( {result} )"
        return result

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # print(f"Setting value of '{self.name}' to {value}")
        if self.locked:
            print(f"Cannot change value of locked cell {self.name} to {value}")
            return None
        self.equal_item(value)

    def calculate(self):
        """
        Override this method to implement custom calculations
        """
        cumulative = None
        for operation, cell in self.operations:
            if operation == "=":
                cumulative = add_item(cumulative, cell)
            elif operation == "+":
                cumulative = add_item(cumulative, cell)
            elif operation == "-":
                cumulative = sub_item(cumulative, cell)
            elif operation == "*":
                cumulative = mult_item(cumulative, cell)
            elif operation == "/":
                cumulative = div_item(cumulative, cell)
            elif operation == "//":
                cumulative = floordiv_item(cumulative, cell)
            elif operation == "^":
                cumulative = exp_item(cumulative, cell)
        return cumulative

    def update(self, **kwargs):
        # print(f"Cell '{self.name}' received update signal.")
        if self.locked:
            print(f"Value of locked cell {self.name} cannot be changed from {self._value}")
            return None
        new_value = self.calculate()
        initial_value = self._value
        self._value = new_value
        self.validate()
        if self.has_changed(initial_value):
            # print(f"Cell '{self.name}' changed value from {initial_value} to {self._value}.")
            self.changed.emit(value=self._value)
            if self.callback:
                # print(f"Cell '{self.name}' calling callback with value {self._value}")
                self.callback(self._value)

    def validate(self):
        for rule in self.validation_rules:
            result = rule(self._value)
            if not result:
                raise ValueError(f"Value of '{self.name}' cannot be {self._value}")
        return True

    def has_changed(self, initial_value):
        if initial_value == self._value:
            return False
        elif initial_value is None and self._value is not None:
            return True
        elif initial_value is not None and self._value is None:
            return True
        elif abs(initial_value - self._value) > self.tolerance:
            return True
        return False

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def lock_value(self, value):
        self.value = value
        self.locked = True

    def equal_item(self, cell: "Cell", update: bool = True):
        if hasattr(cell, 'changed'):
            cell.changed.connect(self.update)
        self.operations = [("=", cell)]  # override any previous operations
        if update:
            self.update()
        return self

    def add_item(self, cell: "Cell", update: bool = True):
        if hasattr(cell, 'changed'):
            cell.changed.connect(self.update)
        self.operations.append(("+", cell))
        if update:
            self.update()
        return self

    def sum_items(self, *args):
        for arg in args:
            self.add_item(arg, update=False)
        self.update()
        return self

    def sub_item(self, cell: "Cell", update: bool = True):
        if hasattr(cell, 'changed'):
            cell.changed.connect(self.update)
        self.operations.append(("-", cell))
        if update:
            self.update()
        return self

    def mult_item(self, cell: "Cell", update: bool = True):
        if hasattr(cell, 'changed'):
            cell.changed.connect(self.update)
        self.operations.append(("*", cell))
        if update:
            self.update()
        return self

    def div_item(self, cell: "Cell", update: bool = True):
        if hasattr(cell, 'changed'):
            cell.changed.connect(self.update)
        self.operations.append(("/", cell))
        if update:
            self.update()
        return self
    
    def floordiv_item(self, cell: "Cell", update: bool = True):
        if hasattr(cell, 'changed'):
            cell.changed.connect(self.update)
        self.operations.append(("//", cell))
        if update:
            self.update()
        return self
    
    def exp_item(self, cell: "Cell", update: bool = True):
        if hasattr(cell, 'changed'):
            cell.changed.connect(self.update)
        self.operations.append(("^", cell))
        if update:
            self.update()
        return self

    @classmethod
    def sum(cls, cells: List["Cell"], name: str = "<Cell>", tolerance: float = 0, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Cell":
        cell = Cell(None, name=name, tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
        for c in cells:
            cell.add_item(c, update=False)
        cell.update()
        return cell

    @classmethod
    def mult(cls, cells: List["Cell"], name: str = "<Cell>", tolerance: float = 0, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Cell":
        cell = Cell(None, name=name, tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
        for c in cells:
            cell.mult_item(c, update=False)
        cell.update()
        return cell

    @classmethod
    def div(cls, dividend: "Cell", divisor: "Cell", name: str = "<Cell>", tolerance: float = 0, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Cell":
        cell = Cell(dividend, name=name, tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
        return cell.div_item(divisor)

    @classmethod
    def sub(cls, minuend: "Cell", subtrahend: "Cell", name: str = "<Cell>", tolerance: float = 0, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Cell":
        cell = Cell(minuend, name=name, tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
        return cell.sub_item(subtrahend)

    def __add__(self, other):
        if hasattr(other, "array"):
            return other + self
        cell = Cell()
        cell.equal_item(self)
        cell.add_item(other)
        return cell

    def __radd__(self, other):
        if other == 0:
            return self
        return self.__add__(other)

    def __sub__(self, other):
        # cannot import Array to test using isinstance
        if hasattr(other, "array"):
            return -other + self
        cell = Cell()
        cell.equal_item(self)
        cell.sub_item(other)
        return cell

    def __rsub__(self, other):
        cell = Cell()
        cell.equal_item(other)
        cell.sub_item(self)
        return cell

    def __mul__(self, other):
        if hasattr(other, "array"):
            return other * self
        cell = Cell()
        cell.equal_item(self)
        cell.mult_item(other)
        return cell

    __rmul__ = __mul__

    def __div__(self, other):
        if hasattr(other, "array"):
            return (1 / other) * self
        cell = Cell()
        cell.equal_item(self)
        cell.div_item(other)
        return cell

    def __rdiv__(self, other):
        cell = Cell()
        cell.equal_item(other)
        cell.div_item(self)
        return cell

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __floordiv__(self, other):
        cell = Cell()
        cell.equal_item(self)
        cell.floordiv_item(other)
        return cell
    
    def __rfloordiv__(self, other):
        cell = Cell()
        cell.equal_item(other)
        cell.floordiv_item(self)
        return cell
    
    def __pow__(self, other):
        cell = Cell()
        cell.equal_item(self)
        cell.exp_item(other)
        return cell

    def __neg__(self):
        cell = Cell(self, f"-{self.name}", fmt=self.fmt)
        cell.mult_item(Cell(-1, name="-1"))
        return cell

    def __round__(self, n=0):
        # TODO: return a cell or just a value?
        return round(self.value, n)

    '''
    def __mod__(self, other):
    '''

    def __abs__(self):
        return abs(self.value)

    def __lt__(self, other):
        return self.value < get_value(other)

    def __le__(self, other):
        return self.value <= get_value(other)

    def __eq__(self, other):
        return self.value == get_value(other)

    def __ne__(self, other):
        return self.value != get_value(other)

    def __gt__(self, other):
        return self.value > get_value(other)

    def __ge__(self, other):
        return self.value >= get_value(other)
    
    def __format__(self, fmt: str):
        return f"{self.value:{fmt}}"


# =============================================================================
# MATH OPERATIONS
# =============================================================================

def add_item(cumulative, item):
    item_value = get_value(item, default=0)
    if item_value is not None:
        if cumulative is None:
            cumulative = item_value
        else:
            cumulative += item_value
    return cumulative


def sub_item(cumulative, item):
    item_value = get_value(item, default=0)
    if item_value:
        if cumulative is None:
            cumulative = -item_value
        else:
            cumulative -= item_value
    return cumulative


def mult_item(cumulative, item):
    item_value = get_value(item, default=None)
    if item_value is not None:
        if cumulative is None:
            cumulative = item_value
        else:
            cumulative *= item_value
    return cumulative


def div_item(cumulative, item):
    if cumulative is None:
        return None
    item_value = get_value(item, default=None)
    if item_value is None:
        return None
    if item_value == 0:
        raise ZeroDivisionError
    return cumulative / item_value


def floordiv_item(cumulative, item):
    if cumulative is None:
        return None
    item_value = get_value(item, default=None)
    if item_value is None:
        return None
    if item_value == 0:
        raise ZeroDivisionError
    return cumulative // item_value


def exp_item(cumulative, item):
    item_value = get_value(item, default=None)
    if item_value is not None:
        if cumulative is None:
            cumulative = item_value
        else:
            cumulative **= item_value
    return cumulative
