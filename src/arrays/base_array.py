from sheetcake.src import errors
from sheetcake import Cell


class BaseArray:
    def __init__(self, duration=None, name='Unnamed Array', array=None, fmt=None):
        self.name = name
        self.fmt = fmt
        if array is None:
            if duration is None:
                raise errors.ImproperConfig('must set duration or array')
            self._array = []
            for _ in range(duration):
                self._array.append(Cell(value=None, name=name, fmt=fmt))
        else:
            duration = len(array)
            self._array = []
            for item in array:
                if isinstance(item, Cell):
                    self._array.append(item)
                else:
                    self._array.append(Cell(value=item, name=name, fmt=fmt))
        # self.changed_value = Signal()
        # self.changed = Signal()

    def __len__(self):
        return len(self._array)

    def __getitem__(self, i) -> Cell:
        return self._array[i]

    @property
    def duration(self):
        return len(self._array)

    @property
    def array(self):
        return self._array

    def set_value(self, i, value):
        self._array[i].value = value

    def get_value(self, i):
        return self._array[i].value

    def set_values(self, array, start:int=0):
        for i, value in enumerate(array):
            self._array[start + i].value = value

    # def append(self, value=None, name=None, fmt=None) -> Cell:
    #     cell = Cell(value=value, name=name, fmt=fmt)
    #     self._array.append(cell)
    #     return cell
