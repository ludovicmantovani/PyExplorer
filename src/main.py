import sys

from PySide2.QtWidgets import QApplication, QWidget
from main_window import MainWindow

CONTEXT = {
    "style": "ressources/style.css",
    "home": "ressources/home.svg",
    "desktop": "ressources/desktop.svg",
    "documents": "ressources/documents.svg",
    "movies": "ressources/movies.svg",
    "pictures": "ressources/pictures.svg",
    "music": "ressources/music.svg",
}

if __name__ == '__main__':
    app = QApplication()
    window = MainWindow(CONTEXT)
    window.resize(1500, 600)
    window.show()
    exit_code = app.exec_()
    sys.exit(exit_code)
