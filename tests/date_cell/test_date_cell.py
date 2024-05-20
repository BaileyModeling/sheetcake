from sheetcake import DateCell, errors, validation_rules
from sheetcake.src.cells.date_cell import AbstractDateOperation
from datetime import date
import pytest
from typing import List
from types import SimpleNamespace


class CallbackClass:
    variable = None
    def callback(self, value):
        self.variable = value


def test_date_cell_str():
    a = DateCell(date(2024, 3, 1))
    assert str(a) == "03/01/2024"


def test_date_cell_locked():
    a = DateCell(date(2024, 3, 1), locked=True)
    a.value = date(2024, 12, 1)
    assert a.value == date(2024, 3, 1)


def test_date_cell_formula_locked():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, "b")
    b.lock()
    a.value = date(2024, 12, 1)
    assert b.value == date(2024, 3, 1)


def test_date_cell_repr():
    test_object = CallbackClass()
    a = DateCell(None, "name", callback=test_object.callback)
    assert repr(a) == "DateCell(None, name='name', fmt=mmddyyyy, callback=callback, locked=False, validation_rules=[])"


def test_date_cell_repr_no_callback():
    a = DateCell(None, "name")
    assert repr(a) == "DateCell(None, name='name', fmt=mmddyyyy, callback=None, locked=False, validation_rules=[])"


def test_date_cell_print():
    a = DateCell()
    a.print()
    assert True


def test_date_cell_formula_no_operations():
    a = DateCell(None, "name")
    assert a.formula() == "name"


def test_cell_integer_value_raises_error():
    with pytest.raises(errors.DateValidationError):
        a = DateCell(5, "name")


def test_date_cell_value():
    cell = DateCell(value=date(2024, 3, 1), name="Test Date")
    cell.value = date(2024, 12, 1)
    assert cell == date(2024, 12, 1)


def test_date_cell_equal_init():
    a = DateCell(value=date(2024, 3, 1), name="Test Date 1")
    b = DateCell(value=a, name="Test Date 2")
    assert b == date(2024, 3, 1)


def test_date_cell_equal_method():
    a = DateCell(value=date(2024, 3, 1), name="Test Date 1")
    b = DateCell(name="Test Date 2")
    b.equal_item(a)
    assert b == date(2024, 3, 1)


def test_date_cell_equal_method_updates():
    a = DateCell(value=date(2024, 3, 1), name="Test Date 1")
    b = DateCell(name="Test Date 2")
    b.equal_item(a)
    a.value = date(2024, 12, 1)
    assert b == date(2024, 12, 1)


def test_date_cell_init_with_another_cell_updates():
    a = DateCell(date(2024, 3, 1))
    b = DateCell(a)
    a.value = date(2024, 12, 1)
    assert b.value == date(2024, 12, 1)

def test_date_cell_changed_to_none():
    test_object = CallbackClass()
    test_object.variable = date(2024, 3, 1)
    a = DateCell(date(2024, 3, 1), "name", callback=test_object.callback)
    a.value = None
    assert test_object.variable is None


def test_date_cell_not_equal():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(date(2024, 2, 1), "b")
    assert a != b


def test_date_cell_unlock():
    a = DateCell(date(2024, 3, 1), "a")
    a.lock()
    a.value = date(2024, 12, 1)
    assert a.value == date(2024, 3, 1)
    a.unlock()
    a.value = date(2024, 12, 1)
    assert a.value == date(2024, 12, 1)


def test_date_cell_lock_value():
    a = DateCell(date(2024, 3, 1), "a")
    a.lock_value(date(2024, 12, 1))
    a.value = date(2024, 1, 1)
    assert a.value == date(2024, 12, 1)


def test_date_cell_validateion_rule():
    rule = validation_rules.LessThanOrEqualDate(date(2024, 12, 31))
    a = DateCell(date(2024, 2, 1), "a", validation_rules=[rule.validate])
    with pytest.raises(errors.DateValidationError):
        a.value = date(2025, 1, 1)


def test_date_cell_str_equal_date():
    a = DateCell(date(2024, 3, 1), "a")
    assert str(a) == "03/01/2024"


