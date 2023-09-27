from tools import GenerateShipsException
from board import Board
import random


class Player:
    def __init__(self, num_cells):
        self._board = Board(num_cells)

    @property
    def board(self):
        return self._board

    @property
    def ships(self):
        return self._board.ships

    def generate_ships(self):
        try:
            self._board.add_ship(self.__get_ship_cells(5))
            for i in range(2):
                self._board.add_ship(self.__get_ship_cells(3))
            for i in range(3):
                self._board.add_ship(self.__get_ship_cells(2))
            for i in range(5):
                self._board.add_ship(self.__get_ship_cells(1))
        except Exception:
            self._board.ships.clear()
            raise GenerateShipsException()

    def __get_ship_cells(self, ship_size):
        __cells = []
        while ship_size != len(__cells):
            __cells.clear()
            __cells.append(random.choice(self._board.empty_board_cells))
            if ship_size < 2:
                return __cells
            for i in range(1, ship_size):
                __next_cell = self. __get_next_cell(__cells)
                if not __next_cell:
                    break
                __cells.append(__next_cell)
        return tuple(__cells)

    def __get_next_cell(self, cells):
        __gap = 0
        __len = len(cells)
        if __len == 0:
            return None
        elif __len > 1:
            __gap = abs(cells[1] - cells[0])
        __row = cells[0]//self._board.num_board_cells
        __min_val = min(cells)
        __max_val = max(cells)
        __vals = [__min_val - __gap, __max_val + __gap]
        if __gap == 0:
            __vals = [__min_val - self._board.num_board_cells, __min_val - 1,
                      __max_val + 1, __max_val + self._board.num_board_cells]
        for k in tuple(__vals):
            __gap = abs(k - cells[0])
            if (0 > k or k >= self._board.num_board_cells**2 or k not in self._board.empty_board_cells
                    or k // self._board.num_board_cells != __row and __gap < self._board.num_board_cells):
                __vals.remove(k)
        if len(__vals) == 0:
            return None
        return random.choice(__vals)

    def check_win(self, enemy_board):
        return enemy_board.is_all_ships_killed, 'Вы выиграли!'

    def make_step(self, enemy_board):
        pass

    def test_ships(self):
        # cells = [77]
        # n = self.__get_next_cell(cells)
        # print(n)
        # ship_cells = self.__get_ship_cells(5)
        # print(ship_cells)
        self.generate_ships()
        for ship in self._board.ships:
            print(ship)


if __name__ == '__main__':
    p = Player(10)
    p.test_ships()
