from copy import copy
from typing import Callable, List, Tuple, Union
from datetime import date, datetime
from sheetcake import Signal, fmt, dates, errors, Cell


class DateCell:

    def __init__(
        self,
        value = None,
        name: str = "<DateCell>",
        fmt: Callable = fmt.mmddyyyy,
        callback: Callable = None,
        locked: bool = False,
        validation_rules: List[Callable] = None
    ) -> None:
        self.operations = None
        self.validation_rules = validation_rules or []
        self.changed = Signal()
        self.name = name
        self.fmt = fmt
        self.callback = callback
        self._value = value
        self.locked = locked

        if isinstance(value, DateCell):
            self._value = value.value
            self.equal_item(value)
        elif value is not None:
            self.equal_item(value)

        self.validate()

    def __str__(self) -> str:
        return self.fmt(self._value)

    def __repr__(self) -> str:
        fmt = self.fmt.__name__
        if self.callback is not None:
            callback = self.callback.__name__
        else:
            callback = None
        validation_rules = repr(self.validation_rules)
        return f"DateCell({self._value}, name='{self.name}', fmt={fmt}, callback={callback}, locked={self.locked}, validation_rules={validation_rules})"

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

    @property
    def year(self):
        return self._value.year
    
    @property
    def month(self):
        return self._value.month

    def print(self, width: int = 15):
        result = f'{self.name:<{width}}: {self.fmt(self._value)}'
        print(result)

    def formula(self, deep: bool = False):
        if not self.operations:
            return self.name
        
        return self.operations.formula(deep=deep)

    def value_audit(self, deep: bool = False):
        if not self.operations:
            return self.fmt(self._value)
        return self.operations.value_audit(deep=deep)

    def calculate(self):
        if self.operations:
            return self.operations.value
        return self.value

    def update(self, **kwargs):
        # print(f"Cell '{self.name}' received update signal.")
        if self.locked:
            print(f"Value of locked cell {self.name} cannot be changed from {self._value}")
            return None
        new_value = self.calculate()
        # print(f"Cell '{self.name}' calculated new value {new_value}")
        initial_value = copy(self._value)
        self._value = new_value
        self.validate()
        if self.has_changed(initial_value):
            # print(f"Cell '{self.name}' changed value from {initial_value} to {self._value}.")
            self.changed.emit()
            if self.callback:
                print(f"Cell '{self.name}' calling callback with value {self._value}")
                self.callback(self._value)

    def validate(self):
        if not isinstance(self._value, date) and self._value is not None:
            raise errors.DateValidationError(f"Value of '{self.name}' must be a date, not {type(self._value)}.")
        for rule in self.validation_rules:
            result = rule(self._value)
            if not result:
                raise errors.DateValidationError(f"Value of '{self.name}' cannot be {self._value}")
        return True

    def has_changed(self, initial_value):
        if initial_value is None and self._value is not None:
            return True
        elif initial_value is not None and self._value is None:
            return True
        elif not all((
            initial_value.year == self._value.year,
            initial_value.month == self._value.month,
            initial_value.day == self._value.day
        )):
            return True
        return False

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def lock_value(self, value):
        self.value = value
        self.locked = True

    def equal_item(self, cell: "DateCell", update: bool = True):
        if hasattr(cell, 'changed'):
            cell.changed.connect(self.update)
        self.operations = EqualDateOperation(cell)
        if update:
            self.update()
        return self

    def edays_item(self, cell: "DateCell", num_days: int, update: bool = True):
        if hasattr(cell, 'changed'):
            cell.changed.connect(self.update)
        if hasattr(num_days, 'changed'):
            num_days.changed.connect(self.update)
        cell = cell or self.operations
        self.operations = EdaysDateOperation(cell, num_days)
        if update:
            self.update()
        return self

    def edate_item(self, cell: "DateCell", num_months: int, update: bool = True):
        if hasattr(cell, 'changed'):
            cell.changed.connect(self.update)
        if hasattr(num_months, 'changed'):
            num_months.changed.connect(self.update)
        cell = cell or self.operations
        self.operations = EdateDateOperation(cell, num_months)
        if update:
            self.update()
        return self

    def eomonth_item(self, cell: "DateCell", num_months: int = 0, update: bool = True):
        if hasattr(cell, 'changed'):
            cell.changed.connect(self.update)
        if hasattr(num_months, 'changed'):
            num_months.changed.connect(self.update)
        cell = cell or self.operations
        self.operations = EomonthDateOperation(cell, num_months)
        if update:
            self.update()
        return self

    def max_items(self, cells: List["DateCell"], update: bool = True):
        for cell in cells:
            if hasattr(cell, 'changed'):
                cell.changed.connect(self.update)
        if self.operations:
            cells.append(self.operations)
        self.operations = MaxDateOperation(cells)
        if update:
            self.update()
        return self

    def min_items(self, cells: List["DateCell"], update: bool = True):
        for cell in cells:
            if hasattr(cell, 'changed'):
                cell.changed.connect(self.update)
        if self.operations:
            cells.append(self.operations)
        self.operations = MinDateOperation(cells)
        if update:
            self.update()
        return self
    
    def is_after(self, other: "DateCell", inclusive: bool = False):
        if hasattr(other, "value"):
            other_date = other.value
        else:
            other_date = other
        if inclusive:
            return self.value >= other_date
        else:
            return self.value > other_date
    
    def is_before(self, other: "DateCell", inclusive: bool = False):
        if hasattr(other, "value"):
            other_date = other.value
        else:
            other_date = other
        if inclusive:
            return self.value <= other_date
        else:
            return self.value < other_date
        
    def is_between(self, start: "DateCell", end: "DateCell", incl_start: bool = False, incl_end: bool = False):
        if hasattr(start, "value"):
            start_date = start.value
        else:
            start_date = start
        if hasattr(end, "value"):
            end_date = end.value
        else:
            end_date = end
        if incl_start and incl_end:
            return start_date <= self.value <= end_date
        elif incl_start and not incl_end:
            return start_date <= self.value < end_date
        elif not incl_start and incl_end:
            return start_date < self.value <= end_date
        else:
            return start_date < self.value < end_date

    def __eq__(self, other: object) -> bool:
        if hasattr(other, "value") and self.value == other.value:
            return True
        if self.value == other:
            return True
        return False

    def __gt__(self, other: object) -> bool:
        if hasattr(other, "value"):
            return self.value > other.value
        if self.value > other:
            return True
        return False

    def __ge__(self, other: object) -> bool:
        if hasattr(other, "value"):
            return self.value >= other.value
        if self.value >= other:
            return True
        return False

    def __lt__(self, other: object) -> bool:
        if hasattr(other, "value"):
            return self.value < other.value
        if self.value < other:
            return True
        return False

    def __le__(self, other: object) -> bool:
        if hasattr(other, "value"):
            return self.value <= other.value
        if self.value <= other:
            return True
        return False

    def __sub__(self, other):
        if hasattr(other, "value"):
            return self.value - other.value
        return self.value - other

    def __rsub__(self, other):
        if hasattr(other, "value"):
            return other.value - self.value
        return other - self.value
    
    @classmethod
    def edays(
        cls,
        date_cell: "DateCell",
        num_days: Cell,
        name: str = "<DateCell>",
        fmt: Callable = fmt.mmddyyyy,
        callback: Callable = None,
        locked: bool = False,
        validation_rules: List[Callable] = None
    ) -> "DateCell":
        new_cell = cls(value=None, name=name, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
        new_cell.edays_item(cell=date_cell, num_days=num_days, update=True)
        return new_cell

    @classmethod
    def edate(
        cls,
        date_cell: "DateCell",
        num_months: int,
        name: str = "<DateCell>",
        fmt: Callable = fmt.mmddyyyy,
        callback: Callable = None,
        locked: bool = False,
        validation_rules: List[Callable] = None
    ) -> "DateCell":
        new_cell = cls(value=None, name=name, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
        new_cell.edate_item(cell=date_cell, num_months=num_months, update=True)
        return new_cell

    @classmethod
    def eomonth(
        cls,
        date_cell: "DateCell",
        num_months: int = 0,
        name: str = "<DateCell>",
        fmt: Callable = fmt.mmddyyyy,
        callback: Callable = None,
        locked: bool = False,
        validation_rules: List[Callable] = None
    ) -> "DateCell":
        new_cell = cls(value=None, name=name, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
        new_cell.eomonth_item(cell=date_cell, num_months=num_months, update=True)
        return new_cell

    @classmethod
    def max(
        cls,
        cells: List["DateCell"],
        name: str = "<DateCell>",
        fmt: Callable = fmt.mmddyyyy,
        callback: Callable = None,
        locked: bool = False,
        validation_rules: List[Callable] = None
    ) -> "DateCell":
        new_cell = cls(value=None, name=name, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
        new_cell.max_items(cells=cells, update=True)
        return new_cell

    @classmethod
    def min(
        cls,
        cells: List["DateCell"],
        name: str = "<DateCell>",
        fmt: Callable = fmt.mmddyyyy,
        callback: Callable = None,
        locked: bool = False,
        validation_rules: List[Callable] = None
    ) -> "DateCell":
        new_cell = cls(value=None, name=name, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
        new_cell.min_items(cells=cells, update=True)
        return new_cell


def get_value(obj) -> date:
    if hasattr(obj, 'value'):
        return obj.value
    else:
        return obj


class AbstractDateOperation:

    def __init__(
        self,
        fmt: Callable = fmt.mmddyyyy,
    ) -> None:
        self.fmt = fmt

    def __str__(self) -> str:
        return self.fmt(self.value)

    @property
    def value(self) -> date:
        raise NotImplementedError

    def formula(self, deep: bool = False) -> str:
        raise NotImplementedError

    def value_audit(self, deep: bool = False):
        raise NotImplementedError


class EqualDateOperation(AbstractDateOperation):

    def __init__(self, dt_item: Union[DateCell, AbstractDateOperation, date], fmt: Callable = fmt.mmddyyyy) -> None:
        super().__init__(fmt=fmt)
        self.dt_item = dt_item

    @property
    def value(self) -> date:
        start_date = get_value(self.dt_item)
        return start_date

    def formula(self, deep: bool = False):
        if deep and hasattr(self.dt_item, 'formula'):
            result = f'{self.dt_item.formula(deep=deep)}'
        elif hasattr(self.dt_item, 'name'):
            result = f'{self.dt_item.name}'
        else:
            result = f'{self.dt_item}'
        return result

    def value_audit(self, deep: bool = False):
        result = ""
        if deep and hasattr(self.dt_item, 'value_audit'):
            result = self.dt_item.value_audit()
        else:
            result = str(self.dt_item)
        return result


class EdaysDateOperation(AbstractDateOperation):

    def __init__(self, dt_item: Union[DateCell, AbstractDateOperation, date], num_days: int, fmt: Callable = fmt.mmddyyyy) -> None:
        super().__init__(fmt=fmt)
        self.dt_item = dt_item
        self.num_days = num_days

    @property
    def value(self) -> date:
        start_date = get_value(self.dt_item)
        num_days = get_value(self.num_days)
        return dates.edays(start_date=start_date, num_days=num_days)

    def formula(self, deep: bool = False):
        if deep and hasattr(self.dt_item, 'formula'):
            result = f'edays( {self.dt_item.formula(deep=deep)}, {self.num_days} )'
        elif hasattr(self.dt_item, 'name'):
            result = f'edays( {self.dt_item.name}, {self.num_days} )'
        else:
            result = f'edays( {self.dt_item}, {self.num_days} )'
        return result

    def value_audit(self, deep: bool = False):
        result = ""
        if deep and hasattr(self.dt_item, 'value_audit'):
            result = f'edays( {self.dt_item.value_audit(deep=deep)}, {self.num_days} )'
        else:
            result = f'edays( {get_value(self.dt_item)}, {self.num_days} )'
        return result


class EdateDateOperation(AbstractDateOperation):

    def __init__(self, dt_item: Union[DateCell, AbstractDateOperation, date], num_months: int, fmt: Callable = fmt.mmddyyyy) -> None:
        super().__init__(fmt=fmt)
        self.dt_item = dt_item
        self.num_months = num_months

    @property
    def value(self) -> date:
        start_date = get_value(self.dt_item)
        num_months = get_value(self.num_months)
        return dates.edate(start_date=start_date, num_months=num_months)

    def formula(self, deep: bool = False):
        if deep and hasattr(self.dt_item, 'formula'):
            result = f'edate( {self.dt_item.formula(deep=deep)}, {self.num_months} )'
        elif hasattr(self.dt_item, 'name'):
            result = f'edate( {self.dt_item.name}, {self.num_months} )'
        else:
            result = f'edate( {self.dt_item}, {self.num_months} )'
        return result

    def value_audit(self, deep: bool = False):
        result = ""
        if deep and hasattr(self.dt_item, 'value_audit'):
            result = f'edate( {self.dt_item.value_audit(deep=deep)}, {self.num_months} )'
        else:
            result = f'edate( {get_value(self.dt_item)}, {self.num_months} )'
        return result


class EomonthDateOperation(AbstractDateOperation):

    def __init__(self, dt_item: Union[DateCell, AbstractDateOperation, date], num_months: int, fmt: Callable = fmt.mmddyyyy) -> None:
        super().__init__(fmt=fmt)
        self.dt_item = dt_item
        self.num_months = num_months

    @property
    def value(self) -> date:
        start_date = get_value(self.dt_item)
        num_months = get_value(self.num_months)
        return dates.eomonth(start_date=start_date, num_months=num_months)

    def formula(self, deep: bool = False):
        if deep and hasattr(self.dt_item, 'formula'):
            result = f'eomonth( {self.dt_item.formula(deep=deep)}, {self.num_months} )'
        elif hasattr(self.dt_item, 'name'):
            result = f'eomonth( {self.dt_item.name}, {self.num_months} )'
        else:
            result = f'eomonth( {self.dt_item}, {self.num_months} )'
        return result

    def value_audit(self, deep: bool = False):
        result = ""
        if deep and hasattr(self.dt_item, 'value_audit'):
            result = f'eomonth( {self.dt_item.value_audit(deep=deep)}, {self.num_months} )'
        else:
            result = f'eomonth( {get_value(self.dt_item)}, {self.num_months} )'
        return result


class MaxDateOperation(AbstractDateOperation):

    def __init__(self, dt_list: List[Union[DateCell, AbstractDateOperation, date]], fmt: Callable = fmt.mmddyyyy) -> None:
        super().__init__(fmt=fmt)
        self.dt_list = dt_list

    @property
    def value(self) -> date:
        return max([get_value(dt) for dt in self.dt_list])

    def formula(self, deep: bool = False):
        formula_list = []
        for dt in self.dt_list:
            if deep and hasattr(dt, 'formula'):
                formula_list.append(dt.formula(deep=deep))
            elif hasattr(dt, 'name'):
                formula_list.append(dt.name)
            else:
                formula_list.append(str(dt))
        result = ', '.join(formula_list)
        return f"max( {result} )"

    def value_audit(self, deep: bool = False):
        return self.formula(deep=deep)


class MinDateOperation(AbstractDateOperation):

    def __init__(self, dt_list: List[Union[DateCell, AbstractDateOperation, date]], fmt: Callable = fmt.mmddyyyy) -> None:
        super().__init__(fmt=fmt)
        self.dt_list = dt_list

    @property
    def value(self) -> date:
        return min([get_value(dt) for dt in self.dt_list])

    def formula(self, deep: bool = False):
        formula_list = []
        for dt in self.dt_list:
            if deep and hasattr(dt, 'formula'):
                formula_list.append(dt.formula(deep=deep))
            elif hasattr(dt, 'name'):
                formula_list.append(dt.name)
            else:
                formula_list.append(str(dt))
        result = ', '.join(formula_list)
        return f"min( {result} )"

    def value_audit(self, deep: bool = False):
        return self.formula(deep=deep)
