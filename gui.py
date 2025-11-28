from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTextEdit, QTreeWidget, QDockWidget, QTreeView, QInputDialog
from PyQt6.QtGui import QIcon, QAction, QFileSystemModel
from PyQt6.QtCore import Qt, pyqtSignal
from pathlib import Path
from file_actions import *
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
        self.current_directory = str(Path.cwd())
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
        newFileAct.triggered.connect(self.createFileAction)
    #Create menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newFileAct)
        fileMenu.addAction(exitAct)

    #Central text editor widget
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)
    #File tree dock widget
        self.file_tree_widget = fileTreeView()
        self.file_tree_widget.directorySelected.connect(self.onDirectorySelected)
        dock = QDockWidget("File Tree", self)
        dock.setWidget(self.file_tree_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
    #Status bar at the bottom of the page
        self.statusBar()

    #Position window on creation
        self.setGeometry(0, 0, 900, 600)
        self.center()
        self.setWindowTitle('Main window')
        self.show()

    def onDirectorySelected(self, directory_path):
        self.current_directory = directory_path
        self.statusBar().showMessage(f"Current directory: {self.current_directory}")
    def createFileAction(self):
        file_name, ok = QInputDialog.getText(self, "New File", "Enter file name:")
        if ok and file_name:
            new_file_path = self.current_directory+ "/" + file_name
            createNewFile(new_file_path)

class fileTreeView(QTreeView):
    directorySelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.file_system = QFileSystemModel()
        root_file_path = str(Path.cwd())
        self.file_system.setRootPath(root_file_path)
        self.setModel(self.file_system)

        root_index = self.file_system.index(root_file_path)
        self.setRootIndex(root_index)

        self.clicked.connect(self.onItemClicked)

    def onItemClicked(self, index):
        file_path = self.file_system.filePath(index)
        if self.file_system.isDir(index):
            self.directorySelected.emit(file_path)
        else:
            parent_path = str(Path(file_path).parent)
            self.directorySelected.emit(parent_path)

        
    