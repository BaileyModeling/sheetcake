from sheetcake2 import Array, Cell
from typing import List


class EndingBalance(Array):
    default_name = "Ending Balance"

    def __init__(self, array: List[Cell], name: str = 'Ending Balance') -> None:
        super().__init__(array=array, name=name)
        self.total = self.array[-1]

    def append(self, cell: Cell):
        self.array.append(cell)
        self.total = self.array[-1]
