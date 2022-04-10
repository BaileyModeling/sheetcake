from sheetcake import Array, NegateArray


def test_negate_array():
    a = Array(array=(-3, 0, 5, 10.1), name='a')
    c = NegateArray(a)
    assert c[0] == 3
    assert c[1] == 0
    assert c[2] == -5
    assert c[3] == -10.1
    assert abs(c.total + 12.1) < 0.001
