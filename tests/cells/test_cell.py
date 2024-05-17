from sheetcake import Cell


class CallbackClass:
    variable = None
    def callback(self, value):
        self.variable = value


class ObserverClass:
    variable = None
    def callback(self, value):
        self.variable = value


def test_cell_str():
    a = Cell(5)
    assert str(a) == "5"


def test_cell_repr():
    a = Cell(5)
    repr(a)
    assert True


def test_cell_repr_callback():
    test_object = CallbackClass()
    a = Cell(5, "name", callback=test_object.callback)
    assert repr(a) == "Cell(5, name='name', tolerance=0.0, fmt=str, callback=callback, locked=False, validation_rules=[], meta_data={})"


def test_cell_callback():
    test_object = CallbackClass()
    a = Cell(1, "a")
    b = Cell(2, "b")
    c = Cell(None, "c", callback=test_object.callback)
    c.sum_items(a, b)
    a.value = 10
    assert test_object.variable == 12


def test_cell_signal_sends_new_value():
    observer = ObserverClass()
    a = Cell(5, "name")
    a.changed.connect(observer.callback)
    a.value = 10
    assert observer.variable == 10


def test_cell_print():
    a = Cell(5)
    a.print()
    assert True


def test_cell_formula_no_operations():
    a = Cell(None, "name")
    assert a.formula() == "name"


def test_cell_formula_number():
    a = Cell(5, "name")
    assert a.formula() == "name"


def test_cell_formula():
    a = Cell(5, "a")
    b = Cell(3, "b")
    c = a + b
    assert c.formula() == "( a + b )"


def test_cell_formula_integer():
    a = Cell(5, "a")
    c = a + 3
    assert c.formula() == "( a + 3 )"


def test_cell_formula_deep():
    a = Cell(5, "a")
    b = Cell(3, "b")
    c = a + b
    d = Cell(4, "d")
    e = c + d
    assert e.formula(deep=True) == "( ( a + b ) + d )"


def test_cell_value_audit_no_operations():
    a = Cell(None, "name")
    assert a.value_audit() == "None"


def test_cell_value_audit_integer():
    a = Cell(5, "name")
    assert a.value_audit() == "5"


def test_cell_value_audit():
    a = Cell(5, "a")
    b = Cell(3, "b")
    c = a + b
    d = Cell(4, "d")
    e = c + d
    assert e.value_audit(deep=True) == "( ( 5 + 3 ) + 4 )"


def test_cell_init_empty():
    cell = Cell()
    assert cell.value is None


def test_cell_init_zero():
    cell = Cell(0)
    assert cell.value == 0
    assert isinstance(cell.value, int)


def test_cell_value_updates():
    cell = Cell()
    cell.value = 5
    assert cell.value == 5


def test_cell_equal_formula():
    a = Cell(5)
    b = Cell()
    b.equal_item(a)
    assert b.value == 5
    a.value = 100
    assert b.value == 100


def test_cell_init_with_another_cell_sets_value():
    a = Cell(5)
    b = Cell(a)
    assert b.value == 5


def test_cell_equal_number():
    a = Cell()
    a.equal_item(5)
    assert a.value == 5


def test_cell_init_with_another_cell_updates():
    a = Cell(5)
    b = Cell(a)
    a.value = 3
    assert b.value == 3


def test_sequence_and_timing():
    a = Cell(5, name="a")
    previous = a
    cells = []
    for _ in range(100):
        cell = Cell(previous)
        cells.append(cell)
        previous = cell
    a.value = 99
    assert cells[-1].value == 99


def test_cell_equal_override():
    """
    The 'equal' function should override any previous operations.
    """
    a = Cell(5, "a")
    b = Cell(10, "b")
    c = Cell(None, "c").sum_items(a, b)
    d = Cell(99, "d")
    c.equal_item(d)
    assert c.value == 99


def test_cell_negative():
    a = Cell(5)
    b = -a
    assert b.value == -5


def test_cell_negative_updates():
    a = Cell(5)
    b = -a
    a.value = 10
    assert b.value == -10

def test_cell_rounding():
    a = Cell(1.234567)
    assert round(a, 2) == 1.23
    assert round(a, 3) == 1.235


def test_formula_updates():
    a = Cell(5, "a")
    b = Cell(3, "b")
    c = 4 * (a + b) / 2
    b.value = 4
    assert c.value == 18


def test_cell_change_value_to_none():
    a = Cell()
    assert a.has_changed(5)


def test_cell_isequal_cell():
    a = Cell(5)
    b = Cell(5)
    assert a == b


def test_cell_isequal_number():
    a = Cell(5)
    assert a == 5


def test_cell_not_equal_number():
    a = Cell(5)
    assert not a == 1


def test_cell_has_changed_below_tolerance():
    a = Cell(5.50, tolerance=0.1)
    assert not a.has_changed(5.54)


def test_cell_meta_data():
    a = Cell(5, "name")
    a.meta_data["key"] = "value"
    assert a.meta_data["key"] == "value"


def test_cell_meta_data_init():
    a = Cell(5, "name", meta_data={"key": "value"})
    assert a.meta_data["key"] == "value"


# TODO: test decimal math
