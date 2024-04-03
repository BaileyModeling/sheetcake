from sheetcake.src.utils import get_value


def test_get_value_returns_default():
    assert get_value(None, 0) == 0
    assert get_value("string", 0) == 0
