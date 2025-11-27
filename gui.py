from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTextEdit, QTreeWidget, QDockWidget, QTreeView
from PyQt6.QtGui import QIcon, QAction, QFileSystemModel
from PyQt6.QtCore import Qt
from pathlib import Path
class CenterMixin():
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class defaultWindow(QWidget, CenterMixin):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.resize(350, 250)
        self.center()

        self.setWindowTitle("File App")
        self.show()

class mainWindow(QMainWindow, CenterMixin):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):


    #Actions for menu bar options
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        newFileAct = QAction("New File", self)
        newFileAct.setShortcut("Ctrl+N")
        newFileAct.setStatusTip("Create a new file")
        newFileAct.triggered.connect(self.close)

    #Create menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newFileAct)
        fileMenu.addAction(exitAct)

    #Central text editor widget
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)
    #File tree dock widget
        file_tree_widget = fileTreeView()
        dock = QDockWidget("File Tree", self)
        dock.setWidget(file_tree_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
    #Status bar at the bottom of the page
        self.statusBar()

    #Position window on creation
        self.setGeometry(0, 0, 900, 600)
        self.center()
        self.setWindowTitle('Main window')
        self.show()

    
class fileTreeView(QTreeView):
    def __init__(self):
        super().__init__()
        file_system = QFileSystemModel()
        root_file_path = str(Path.cwd())
        file_system.setRootPath(root_file_path)
        self.setModel(file_system)
    