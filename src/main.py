import sys

from PySide2.QtWidgets import QApplication, QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Title")


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.resize(550, 600)
    window.show()
    exit_code = app.exec_()
    sys.exit(exit_code)
