from sheetcake2 import Cell, MinCell
import pytest
from typing import List


@pytest.fixture
def cells() -> List[Cell]:
    a = Cell(-10, "a")
    b = Cell(0, "b")
    c = Cell(0.5, "c")
    d = Cell(10, "d")
    return [a, b, c, d]


def test_min_cell_init(cells: List[Cell]):
    min_cell = MinCell(cells)
    assert min_cell.value == -10


def test_min_cell_smallest_updates(cells: List[Cell]):
    min_cell = MinCell(cells)
    cells[0].value = -100
    assert min_cell.value == -100


def test_min_cell_largest_updates(cells: List[Cell]):
    min_cell = MinCell(cells)
    cells[3].value = -100
    assert min_cell.value == -100


def test_min_cell_formula(cells: List[Cell]):
    min_cell = MinCell(cells)
    assert min_cell.formula() == "min( a, b, c, d )"
