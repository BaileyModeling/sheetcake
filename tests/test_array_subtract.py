from sheetcake import ArraySubtract, Array


def test_array_subtract():
    a = Array(array=(-100, 0, 100), name='a')
    b = Array(array=(100, 100, -200), name='b')
    c = ArraySubtract(a, a, b, name="c")
    assert c[0].value == 100
    assert c[1].value == -100
    assert c[2].value == 0
