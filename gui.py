from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTextEdit, QTreeWidget, QDockWidget, QTreeView, QInputDialog, QFileDialog, QLineEdit, QMessageBox
from PyQt6.QtGui import QIcon, QAction, QFileSystemModel
from PyQt6.QtCore import Qt, pyqtSignal
from pathlib import Path
from file_actions import *

#Mixin class to center any window on the screen
class CenterMixin():
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

#Default window class
class defaultWindow(QWidget, CenterMixin):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.resize(350, 250)
        self.center()

        self.setWindowTitle("File App")
        self.show()

#Main window of the program that houses all main actions
class mainWindow(QMainWindow, CenterMixin):
    def __init__(self):
        super().__init__()
        self.current_directory = str(Path.cwd()) #variable to hold the current selected directory, initialized to the top of the current working directory
        self.current_file = None #variable to hold the current selected directory, initialized to None
        self.initUI()

    def initUI(self):
    #Actions for menu bar options
    #Menubar action: exit program
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.exitProgram)

    #Menubar action: create new file
        newFileAct = QAction("New File", self)
        newFileAct.setShortcut("Ctrl+N")
        newFileAct.setStatusTip("Create a new file")
        newFileAct.triggered.connect(self.createFileAction)

    #Menubar action: create new Folder
        newFolderAct = QAction("New Folder", self)
        newFolderAct.setShortcut("Ctrl+K")
        newFolderAct.setStatusTip("Create a new folder")
        newFolderAct.triggered.connect(self.createFolderAction)

    #Menubar action: open file
        openFileAct = QAction("Open File", self)
        openFileAct.setShortcut("Ctrl+O")
        openFileAct.setStatusTip("Open a file")
        openFileAct.triggered.connect(self.openFile)

    #Create menu bar and add menubar members
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newFileAct)
        fileMenu.addAction(newFolderAct)
        fileMenu.addAction(openFileAct)
        fileMenu.addAction(exitAct)

    #Central text editor widget
        self.textEditor = QTextEdit()
        self.textEditor.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.textEditor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setCentralWidget(self.textEditor)

    #File tree dock widget
        self.file_tree_widget = fileTreeView()
        self.file_tree_widget.directorySelected.connect(self.onDirectorySelected) #when a directory change is detected, call the OnDirectorySelected method with the appropriate directory path
        self.file_tree_widget.fileSelected.connect(self.onFileSelected) #when a file change is detected, call the OnFileSelected method with the appropriate file path
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
        #Update the current working directory when a user selects a directory
        self.current_directory = directory_path
        self.statusBar().showMessage(f"Current directory: {self.current_directory}")

    def onFileSelected(self, file_path):
        #update the current file when selected when a user selects a file
        self.current_file = file_path
        self.statusBar().showMessage(f"Current file: {self.current_file}")

    def createFileAction(self):
        #display message to capture file name text and attempt file creation
        file_name, ok = QInputDialog.getText(self, "New File", "Enter file name:", QLineEdit.EchoMode.Normal, "File.txt")
        if ok and file_name:
            createNewFile(self, self.current_directory, file_name)

    def createFolderAction(self):
        #display message to capture folder name text and attempt folder creation
        folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:", QLineEdit.EchoMode.Normal, "New Folder")
        if ok and folder_name:
            createNewFolder(self, self.current_directory, folder_name)

    def openFile(self):
        #display a file open prompt and allow the user to select a file to open
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File") #returns an empty string if the user clicks cancel
        if file_path != "":
            loadFile(self, file_path)
            self.statusBar().showMessage(f"Opened file: {file_path}")

    def exitProgram(self):
        #display message to confirm the user would like to exit the program
        confirm_exit = QMessageBox.question(self, "Message", "Are you sure you want to exit?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if confirm_exit == QMessageBox.StandardButton.Yes:
            self.close()
    
    def showErrorMessage(self, error_message):
        #generic message box that shows an error message and does not allow the user to continue unless they accept
        message = QMessageBox(self)
        message.setText(error_message)
        message.exec()


class fileTreeView(QTreeView):
    directorySelected = pyqtSignal(str) #custom signal to emit the current selected directory
    fileSelected = pyqtSignal(str) #custom signal to emit the current selected file and parent directory
    def __init__(self):
        super().__init__()
        self.file_system = QFileSystemModel()
        #initialize the root file path in the tree as the top of the current working directory
        root_file_path = str(Path.cwd())
        self.file_system.setRootPath(root_file_path)
        self.setModel(self.file_system)

        root_index = self.file_system.index(root_file_path)
        self.setRootIndex(root_index)
        #connect the onItemClicked method to the action of clicking on an item in the tree, the clicked signal will send an index indicating which item was clicked
        self.clicked.connect(self.onItemClicked)

    def onItemClicked(self, index):
        #handle when an item in the tree is selected
        path = self.file_system.filePath(index) #set the file path to the current path at index
        #if the selected item index points to a directory, then emit the directory
        if self.file_system.isDir(index):
            self.directorySelected.emit(path)
        else:
        #if the selected item index points to a file, then emit the parent directory of the file and then emit the file path
            parent_path = str(Path(path).parent)
            self.directorySelected.emit(parent_path)
            self.fileSelected.emit(path)

        
    