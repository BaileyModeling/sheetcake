from sheetcake import Row


def test_row_get_value():
    row = Row.from_values([1, 2], "test")
    assert row.get_value(0) == 1
    assert row.get_value(1) == 2


def test_row_get_item():
    row = Row.from_values([1, 2], "test")
    assert row[0] == 1
    assert row[1] == 2


def test_row_len():
    row = Row.from_values([1, 2], "test")
    assert len(row) == 2


def test_row_iter():
    row = Row.from_values([1, 2], "test")
    assert list(row) == [1, 2]


def test_row_append():
    row = Row.from_values([1, 2], "test")
    row.append(3)
    assert row[2] == 3


def test_row_blank():
    row = Row.blank(2, "test")
    assert len(row) == 2
    assert row[0].value is None


def test_row_zeros():
    row = Row.zeros(2, "test")
    assert len(row) == 2
    assert row[0].value == 0
    assert row[1].value == 0
