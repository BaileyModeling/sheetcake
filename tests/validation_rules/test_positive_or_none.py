from sheetcake2 import Cell
from sheetcake2 import validation_rules as vr
import pytest


def test_pos_or_none_positive():
    assert vr.positive_or_none(1) == True


def test_pos_or_none_negative():
    assert vr.positive_or_none(-1) == False


def test_pos_or_none_zero():
    assert vr.positive_or_none(0) == True


def test_pos_or_none_none():
    assert vr.positive_or_none(None) == True


def test_cell_pos_or_none_no_error_on_init():
    cell = Cell(value=1, name="test", validation_rules=[vr.positive_or_none])
    assert True


def test_cell_pos_or_none_error_on_init():
    with pytest.raises(ValueError):
        cell = Cell(value=-1, name="test", validation_rules=[vr.positive_or_none])


def test_cell_pos_or_none_error_on_update():
    cell = Cell(value=1, name="test", validation_rules=[vr.positive_or_none])
    with pytest.raises(ValueError):
        cell.value = -1
