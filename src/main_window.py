from functools import partial

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QToolBar, QTreeView, QListView, QSlider, QWidget, QHBoxLayout, \
    QFileSystemModel, QHeaderView
from PySide2.QtCore import Qt, QDir, QItemSelectionModel, QSize, QStandardPaths


# noinspection PyAttributeOutsideInit
class MainWindow(QMainWindow):
    def __init__(self, context):
        super().__init__()
        self.ctx = context
        self.setWindowTitle("PyExplorer")
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.add_actions_to_toolbar()
        self.setup_connections()
        self.create_file_model()

    def create_widgets(self):
        self.toolbar = QToolBar()
        self.tree_view = QTreeView()
        self.list_view = QListView()
        self.sld_iconSize = QSlider()
        self.main_widget = QWidget()

    def modify_widgets(self):
        style_file = self.ctx.get("style", None)
        if style_file:
            with open(style_file, "r") as f:
                self.setStyleSheet(f.read())

        self.list_view.setViewMode(QListView.IconMode)
        self.list_view.setUniformItemSizes(True)
        self.list_view.setIconSize(QSize(48, 48))

        self.sld_iconSize.setRange(48, 256)
        self.sld_iconSize.setValue(48)

        self.tree_view.setSortingEnabled(True)
        self.tree_view.sortByColumn(0, Qt.AscendingOrder)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def create_layouts(self):
        self.main_layout = QHBoxLayout(self.main_widget)

    def add_widgets_to_layouts(self):
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.setCentralWidget(self.main_widget)
        self.main_layout.addWidget(self.tree_view)
        self.main_layout.addWidget(self.list_view)
        self.main_layout.addWidget(self.sld_iconSize)

    def add_actions_to_toolbar(self):
        locations = ["home", "desktop", "documents", "movies", "pictures", "music"]
        for location in locations:
            icon = self.ctx.get(location, None)
            action = self.toolbar.addAction(QIcon(icon), location.capitalize())
            action.triggered.connect(partial(self.change_location, location))

    def setup_connections(self):
        self.tree_view.clicked.connect(self.treeview_cliked)
        self.list_view.clicked.connect(self.listview_cliked)
        self.list_view.doubleClicked.connect(self.listview_double_cliked)
        self.sld_iconSize.valueChanged.connect(self.change_icon_size)

    def change_icon_size(self, value):
        self.list_view.setIconSize(QSize(value, value))

    def change_location(self, location):
        standard_path = QStandardPaths()
        path = eval(f"standard_path.standardLocations(QStandardPaths.{location.capitalize()}Location)")
        path = path[0]
        self.tree_view.setRootIndex(self.model.index(path))
        self.list_view.setRootIndex(self.model.index(path))

    def create_file_model(self):
        self.model = QFileSystemModel()
        root_path = QDir.rootPath()
        self.model.setRootPath(root_path)
        self.tree_view.setModel(self.model)
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(root_path))
        self.tree_view.setRootIndex(self.model.index(root_path))

    def treeview_cliked(self, index):
        if self.model.isDir(index):
            self.list_view.setRootIndex(index)
        else:
            self.list_view.setRootIndex(index.parent())

    def listview_cliked(self, index):
        selection_model = self.tree_view.selectionModel()
        selection_model.setCurrentIndex(index, QItemSelectionModel.ClearAndSelect)

    def listview_double_cliked(self, index):
        self.list_view.setRootIndex(index)
