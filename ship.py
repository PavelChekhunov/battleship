from tools import CellState, ShipOrientation


class Ship:
    """
    Класс корабль.
    В качестве входных данных конструктора получает кортеж с индексами ячеек кораблей (cells).
    Все свойства вычисляются  исходя из этих данных
    """

    def __init__(self, cells):
        self._cells = cells
        self._states = {x: CellState.EMPTY for x in cells}

    @property
    def cells(self):
        return self._cells

    @property
    def length(self):
        return len(self._cells)

    @property
    def start_index(self):
        return min(self._cells)

    @property
    def ship_orientation(self):
        return ShipOrientation.HORIZONTAL if self.length < 2 or abs(self._cells[0] - self._cells[1]) == 1 \
            else ShipOrientation.VERTICAL

    def get_cells(self, state: CellState):
        return [cell for cell in self._cells if self._states[cell] == state]

    def is_ship_died(self):
        # return len(self.get_cells(CellState.HIT)) == len(self.cells)
        return len(self.get_cells(CellState.EMPTY)) == 0

    def set_state(self, cell_idx, state: CellState):
        self._states[cell_idx] = state

    def __repr__(self):
        return f'Ship cells: {self.cells}'

    def test1(self):
        print(self._states)


if __name__ == '__main__':
    s = Ship((11, 12, 10))
    s.test1()
