from .cell import Cell
from typing import List, Callable
from sheetcake.src.utils import get_value


class MaxCell(Cell):
    def __init__(self, cells: List[Cell], name: str = "MaxCell", tolerance = 0.0, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> None:
        super().__init__(value = None, name=name, tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
        self.cells = cells
        for cell in cells:
            if hasattr(cell, "changed"):
                cell.changed.connect(self.update)
        self.update()

    def formula(self, deep: bool = False):
        return f"max( {', '.join(c.formula(deep) for c in self.cells)} )"
    
    def calculate(self):
        return max([get_value(cell) for cell in self.cells])
