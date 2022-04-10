from sheetcake import Array
from sheetcake.src import errors


class ArraySubtract(Array):

    def __init__(self, *args, name='Unnamed Array', fmt=None, duration=None):
        self.args = list(args)
        if len(args):
            duration = len(args[0])
        if duration is None:
            raise errors.ImproperConfig("Must set either args or duration.")
        super().__init__(duration=duration, name=name, fmt=fmt)
        for array in args:
            if not len(array) == duration:
                raise ValueError(f"Cannot add arrays of different length: {len(array)}, {duration}")
            for i, cell in enumerate(array):
                self[i].sub(cell)

    @property
    def arrays(self):
        return self.args

    def sub(self, *args):
        self.args += list(args)
        super().sub(*args)
