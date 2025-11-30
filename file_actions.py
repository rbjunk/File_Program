import os
import shutil
from pathlib import Path
from gui import *

#Create file
def createNewFile(window, current_directory, new_file_name):
    try: 
        #attempt to create the new file, otherwise display a message describing the error
        new_file_location = current_directory+ "/" + new_file_name
        Path.touch(new_file_location, 0o666, False)
        window.statusBar().showMessage(f"Created file: {new_file_location}")
        #load the newly created file into the text editor
        loadFile(window, new_file_location)
    except FileExistsError as e:
        window.showErrorMessage(("Cannot create file \"" + new_file_name + "\" when that file already exists in " + current_directory))
    except PermissionError as e:
        window.showErrorMessage(("Cannot create file \"" + new_file_name + "\" permission denied"))

#Create folder
def createNewFolder(window, current_directory, new_folder_name):
    try:
        #attempt to create the new file, otherwise display a message describing the error
        new_folder_location = current_directory+ "/" + new_folder_name
        Path.mkdir(new_folder_location)
        window.statusBar().showMessage(f"Created folder: {new_folder_location}")
    except FileExistsError as e:
        window.showErrorMessage(("Cannot create folder \"" + new_folder_name + "\" when that folder already exists in " + current_directory))
    except PermissionError as e:
        window.showErrorMessage(("Cannot create folder \"" + new_folder_name + "\" permission denied"))

#Load file
def loadFile(window, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
        #load the file into the text editor window
        window.textEditor.setPlainText(text)
