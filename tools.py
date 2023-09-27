from enum import Enum


class CellState(Enum):
    EMPTY = 0
    HIT = 1


class ShipOrientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class PlayerStep(Enum):
    USER = 1
    COMPUTER = 2


class ThisGameException(Exception):
    pass


class GenerateShipsException(ThisGameException):
    """Exception raised когда при случайной генерации кораблей доска уже имеет корабли """
    def __init__(self):
        super().__init__("Ошибка при генерации кораблей.")


class ShootingWithoutThinkingException(ThisGameException):
    def __init__(self, msg):
        super().__init__(msg)
