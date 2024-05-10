from sheetcake import Cell, SumCell
import pytest
from typing import List


@pytest.fixture
def cells() -> List[Cell]:
    a = Cell(-10, "a")
    b = Cell(0, "b")
    c = Cell(0.5, "c")
    d = Cell(10, "d")
    return [a, b, c, d]


def test_sum_cell_init(cells: List[Cell]):
    sum_cell = SumCell(cells)
    assert sum_cell.value == 0.5


def test_sum_cell_init_empty_list():
    sum_cell = SumCell(cells=[])
    assert sum_cell.value == None


def test_sum_cell_smallest_updates(cells: List[Cell]):
    sum_cell = SumCell(cells)
    cells[0].value = 100
    assert sum_cell.value == 110.5


def test_sum_cell_largest_updates(cells: List[Cell]):
    sum_cell = SumCell(cells)
    cells[3].value = 100
    assert sum_cell.value == 90.5
