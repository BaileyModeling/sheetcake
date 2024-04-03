from sheetcake import DateCell, errors, validation_rules
from sheetcake.src.cells.date_cell import edays_cell, edate_cell, eomonth_cell, max_date_cell, min_date_cell, AbstractDateOperation
from datetime import date
import pytest
from typing import List
from types import SimpleNamespace


@pytest.fixture
def cell_list() -> List[DateCell]:
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(date(2025, 1, 1), "b")
    c = DateCell(date(2026, 1, 1), "c")
    d = DateCell(date(2027, 1, 1), "d")
    return [a, b, c, d]


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


def test_date_cell_eq_date():
    cell = DateCell(value=date(2024, 3, 1), name="Test Date")
    assert cell == date(2024, 3, 1)


def test_date_cell_eq_date_cell():
    a = DateCell(value=date(2024, 3, 1), name="Test Date 1")
    b = DateCell(value=date(2024, 3, 1), name="Test Date 2")
    assert a == b


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
    b.equal(a)
    assert b == date(2024, 3, 1)


def test_date_cell_equal_method_updates():
    a = DateCell(value=date(2024, 3, 1), name="Test Date 1")
    b = DateCell(name="Test Date 2")
    b.equal(a)
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


def test_date_cell_edays_operation():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edays(a, 5)
    assert b.value == date(2024, 3, 6)


def test_date_cell_edays_operation_consecutive():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edays(a, 5)
    b.edays(None, 5)
    assert b.value == date(2024, 3, 11)


def test_edays_cell():
    a = DateCell(date(2024, 3, 1), "a")
    b = edays_cell(a, 5, name="b")
    a.value = date(2024, 12, 1)
    assert b.value == date(2024, 12, 6)


def test_date_cell_edate_operation():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edate(a, 5)
    assert b.value == date(2024, 8, 1)


def test_edate_cell():
    a = DateCell(date(2024, 3, 1), "a")
    b = edate_cell(a, 5, name="b")
    assert b.value == date(2024, 8, 1)


def test_date_cell_edate_operation_updates():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edate(a, 5)
    a.value = date(2024, 1, 1)
    assert b.value == date(2024, 6, 1)


def test_date_cell_edate_operation_consecutive():
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(name="b")
    b.edate(a, 5)
    b.edate(None, 5)
    assert b.value == date(2024, 11, 1)


def test_date_cell_eomonth_operation():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.eomonth(a, 5)
    assert b.value == date(2024, 8, 31)


def test_eomonth_cell():
    a = DateCell(date(2024, 3, 1), "a")
    b = eomonth_cell(a, 5, name="b")
    assert b.value == date(2024, 8, 31)


def test_date_cell_eomonth_operation_updates():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.eomonth(a, 5)
    a.value = date(2024, 1, 1)
    assert b.value == date(2024, 6, 30)


def test_date_cell_eomonth_operation_consecutive():
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(name="b")
    b.eomonth(a, 5)
    b.eomonth(None, 5)
    assert b.value == date(2024, 11, 30)


def test_date_cell_max_operation():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell(name="d")
    d.max([a, b, c])
    assert d.value == date(2025, 1, 1)


def test_max_date_cell():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = max_date_cell([a, b, c], name="d")
    assert d.value == date(2025, 1, 1)


def test_date_cell_max_operation_updates():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell(name="d")
    d.max([a, b, c])
    a.value = date(2030, 1, 1)
    assert d.value == date(2030, 1, 1)


def test_date_cell_max_operation_consecutive():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell(date(2026, 1, 1), "d")
    f = DateCell(date(2027, 1, 1), "f")
    g = DateCell(name="g")
    g.max([a, b, c])
    g.max([d, f])
    assert g.value == date(2027, 1, 1)


def test_date_cell_min_operation():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell(name="d")
    d.min([a, b, c])
    assert d.value == date(2000, 1, 1)


def test_min_date_cell():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = min_date_cell([a, b, c], name="d")
    assert d.value == date(2000, 1, 1)


