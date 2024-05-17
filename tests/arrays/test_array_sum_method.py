from sheetcake import Array


def test_adding_one_array_to_blank_array():
    c = Array.blank(num_cols=3, name='c')
    a = Array.from_values(values=(-10, 20, 30), name='a')
    c.add_item(a)
    assert c.get_value(0) == -10
    assert c.get_value(1) == 20
    assert c.get_value(2) == 30


def test_adding_two_arrays_with_array_sum_method():
    a = Array.from_values(values=(10, 20, 30), name='a')
    b = Array.from_values(values=(40, 50, 60), name='b')
    c = Array.sum(arrays=[a, b], name='c') 
    assert c.get_value(0) == 50
    assert c.get_value(1) == 70
    assert c.get_value(2) == 90


def test_adding_nested_array_sum_method_updating():
    a = Array.from_values(values=(1, 2, 3), name='a')
    b = Array.from_values(values=(10, 20, 30), name='b')
    c = Array.from_values(values=(100, 200, 300), name='c')
    d = Array.sum(arrays=[a, b], name='d')
    e = Array.sum(arrays=[d, c], name='e')
    a.set_value(0, 0)
    a.set_value(1, 0)
    a.set_value(2, 0)
    assert e[0] == 110
    assert e[1] == 220
    assert e[2] == 330
    assert e.total == 660
