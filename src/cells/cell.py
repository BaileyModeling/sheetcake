from sheetcake.src.signal import Signal
from sheetcake.src.utils import get_value, is_number


class Cell:

    def __init__(self, value=None, name=None, fmt=None) -> None:
        if isinstance(value, Cell):
            self._value = get_value(value)
            # value.changed.connect(self.update)
        else:
            self._value = value
        self.fmt = fmt
        self.name = name
        self.changed = Signal()
        self.operations = []
        if value is not None:
            self.add(value)

    def __repr__(self):
        '''Returns representation of the object'''
        if self.fmt is not None:
            fmt = self.fmt.__name__
        else:
            fmt = self.fmt
        cls_name = self.__class__.__name__
        return f"{cls_name}({self._value}, {self.name}, {fmt})"

    def __str__(self) -> str:
        formatter = str
        if self.fmt is not None:
            formatter = self.fmt
        return formatter(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        initial_value = self._value
        self._value = value
        if not initial_value == self._value:
            # print("emitting signal")
            self.changed.emit()

    @property
    def formula(self):
        result = ""
        for operation, arg in self.operations:
            if result:
                result += f' {operation} '
            if hasattr(arg, 'name') and arg.name:
                result += arg.name
            else:
                result += str(arg)
        return result

    @property
    def formula_audit(self):
        result = ""
        for operation, arg in self.operations:
            if result:
                result += f' {operation} '
            if hasattr(arg, 'formula_audit'):
                result += f"[ {arg.formula_audit} ]"
            elif hasattr(arg, 'name') and arg.name is None:
                result += "<anonymous>"
            elif hasattr(arg, "name"):
                result += arg.name
            else:
                result += str(arg)
        return result

    def print(self):
        if self.name is not None:
            result = f'{self.name}: '
        else:
            result = ''

        if self.fmt is not None:
            result += self.fmt(self._value)
        else:
            result += str(self._value)
        print(result)

    def update(self):
        cumulative = None
        for row in self.operations:
            if row[0] == "=":
                cumulative = add_item(cumulative, row[1])
            elif row[0] == "+":
                cumulative = add_item(cumulative, row[1])
            elif row[0] == "-":
                cumulative = sub_item(cumulative, row[1])
            elif row[0] == "*":
                cumulative = mult_item(cumulative, row[1])
            elif row[0] == "/":
                cumulative = div_item(cumulative, row[1])
            elif row[0] == "//":
                cumulative = floordiv_item(cumulative, row[1])
        self.value = cumulative

    def sum(self, *args):
        value = 0
        for arg in args:
            value += self.add(arg) or 0
        return value

    def equal(self, item):
        if hasattr(item, 'changed'):
            item.changed.connect(self.update)
        self.operations.append(("=", item))
        self.update()
        return self.value

    def add(self, item):
        if hasattr(item, 'changed'):
            item.changed.connect(self.update)
        self.operations.append(("+", item))
        self.update()
        return self.value

    def sub(self, item):
        if hasattr(item, 'changed'):
            item.changed.connect(self.update)
        self.operations.append(("-", item))
        self.update()
        return self.value

    def mult(self, item):
        if hasattr(item, 'changed'):
            item.changed.connect(self.update)
        self.operations.append(("*", item))
        self.update()
        return self.value

    def div(self, item):
        if hasattr(item, 'changed'):
            item.changed.connect(self.update)
        self.operations.append(("/", item))
        self.update()
        return self.value

    def __add__(self, other):
        if hasattr(other, "array"):
            return other + self
        cell = Cell()
        cell.add(self)
        cell.add(other)
        # print("self: ", repr(self))
        # print("other: ", repr(other))
        return cell

    __radd__ = __add__

    def __sub__(self, other):
        # cannot import Array to test using isinstance
        if hasattr(other, "array"):
            # breakpoint()
            return -other + self
        cell = Cell()
        cell.add(self)
        cell.sub(other)
        return cell

    def __rsub__(self, other):
        cell = Cell()
        cell.add(other)
        cell.sub(self)
        return cell

    def __mul__(self, other):
        # breakpoint()
        if hasattr(other, "array"):
            return other * self
        cell = Cell()
        cell.equal(self)
        cell.mult(other)
        return cell

    __rmul__ = __mul__

    def __div__(self, other):
        if hasattr(other, "array"):
            return (1 / other) * self
        cell = Cell()
        cell.equal(self)
        cell.div(other)
        return cell

    def __rdiv__(self, other):
        cell = Cell()
        cell.equal(other)
        cell.div(self)
        return cell

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __neg__(self):
        cell = Cell(-1, self.name, self.fmt)
        cell.mult(self)
        return cell

    def __round__(self, n=0):
        return round(self.value, n)

    def __eq__(self, other: object) -> bool:
        if hasattr(other, "value") and self.value == other.value:
            return True
        if self.value == other:
            return True
        return False

    '''
    def __mod__(self, other):
    def __floordiv__(self, other):
    def __pow__(self, other):
    def __abs__(self):
    '''


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
    item_value = get_value(item, default=0)
    if item_value:
        if cumulative is None:
            cumulative = item_value
        else:
            cumulative *= item_value
    return cumulative


def div_item(cumulative, item):
    item_value = get_value(item, default=0)
    print(f"{cumulative=}")
    print(f"{item=}")
    print(f"{item_value=}")
    if item_value == 0:
        raise ZeroDivisionError
    elif item_value:
        if cumulative is None:
            cumulative = 0
        else:
            cumulative = cumulative / item_value
    return cumulative


def floordiv_item(cumulative, item):
    item_value = get_value(item, default=0)
    if item_value:
        if cumulative is None:
            cumulative = item_value
        else:
            cumulative = cumulative // item_value
    return cumulative


if __name__=="__main__":
    # a = Cell(5, "a")
    # b = Cell(3, "b")
    # c = 2* (a + b)
    # c.print()
    # print(c.operations)
    # print(c.formula)
    # print(c.formula_audit)
    f = Cell(0)
    print(f._value)