def test_date_cell_formula_equal_date():
    a = DateCell(date(2024, 3, 1), "a")
    assert a.formula() == "2024-03-01"


def test_date_cell_formula_equal_date_cell():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, "b")
    c = DateCell(b, "c")
    assert c.formula() == "b"


def test_date_cell_formula_equal_date_cell_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, "b")
    c = DateCell(b, "c")
    assert c.formula(deep=True) == "2024-03-01"


def test_date_cell_calculate_blank_cell():
    a = DateCell(None, "a")
    assert a.calculate() is None


def test_abstract_date_operation_value_raises_error():
    obj = AbstractDateOperation()
    with pytest.raises(NotImplementedError):
        obj.value


def test_abstract_date_operation_formula_raises_error():
    obj = AbstractDateOperation()
    with pytest.raises(NotImplementedError):
        obj.formula()


def test_abstract_date_operation_value_audit_raises_error():
    obj = AbstractDateOperation()
    with pytest.raises(NotImplementedError):
        obj.value_audit()


def test_date_cell_formula_eomonth_edays():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.eomonth_item(a, 0)
    b.edays_item(None, 5)
    assert b.formula() == "edays( 03/31/2024, 5 )"


def test_date_cell_formula_deep_eomonth_edays():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.eomonth_item(a, 0)
    b.edays_item(None, 5)
    assert b.formula(deep=True) == "edays( eomonth( 2024-03-01, 0 ), 5 )"


def test_date_cell_edate_max_combined_value():
    a = DateCell(name="a")
    a.edate_item(date(2028, 1, 1), 12)
    b = DateCell(date(2025, 1, 1), name="b")
    c = DateCell(date(2026, 1, 1), name="c")
    d = DateCell(date(2027, 1, 1), name="d")
    a.max_items([b, c, d])
    assert a.value == date(2029, 1, 1)


def test_date_cell_edate_max_combined_formula():
    a = DateCell(name="a")
    a.edate_item(date(2028, 1, 1), 12)
    b = DateCell(date(2025, 1, 1), name="b")
    c = DateCell(date(2026, 1, 1), name="c")
    d = DateCell(date(2027, 1, 1), name="d")
    a.max_items([b, c, d])
    assert a.formula() == "max( b, c, d, 01/01/2029 )"


def test_date_cell_edate_max_combined_formula_deep():
    a = DateCell(name="a")
    a.edate_item(date(2028, 1, 1), 12)
    b = DateCell(date(2025, 1, 1), name="b")
    c = DateCell(date(2026, 1, 1), name="c")
    d = DateCell(date(2027, 1, 1), name="d")
    a.max_items([b, c, d])
    assert a.formula(deep=True) == "max( 2025-01-01, 2026-01-01, 2027-01-01, edate( 2028-01-01, 12 ) )"


def test_date_cell_value_audit_equal_date_cell():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, "b")
    c = DateCell(b, "c")
    assert c.value_audit() == "03/01/2024"


def test_date_cell_value_audit_equal_date_cell_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, "b")
    c = DateCell(b, "c")
    assert c.value_audit(deep=True) == "03/01/2024"


def test_date_cell_empty_value_audit():
    a = DateCell(None, "a")
    assert a.value_audit() == ""


def test_date_cell_subtract_date_cell():
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(date(2024, 2, 1), "b")
    result = b - a
    assert result.days == 31


def test_date_cell_subtract_date():
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(date(2024, 2, 1), "b")
    result = b - a.value
    assert result.days == 31


def test_date_subtract_date_cell():
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(date(2024, 2, 1), "b")
    result = b.value - a
    assert result.days == 31


def test_object_subtract_date_cell():
    a = DateCell(date(2024, 1, 1), "a")
    b = SimpleNamespace(value=date(2024, 2, 1))
    result = b - a
    assert result.days == 31


def test_date_cell_year():
    a = DateCell(date(2024, 1, 1), "a")
    assert a.year == 2024


def test_date_cell_month():
    a = DateCell(date(2024, 1, 1), "a")
    assert a.month == 1
