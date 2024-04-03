from sheetcake import Array, Cell


def test_array_max():
    a = Array.from_values(values=(-100, 0, 100), name='a')
    b = Array.from_values(values=(10, 10, 10), name='b')
    c = Array.max(arrays=[a, b], name='c')
    assert c[0] == 10
    assert c[1] == 10
    assert c[2] == 100


def test_array_max_updates():
    a = Array.from_values(values=(-100, 0, 100), name='a')
    b = Array.from_values(values=(10, 10, 10), name='b')
    c = Array.max(arrays=[a, b], name='c')
    a.set_value(0, 1000)
    a.set_value(1, 1000)
    b.set_value(2, 1000)
    assert c[0] == 1000
    assert c[1] == 1000
    assert c[2] == 1000


def test_array_max_with_cell():
    a = Array.from_values(values=(-100, 0, 100), name='a')
    b = Cell(10, "b")
    c = Array.max(arrays=[a, b], name='c')
    assert c[0] == 10
    assert c[1] == 10
    assert c[2] == 100


def test_array_max_with_int():
    a = Array.from_values(values=(-100, 0, 100), name='a')
    b = 10
    c = Array.max(arrays=[a, b], name='c')
    assert c[0] == 10
    assert c[1] == 10
    assert c[2] == 100
