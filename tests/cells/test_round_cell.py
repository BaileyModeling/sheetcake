from sheetcake2 import RoundCell, Cell
import pytest


@pytest.fixture
def rnd_float() -> RoundCell:
    return RoundCell(1.23456, 2, "rnd")


@pytest.fixture
def rnd_cell() -> RoundCell:
    a = Cell(1.23456, "a")
    return RoundCell(a, 2, "rnd")


def test_round_cell_float_formula(rnd_float: RoundCell):
    assert rnd_float.formula() == "round( 1.23456, 2 )"


def test_round_cell_cell_formula(rnd_cell: RoundCell):
    assert rnd_cell.formula() == "round( a, 2 )"


def test_round_cell_float_value(rnd_float: RoundCell):
    assert rnd_float.value == 1.23


def test_round_cell_cell_value(rnd_cell: RoundCell):
    assert rnd_cell.value == 1.23


def test_round_cell_none_is_none():
    a = Cell(None, "a")
    rnd = RoundCell(a, 2, "rnd")
    assert rnd.value is None