from sheetcake import Cell, MaxCell
import pytest
from typing import List


@pytest.fixture
def cells() -> List[Cell]:
    a = Cell(-10, "a")
    b = Cell(0, "b")
    c = Cell(0.5, "c")
    d = Cell(10, "d")
    return [a, b, c, d]


def test_max_cell_init(cells: List[Cell]):
    max_cell = MaxCell(cells)
    assert max_cell.value == 10


def test_max_cell_smallest_updates(cells: List[Cell]):
    max_cell = MaxCell(cells)
    cells[0].value = 100
    assert max_cell.value == 100


def test_max_cell_largest_updates(cells: List[Cell]):
    max_cell = MaxCell(cells)
    cells[3].value = 100
    assert max_cell.value == 100


def test_max_cell_formula(cells: List[Cell]):
    max_cell = MaxCell(cells)
    assert max_cell.formula() == "max( a, b, c, d )"
