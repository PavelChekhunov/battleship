from tools import CellState
from ship import Ship


class Board:
    """
    Класс Board описывает игровое поле игрока или компа
    """

    def __init__(self, num_board_cells):
        self._num_board_cells = num_board_cells 
        self._board_cells = [-1 for _ in range(0, self._num_board_cells**2)]    # steps
        self._ships = []

    @property
    def num_board_cells(self):
        return self._num_board_cells

    @property
    def board_cells(self):
        return self._board_cells

    @property
    def ships(self):
        return self._ships

    def get_ships_lived(self):
        return [ship for ship in self._ships if ship.get_num_cells(CellState.EMPTY) > 0]

    def get_board_cells(self, cell_state: int):
        return [idx for idx, cell in enumerate(self._board_cells) if cell == cell_state]

    def add_ship(self, ship_cells: tuple):
        self._ships.append(Ship(ship_cells))

    def get_ship_area(self, ship):
        ret_cells = {*ship.cells}
        for cell in ship.cells:
            row_idx = cell // self._num_board_cells
            col_idx = cell % self._num_board_cells
            if row_idx > 0:
                ret_cells.add(cell - self._num_board_cells)
            if row_idx < self._num_board_cells - 1:
                ret_cells.add(cell + self._num_board_cells)
            if col_idx > 0:
                ret_cells.add(cell - 1)
                if row_idx > 0:
                    ret_cells.add(cell - self._num_board_cells - 1)
                if row_idx < self._num_board_cells - 1:
                    ret_cells.add(cell + self._num_board_cells - 1)
            if col_idx < self._num_board_cells - 1:
                ret_cells.add(cell + 1)
                if row_idx > 0:
                    ret_cells.add(cell - self._num_board_cells + 1)
                if row_idx < self._num_board_cells - 1:
                    ret_cells.add(cell + self._num_board_cells + 1)
        return tuple(ret_cells)

    def is_area_ship_died(self, cell_idx):
        for ship in self._ships:
            area_cells = self.get_ship_area(ship)
            if ship.is_ship_died() and cell_idx in area_cells:
                return True
        return False

    def get_ships_wounded(self):
        __ships = []
        for ship in self._ships:
            if not ship.is_ship_died():
                __ship_cells = ship.get_cells(CellState.HIT)
                if len(__ship_cells)>0:
                    __ships.append(__ship_cells)
        return __ships

    @property
    def empty_board_cells(self):
        __all_ships_cells = []
        for ship in self._ships:
            __all_ships_cells.extend(self.get_ship_area(ship))
        return [x for x in range(len(self._board_cells)) if x not in __all_ships_cells]

    def get_ship(self, cell_idx):
        for ship in self._ships:
            if cell_idx in ship.cells:
                return ship
        return None

    def shot(self, row, col):
        cell_idx = row * 10 + col
        ship = self.get_ship(cell_idx)
        if ship:
            ship.set_state(cell_idx, CellState.HIT)
            self._board_cells[cell_idx] = 1
            return True
        else:
            self._board_cells[cell_idx] = 0
            return False

    def test_get_ship(self, cell_index):
        self._ships.append(Ship((25, 35, 45)))
        result = (14, 15, 16, 24, 25, 26, 34, 35, 36, 44, 45, 46, 54, 55, 56)
        m_result = tuple(sorted(self.get_ship_area(self.get_ship(cell_index))))
        print(f'm: {m_result}\nd: {result}')
        assert result == m_result
        print(self.empty_board_cells)
        self.shot(4, 5)
        self.shot(4, 6)
        self.shot(3, 5)
        self.shot(2, 5)
        print(self.ships[0].get_cells(CellState.HIT), self.ships[0].is_ship_died())

    @property
    def is_all_ships_killed(self):
        for ship in self._ships:
            if not ship.is_ship_died():
                return False
        return True


if __name__ == '__main__':
    b = Board(10)
    b.test_get_ship(0)
