from player import Player
import random
from tools import ShotOnBoardException

class CompPlayer(Player):
    def __init__(self, num_cells):
        super().__init__(num_cells)

    def check_win(self, enemy_board):
        return enemy_board.is_all_ships_killed, 'Вы програли!'

    @staticmethod
    def __get_next_step(cells, board):
        __gap = 0
        __len = len(cells)
        if __len == 0:
            return None
        elif __len > 1:
            __gap = abs(cells[1] - cells[0])
        __row = cells[0] // board.num_board_cells
        __min_val = min(cells)
        __max_val = max(cells)
        __vals = [__min_val - __gap, __max_val + __gap]
        if __gap == 0:
            __vals = [__min_val - board.num_board_cells, __min_val - 1,
                      __max_val + 1, __max_val + board.num_board_cells]
        for k in tuple(__vals):
            __gap = abs(k - cells[0])
            if (0 > k or k >= board.num_board_cells ** 2 or k not in board.get_board_cells(-1)
                    or k // board.num_board_cells != __row and __gap < board.num_board_cells):
                __vals.remove(k)
        if len(__vals) == 0:
            return -1
        return random.choice(__vals)

    @staticmethod
    def ai_player_step(func):
        def wrapper(self, enemy_board):
            __ships = enemy_board.get_ships_wounded()
            if len(__ships):
                __ship = random.choice(__ships)
                __next_idx = self.__get_next_step(__ship, enemy_board)
                return func(self, enemy_board, __next_idx)
            return func(self, enemy_board)
        return wrapper

    @ai_player_step
    def make_step(self, enemy_board, _cell_idx=-1):
        if _cell_idx == -1:
            _bcells = enemy_board.get_board_cells(-1)
            if not len(_bcells):
                raise ShotOnBoardException('Нет пустых ячеек для стрельбы по кораблям')
            _cell_idx = random.choice(_bcells)
        _row = _cell_idx // enemy_board.num_board_cells
        _col = _cell_idx % enemy_board.num_board_cells
        hit = enemy_board.shot(_row, _col)
        return hit, _row, _col
