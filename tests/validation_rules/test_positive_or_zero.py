from sheetcake import Cell
from sheetcake import validation_rules as vr
import pytest


def test_pos_or_zero_positive():
    assert vr.positive_or_zero(1) == True


def test_pos_or_zero_negative():
    assert vr.positive_or_zero(-1) == False


def test_pos_or_zero_zero():
    assert vr.positive_or_zero(0) == True


def test_pos_or_zero_none():
    assert vr.positive_or_zero(None) == False


def test_cell_pos_or_zero_no_error_on_init():
    cell = Cell(value=1, name="test", validation_rules=[vr.positive_or_zero])
    assert True


def test_cell_pos_or_zero_error_on_init():
    with pytest.raises(ValueError):
        cell = Cell(value=-1, name="test", validation_rules=[vr.positive_or_zero])


def test_cell_pos_or_zero_error_on_update():
    cell = Cell(value=1, name="test", validation_rules=[vr.positive_or_zero])
    with pytest.raises(ValueError):
        cell.value = -1
