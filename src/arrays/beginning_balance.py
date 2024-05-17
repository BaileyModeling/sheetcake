from sheetcake import Array, Cell
from typing import List


class BeginningBalance(Array):
    default_name = "Beginning Balance"

    def __init__(self, array: List[Cell], name: str = 'Beginning Balance') -> None:
        super().__init__(array=array, name=name)
        self.total = self.array[0]

    def connect_ending_balance(self, ebal_array):
        self.ebal_array = ebal_array
        if not len(ebal_array) == self.duration:
            raise ValueError(f"Beginning Balance Array length does not match Ending Balance Array length: {self.duration} vs. {len(ebal_array)}")
        for i, cell in enumerate(ebal_array):
            if i < self.duration - 1:
                self[i+1].equal_item(cell)

    def append(self, cell: Cell):
        self.array.append(cell)
