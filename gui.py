from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTextEdit, QTreeWidget, QDockWidget, QTreeView, QInputDialog, QFileDialog, QLineEdit, QMessageBox, QMenu
from PyQt6.QtGui import QIcon, QAction, QFileSystemModel, QFont
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
        self.active_file = None #variable to hold the path of the currently active file within the text editor
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

    #Menubar action: save file
        saveFileAct = QAction("Save", self)
        saveFileAct.setShortcut("Ctrl+S")
        saveFileAct.setStatusTip("Save a file")
        saveFileAct.triggered.connect(self.saveFileAction)

    #Create menu bar and add menubar members
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newFileAct)
        fileMenu.addAction(newFolderAct)
        fileMenu.addAction(openFileAct)
        fileMenu.addAction(saveFileAct)
        fileMenu.addAction(exitAct)

    #Central text editor widget
        self.textEditor = QTextEdit()
        self.textEditor.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.textEditor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setCentralWidget(self.textEditor)
        font = QFont("Courier", 12)
        self.textEditor.setFont(font)

    #File tree dock widget
        self.file_tree_widget = fileTreeView()
        self.file_tree_widget.directorySelected.connect(self.onDirectorySelected) #when a directory change is detected, call the OnDirectorySelected method with the appropriate directory path
        self.file_tree_widget.fileSelected.connect(self.onFileSelected) #when a file change is detected, call the OnFileSelected method with the appropriate file path
        self.file_tree_widget.loadFileRequested.connect(self.openFile) #when a file is requested to be loaded from the file tree view, call the openFile method with the requested location 
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
            file_path = createNewFile(self, self.current_directory, file_name)
            if file_path is not None:
                self.file_tree_widget.focusOnPath(file_path)

    def createFolderAction(self):
        #display message to capture folder name text and attempt folder creation
        folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:", QLineEdit.EchoMode.Normal, "New Folder")
        if ok and folder_name:
            folder_path = createNewFolder(self, self.current_directory, folder_name)
            if folder_path is not None:
                self.file_tree_widget.focusOnPath(folder_path)

    def openFile(self, from_file_tree = False):
        #display a file open prompt and allow the user to select a file to open
        file_path = None
        #test if openFile was requested from the menu and needs a file or if a specific file has already been selected in the file tree view
        if from_file_tree:
            file_path = from_file_tree
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open File") #returns an empty string if the user clicks cancel

        if file_path != "": #ensure file path is not empty
            loadFile(self, file_path)
            self.active_file = file_path
            self.statusBar().showMessage(f"Opened file: {file_path}")

    def saveFileAction(self):
        if self.active_file:
            #Normal saving for when a user has already opened a file and edited
            saveFile(self, self.active_file)
        else:
            #Dynamic saving by allowing the user to select a location and name for the file
            self.saveAsDialog()

    def saveAsDialog(self):
        #Get a name and location for the file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "")
        if file_path: #if valid
            #focus the file tree on that path and then save
            self.file_tree_widget.focusOnPath(file_path)
            saveFile(self, file_path)

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
    loadFileRequested = pyqtSignal(str) #custom signal to emit the requested file to be opened in the main text editor
    def __init__(self):
        super().__init__()
        self.file_system = QFileSystemModel()
        #initialize the root file path in the tree as the top of the current working directory
        root_file_path = str(Path.cwd())
        self.file_system.setRootPath(root_file_path)
        self.setModel(self.file_system)

        #context menu (right click properties) for items in the file tree view
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openContextMenu)

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

    def focusOnPath(self, path):
        #focus the file tree on a specific file/folder and update the currently selected file or directory
        pathIndex = self.file_system.index(path) #index in the model of a specific path
        if pathIndex.isValid():
            self.expand(pathIndex)
            self.scrollTo(pathIndex)
            self.setCurrentIndex(pathIndex)
            #if the focused path is a directory, then emit the directory
            if self.file_system.isDir(pathIndex):
                self.directorySelected.emit(path)
            else:
            #if the focused path is a file, then emit the parent directory of the file and then emit the file path
                parent_path = str(Path(path).parent)
                self.directorySelected.emit(parent_path)
                self.fileSelected.emit(path)
        #fallback for if a root folder or file was deleted
        else:
            self.fileSelected.emit(None)
            self.directorySelected.emit(str(Path.cwd()))

    def openContextMenu(self, position):
        #Find the index of the item at the position of the cursor
        index = self.indexAt(position)
        if not index.isValid():
            return   # right-click on empty area
        #file path to the selected item
        path = self.file_system.filePath(index)

        menu = QMenu(self)
        if self.file_system.isDir(index):
            #Context menu actions for folders
            #Action to expand the folder in the file tree view
            expandFolderAct = QAction("Expand Folder", self)
            expandFolderAct.setStatusTip("Expand the folder")
            expandFolderAct.triggered.connect(lambda: self.expand(index))
            #Action to collapse the folder in te file tree view
            collapseFolderAct = QAction("Collapse Folder", self)
            collapseFolderAct.setStatusTip("Collapse the folder")
            collapseFolderAct.triggered.connect(lambda: self.collapse(index))
            #Action to delete the selected folder
            deleteFolderAct = QAction("Delete Folder", self)
            deleteFolderAct.setStatusTip("Delete the selected folder")
            deleteFolderAct.triggered.connect(lambda: self.deleteFolderHelper(path))
            #Action to rename the selected folder
            renameFolderAct = QAction("Rename Folder", self)
            renameFolderAct.setStatusTip("Rename the selected folder")
            renameFolderAct.triggered.connect(lambda: self.renameFolderHelper(path))
            #check if the folder is already expanded
            if self.isExpanded(index):
                menu.addAction(collapseFolderAct)
            else:
                menu.addAction(expandFolderAct)
            menu.addAction(renameFolderAct)
            menu.addAction(deleteFolderAct)
        else:
            #Context menu actions for files
            #open a selected file in the text editor widget
            openFileAct = QAction("Open File", self)
            openFileAct.setStatusTip("Load the file into the editor")
            openFileAct.triggered.connect(lambda: self.loadFileRequested.emit(path))
            #Action to delete the selected file
            deleteFileAct = QAction("Delete File", self)
            deleteFileAct.setStatusTip("Delete the selected file")
            deleteFileAct.triggered.connect(lambda: self.deleteFileHelper(path))      
            #Action to rename the selected file
            renameFileAct = QAction("Rename File", self)
            renameFileAct.setStatusTip("Rename the selected file")
            renameFileAct.triggered.connect(lambda: self.renameFileHelper(path))
            menu.addAction(openFileAct)
            menu.addAction(renameFileAct)
            menu.addAction(deleteFileAct)
        #detect which
        chosen = menu.exec(self.viewport().mapToGlobal(position))
    
    def deleteFolderHelper(self, folder_path):
        #helper method to delete folders from the file tree view
        confirm_delete = QMessageBox.question(self, "Message", ("Are you you want to remove folder " + folder_path), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if confirm_delete == QMessageBox.StandardButton.Yes:
            deleteFolder(self, folder_path)
            self.focusOnPath(str(Path(folder_path).parent))

    def deleteFileHelper(self, file_path):
        #helper method to delete files from the file tree view
        confirm_delete = QMessageBox.question(self, "Message", ("Are you you want to remove file " + file_path), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if confirm_delete == QMessageBox.StandardButton.Yes:
            deleteFile(self, file_path)
            self.focusOnPath(str(Path(file_path).parent))

    def renameFolderHelper(self, folder_path):
        #helper method to ask the user for a new folder name for a selected folder in the tree view
        path = Path(folder_path)
        old_folder_name = path.name
        new_folder_name, ok = QInputDialog.getText(self, "Rename Folder", "Enter new folder name:", QLineEdit.EchoMode.Normal, old_folder_name)
        renamed_folder_path = renameFolder(self, path, new_folder_name)
        if renamed_folder_path.exists():
            self.focusOnPath(str(renamed_folder_path))
    
    def renameFileHelper(self, file_path):
        #helper method to ask the user for a new folder name for a selected folder in the tree view
        path = Path(file_path)
        old_file_name = path.name
        new_file_name, ok = QInputDialog.getText(self, "Rename File", "Enter new file name:", QLineEdit.EchoMode.Normal, old_file_name)
        renamed_file_path = renameFile(self, path, new_file_name)
        if renamed_file_path.exists():
            self.focusOnPath(str(renamed_file_path))
        
        
    def showErrorMessage(self, error_message):
        #generic message box that shows an error message and does not allow the user to continue unless they accept
        message = QMessageBox(self)
        message.setText(error_message)
        message.exec()

        
    