import email.message
from tkinter import *
from tkinter import messagebox
from player import Player
from comp_player import CompPlayer
from tools import PlayerStep, GenerateShipsException, ShootingWithoutThinkingException, ShotOnBoardException
import time


class MainWindow(Tk):
    """
    Класс окно приложения. Для простоты реализации окно не может менять своего размера
    """

    WINDOW_WIDTH = 630
    WINDOW_HEIGHT = 400
    AREA_NUM_CELLS = 10
    CELL_WIDTH = CELL_HEIGHT = 25
    AREA_PAD = 40

    def __init__(self):
        super().__init__()
        self.geometry("600x450")
        self.title("Морской бой")
        x = (self.winfo_screenwidth() - MainWindow.WINDOW_WIDTH) // 2
        y = (self.winfo_screenheight() - MainWindow.WINDOW_HEIGHT) // 2
        self.geometry('{}x{}+{}+{}'.format(MainWindow.WINDOW_WIDTH, MainWindow.WINDOW_HEIGHT, x, y))
        self.resizable(False, False)
        self.attributes("-topmost", 1)
        area_w = MainWindow.AREA_NUM_CELLS * MainWindow.CELL_WIDTH
        area_h = MainWindow.AREA_NUM_CELLS * MainWindow.CELL_HEIGHT
        self._area1 = (MainWindow.AREA_PAD, MainWindow.AREA_PAD,
                       area_w + MainWindow.AREA_PAD, area_h + MainWindow.AREA_PAD)
        self._area2 = (area_w + MainWindow.AREA_PAD + MainWindow.CELL_WIDTH*2, MainWindow.AREA_PAD,
                       MainWindow.AREA_PAD + MainWindow.CELL_WIDTH*2 + area_w * 2, area_h + MainWindow.AREA_PAD)
        self._canvas = Canvas(self, width=MainWindow.WINDOW_WIDTH, height=MainWindow.AREA_PAD * 2 + area_h)
        self._canvas.place(x=0, y=0)
        self._btn1 = Button(self, text="Начать заново!", width=25, font="arial 10 bold",
                            command=self.btn_onstart)
        self._btn2 = Button(self, text="Показать корабли противника", width=25, font="arial 10 bold",
                            command=self.btn_showships)
        self._btn1.place(y=self._area1[3] + self._area1[1], x=self._area1[0])
        self._btn2.place(y=self._area2[3] + self._area2[1], x=self._area2[0])
        self.update_idletasks()
        self._btn1.place(y=self._area1[3] + self._area1[1] + self._btn1.winfo_height() // 2,
                         x=(self._area1[2] + self._area1[0] - self._btn1.winfo_width()) // 2)
        self._btn2.place(y=self._area2[3] + self._area2[1] + self._btn1.winfo_height() // 2,
                         x=(self._area2[2] + self._area2[0] - self._btn2.winfo_width()) // 2)
        self._player = Player(MainWindow.AREA_NUM_CELLS)
        self._comp_player = CompPlayer(MainWindow.AREA_NUM_CELLS)
        self.btn_onstart()

    def btn_onstart(self):
        self._canvas.bind_all("<Button-1>", self.cnv_onclick)
        self._remove_ships()
        self.__draw_areas()
        try:
            self._player.generate_ships()
        except GenerateShipsException as e:
            print("Exception has occurred! \n К сожалению игра сломалась!")
            self.quit()
        self._draw_ships(self._player.ships, self._area1)
        self._comp_player.generate_ships()
        self.update()

    def _remove_ships(self):
        self._player.board.__init__(MainWindow.AREA_NUM_CELLS)
        self._comp_player.board.__init__(MainWindow.AREA_NUM_CELLS)

    def _draw_ships(self, ships, area):
        for ship in ships:
            min_x = max_x = min_y = max_y = 0
            for cell in ship.cells:
                x = area[0] + (cell % 10) * MainWindow.CELL_WIDTH
                y = area[1] + (cell // 10) * MainWindow.CELL_HEIGHT
                area_cell = (x, y, MainWindow.CELL_WIDTH + x, MainWindow.CELL_HEIGHT + y)
                self._canvas.create_rectangle(area_cell, fill='#9acafa')
                min_x = x if min_x == 0 or min_x > x else min_x
                max_x = x if max_x == 0 or max_x < x else max_x
                min_y = y if min_y == 0 or min_y > y else min_y
                max_y = y if max_y == 0 or max_y < y else max_y
            area_cell = (min_x, min_y, MainWindow.CELL_WIDTH + max_x + 1, MainWindow.CELL_HEIGHT + max_y + 1)
            self._canvas.create_rectangle(area_cell, outline='#a02525', width=2, tags="ship-border")

    def btn_showships(self):
        self._draw_ships(self._comp_player.ships, self._area2)
        for item in self._canvas.find_withtag("ship-success"):
            self._canvas.tag_raise(item)
        self.update()

    def __draw_areas(self):
        area_line_color = '#30509f'
        self._canvas.delete("all")
        self._canvas.create_rectangle(self._area1, fill='#e7e7e7', outline=area_line_color)
        self._canvas.create_rectangle(self._area2, outline=area_line_color)
        for i in range(1, MainWindow.AREA_NUM_CELLS):
            x = MainWindow.CELL_WIDTH * i
            y = MainWindow.CELL_HEIGHT * i
            self._canvas.create_line(self._area1[0] + x, self._area1[1], self._area1[0] + x, self._area1[3],
                                     fill=area_line_color)
            self._canvas.create_line(self._area1[0], y + self._area1[1], self._area1[2], y + self._area1[1],
                                     fill=area_line_color)
            self._canvas.create_line(self._area2[0] + x, self._area2[1], self._area2[0] + x, self._area2[3],
                                     fill=area_line_color)
            self._canvas.create_line(self._area2[0], y + self._area2[1], self._area2[2], y + self._area2[1],
                                     fill=area_line_color)
            self._canvas.create_text(self._area1[0] + x - MainWindow.CELL_WIDTH // 2,
                                     self._area1[1] - MainWindow.CELL_HEIGHT // 2,
                                     text=chr(i + 64))
            self._canvas.create_text(self._area1[0] + x - MainWindow.CELL_HEIGHT // 2,
                                     self._area1[3] + MainWindow.CELL_HEIGHT // 2,
                                     text=chr(i + 64))
            self._canvas.create_text(self._area2[0] + x - MainWindow.CELL_WIDTH // 2,
                                     self._area1[1] - MainWindow.CELL_HEIGHT // 2,
                                     text=chr(i + 64))
            self._canvas.create_text(self._area2[0] + x - MainWindow.CELL_WIDTH // 2,
                                     self._area1[3] + MainWindow.CELL_HEIGHT // 2,
                                     text=chr(i + 64))
            self._canvas.create_text(self._area1[2] + MainWindow.CELL_WIDTH,
                                     self._area1[1] + y - MainWindow.CELL_HEIGHT // 2,
                                     text=str(i), font="arial 10 bold")
        self._canvas.create_text(self._area1[2] - MainWindow.CELL_WIDTH // 2,
                                 self._area1[1] - MainWindow.CELL_HEIGHT // 2, text=chr(74))
        self._canvas.create_text(self._area1[2] - MainWindow.CELL_WIDTH // 2,
                                 self._area1[3] + MainWindow.CELL_HEIGHT // 2, text=chr(74))
        self._canvas.create_text(self._area2[2] - MainWindow.CELL_WIDTH // 2,
                                 self._area2[1] - MainWindow.CELL_HEIGHT // 2, text=chr(74))
        self._canvas.create_text(self._area2[2] - MainWindow.CELL_WIDTH // 2,
                                 self._area2[3] + MainWindow.CELL_HEIGHT // 2, text=chr(74))
        self._canvas.create_text(self._area1[2] + MainWindow.CELL_WIDTH, self._area1[3] - MainWindow.CELL_HEIGHT // 2,
                                 text="10", font="arial 10 bold")

    def _mark_cell(self, t_step, hit, row, col):
        __area = self._area2 if t_step == PlayerStep.USER else self._area1
        line_color = 'green' if t_step == PlayerStep.USER else 'red'
        oval_color = 'red' if t_step == PlayerStep.USER else 'green'
        __x = __area[0] + col * MainWindow.CELL_WIDTH
        __y = __area[1] + row * MainWindow.CELL_HEIGHT
        if hit:
            __line_area = (__x + 4, __y + 4, __x + MainWindow.CELL_WIDTH - 4, MainWindow.CELL_HEIGHT + __y - 4)
            self._canvas.create_line(__line_area, fill=line_color, width=3, tags="ship-success")
            __line_area = (__x + MainWindow.CELL_WIDTH - 4, __y + 4, __x + 4, MainWindow.CELL_HEIGHT + __y - 4)
            self._canvas.create_line(__line_area, fill=line_color, width=3, tags="ship-success")
        else:
            __line_area = (__x + 7, __y + 7, __x + MainWindow.CELL_WIDTH - 7, MainWindow.CELL_HEIGHT + __y - 7)
            self._canvas.create_oval(__line_area, fill=oval_color, tags="ship-failed")
            pass

    def __draw_ship_background(self, cell_idx):
        __board = self._comp_player.board
        __ship = __board.get_ship(cell_idx)
        if __ship and __ship.is_ship_died():
            for __cell in __board.get_ship_area(__ship):
                __cell_x = __cell % MainWindow.AREA_NUM_CELLS * MainWindow.CELL_WIDTH + self._area2[0]
                __cell_y = __cell // MainWindow.AREA_NUM_CELLS * MainWindow.CELL_HEIGHT + self._area2[1]
                __bg = self._canvas.create_rectangle(__cell_x, __cell_y,
                                                     __cell_x + MainWindow.CELL_WIDTH,
                                                     __cell_y + MainWindow.CELL_HEIGHT,
                                                     fill='#f3c9c9', tags="ship-around-bg")
                self._canvas.tag_lower(__bg)

    def cnv_onclick(self, event):
        _m_x = self._canvas.winfo_pointerx() - self._canvas.winfo_rootx()
        _m_y = self._canvas.winfo_pointery() - self._canvas.winfo_rooty()
        if _m_x < self._area2[0] or _m_x > self._area2[2] or _m_y < self._area2[1] or _m_y > self._area2[3]:
            return
        _col = (_m_x - self._area2[0]) // MainWindow.CELL_WIDTH
        _row = (_m_y - self._area2[1]) // MainWindow.CELL_HEIGHT
        __idx = _row * 10 + _col
        try:
            if self._comp_player.board.is_area_ship_died(__idx):
                """Конечно глупо вызывать исключение, если можно обработать код не вызывая его, 
                но не могу придумать где ещё можно применить знание о них"""
                raise ShootingWithoutThinkingException('В данной ячейке игрового поля не может быть корабля!\n'
                                                       'Корабли стоят друг от друга как минимум на расстоянии '
                                                       'в одну клетку.')
        except ShootingWithoutThinkingException as ex:
            messagebox.showinfo(title='Морской бой', message=str(ex))
        _hit = self._comp_player.board.shot(_row, _col)
        self._mark_cell(PlayerStep.USER, _hit, _row, _col)
        self.__draw_ship_background(__idx)
        self.update()
        _win, _msg = self._player.check_win(self._comp_player.board)
        if _hit or _win:
            if _win:
                self._canvas.unbind_all("<Button-1>")
                messagebox.showinfo(title='Морской бой', message=_msg)
            return
        self._canvas.unbind_all("<Button-1>")
        while True:
            time.sleep(0.5)
            _hit, _row, _col = self._comp_player.make_step(self._player.board)
            try:
                self._mark_cell(PlayerStep.COMPUTER, _hit, _row, _col)
            except ShotOnBoardException as ex:
                messagebox.showinfo(title='Морской бой', message=str(ex))
            self.update()
            _win, _msg = self._comp_player.check_win(self._player.board)
            if _win:
                messagebox.showinfo(title='Морской бой', message=_msg)
                return
            if not _hit:
                break
        self._canvas.bind_all("<Button-1>", self.cnv_onclick)