def test_date_cell_min_operation_updates():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell(name="d")
    d.min([a, b, c])
    a.value = date(1999, 1, 1)
    assert d.value == date(1999, 1, 1)


def test_date_cell_min_operation_consecutive():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell(date(2026, 1, 1), "d")
    f = DateCell(date(2027, 1, 1), "f")
    g = DateCell(name="g")
    g.min([a, b, c])
    g.min([d, f])
    assert g.value == date(2000, 1, 1)


def test_date_cell_gt():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(date(2024, 2, 1), "b")
    assert a > b


def test_date_cell_gt_date():
    a = DateCell(date(2024, 3, 1), "a")
    b = date(2024, 2, 1)
    assert a > b


def test_date_cell_gt_date_rev():
    a = date(2024, 3, 1)
    b = DateCell(date(2024, 2, 1), "b")
    assert a > b


def test_date_cell_gt_date_false():
    a = date(2024, 3, 1)
    b = DateCell(date(2024, 2, 1), "b")
    assert not a < b


def test_date_cell_lt():
    a = DateCell(date(2024, 2, 1), "a")
    b = DateCell(date(2024, 3, 1), "b")
    assert a < b


def test_date_cell_lt_date():
    a = DateCell(date(2024, 2, 1), "a")
    b = date(2024, 3, 1)
    assert a < b


def test_date_cell_lt_date_rev():
    a = date(2024, 2, 1)
    b = DateCell(date(2024, 3, 1), "b")
    assert a < b


def test_date_cell_lt_date_false():
    a = date(2024, 2, 1)
    b = DateCell(date(2024, 3, 1), "b")
    assert not a > b


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
    b.eomonth(a, 0)
    b.edays(None, 5)
    assert b.formula() == "edays( 03/31/2024, 5 )"


def test_date_cell_formula_deep_eomonth_edays():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.eomonth(a, 0)
    b.edays(None, 5)
    assert b.formula(deep=True) == "edays( eomonth( 2024-03-01, 0 ), 5 )"


def test_date_cell_edays_formula():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edays(a, 5)
    assert b.formula() == "edays( a, 5 )"


def test_date_cell_edays_formula_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, name="b")
    c = DateCell(name="c")
    c.edays(a, 5)
    assert c.formula(deep=True) == "edays( 2024-03-01, 5 )"


def test_date_cell_edate_formula():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edate(a, 5)
    assert b.formula() == "edate( a, 5 )"


def test_date_cell_edate_formula_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, name="b")
    c = DateCell(name="c")
    c.edate(a, 5)
    assert c.formula(deep=True) == "edate( 2024-03-01, 5 )"


def test_date_cell_edate_formula_date():
    a = date(2024, 3, 1)
    b = DateCell(name="b")
    b.edate(a, 5)
    assert b.formula() == "edate( 2024-03-01, 5 )"


def test_date_cell_eomonth_formula():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.eomonth(a, 5)
    assert b.formula() == "eomonth( a, 5 )"


def test_date_cell_eomonth_formula_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, name="b")
    c = DateCell(name="c")
    c.eomonth(a, 5)
    assert c.formula(deep=True) == "eomonth( 2024-03-01, 5 )"


def test_date_cell_eomonth_formula_date():
    a = date(2024, 3, 1)
    b = DateCell(name="b")
    b.eomonth(a, 5)
    assert b.formula() == "eomonth( 2024-03-01, 5 )"


def test_date_cell_max_formula(cell_list: List[DateCell]):
    e = max_date_cell(cells=cell_list, name="e")
    assert e.formula() == "max( a, b, c, d )"


def test_date_cell_max_formula_deep(cell_list: List[DateCell]):
    e = max_date_cell(cells=cell_list, name="e")
    assert e.formula(deep=True) == "max( 2024-01-01, 2025-01-01, 2026-01-01, 2027-01-01 )"


