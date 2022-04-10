from sheetcake import Array
from sheetcake.src import errors


class NegateArray(Array):

    def __init__(self, array, name=None):
        name = name or f"Negate: {array.name}"
        duration = len(array)
        negative = Array(array=[-1]*duration, name="-1")
        self.args = [negative, array]
        super().__init__(duration=duration, name=name)
        for i, cell in enumerate(array):
            self[i].equal(-1)
            self[i].mult(cell)

    @property
    def arrays(self):
        return self.args
