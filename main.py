from main_window import MainWindow


class App:
    @staticmethod
    def main():
        window = MainWindow()
        window.mainloop()


if __name__ == '__main__':
    App.main()