def test_date_cell_min_formula(cell_list: List[DateCell]):
    e = min_date_cell(cells=cell_list, name="e")
    assert e.formula() == "min( a, b, c, d )"


def test_date_cell_min_formula_deep(cell_list: List[DateCell]):
    e = min_date_cell(cells=cell_list, name="e")
    assert e.formula(deep=True) == "min( 2024-01-01, 2025-01-01, 2026-01-01, 2027-01-01 )"


def test_date_cell_min_formula_with_date(cell_list: List[DateCell]):
    cell_list[0] = date(2024, 1, 1)
    e = min_date_cell(cells=cell_list, name="e")
    assert e.formula() == "min( 2024-01-01, b, c, d )"


def test_date_cell_edate_max_combined_value():
    a = DateCell(name="a")
    a.edate(date(2028, 1, 1), 12)
    b = DateCell(date(2025, 1, 1), name="b")
    c = DateCell(date(2026, 1, 1), name="c")
    d = DateCell(date(2027, 1, 1), name="d")
    a.max([b, c, d])
    assert a.value == date(2029, 1, 1)


def test_date_cell_edate_max_combined_formula():
    a = DateCell(name="a")
    a.edate(date(2028, 1, 1), 12)
    b = DateCell(date(2025, 1, 1), name="b")
    c = DateCell(date(2026, 1, 1), name="c")
    d = DateCell(date(2027, 1, 1), name="d")
    a.max([b, c, d])
    assert a.formula() == "max( b, c, d, 01/01/2029 )"


def test_date_cell_edate_max_combined_formula_deep():
    a = DateCell(name="a")
    a.edate(date(2028, 1, 1), 12)
    b = DateCell(date(2025, 1, 1), name="b")
    c = DateCell(date(2026, 1, 1), name="c")
    d = DateCell(date(2027, 1, 1), name="d")
    a.max([b, c, d])
    assert a.formula(deep=True) == "max( 2025-01-01, 2026-01-01, 2027-01-01, edate( 2028-01-01, 12 ) )"


def test_date_cell_max_value_audit(cell_list: List[DateCell]):
    e = max_date_cell(cells=cell_list, name="e")
    assert e.value_audit() == "max( a, b, c, d )"


def test_date_cell_max_value_audit_deep(cell_list: List[DateCell]):
    e = max_date_cell(cells=cell_list, name="e")
    assert e.value_audit(deep=True) == "max( 2024-01-01, 2025-01-01, 2026-01-01, 2027-01-01 )"


def test_date_cell_min_value_audit(cell_list: List[DateCell]):
    e = min_date_cell(cells=cell_list, name="e")
    assert e.value_audit() == "min( a, b, c, d )"


def test_date_cell_min_value_audit_deep(cell_list: List[DateCell]):
    e = min_date_cell(cells=cell_list, name="e")
    assert e.value_audit(deep=True) == "min( 2024-01-01, 2025-01-01, 2026-01-01, 2027-01-01 )"


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


def test_date_cell_edays_value_audit():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edays(a, 5)
    assert b.value_audit() == "edays( 2024-03-01, 5 )"


def test_date_cell_edays_value_audit_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, name="b")
    c = DateCell(name="c")
    c.edays(a, 5)
    assert c.value_audit(deep=True) == "edays( 2024-03-01, 5 )"


def test_date_cell_edate_value_audit():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edate(a, 5)
    assert b.value_audit() == "edate( 2024-03-01, 5 )"


def test_date_cell_edate_value_audit_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, name="b")
    c = DateCell(name="c")
    c.edate(a, 5)
    assert c.value_audit(deep=True) == "edate( 2024-03-01, 5 )"


def test_date_cell_eomonth_value_audit():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.eomonth(a, 5)
    assert b.value_audit() == "eomonth( 2024-03-01, 5 )"


def test_date_cell_eomonth_value_audit_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, name="b")
    c = DateCell(name="c")
    c.eomonth(a, 5)
    assert c.value_audit(deep=True) == "eomonth( 2024-03-01, 5 )"


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
