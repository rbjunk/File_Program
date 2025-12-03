import os
import shutil
from pathlib import Path
from gui import *

#Create file
def createNewFile(window, current_directory, new_file_name):
    try: 
        #attempt to create the new file, otherwise display a message describing the error
        new_file_location = current_directory + "/" + new_file_name
        Path.touch(new_file_location, 0o666, False)
        #load the newly created file into the text editor
        loadFile(window, new_file_location)
        return new_file_location
    except FileExistsError as e:
        window.showErrorMessage(("Cannot create file \"" + new_file_name + "\" when that file already exists in " + current_directory))
        return None
    except PermissionError as e:
        window.showErrorMessage(("Cannot create file \"" + new_file_name + "\" permission denied"))
        return None

#Create folder
def createNewFolder(window, current_directory, new_folder_name):
    try:
        #attempt to create the new file, otherwise display a message describing the error
        new_folder_location = current_directory + "/" + new_folder_name
        Path.mkdir(new_folder_location)
        return new_folder_location
    except FileExistsError as e:
        window.showErrorMessage(("Cannot create folder \"" + new_folder_name + "\" when that folder already exists in " + current_directory))
        return None
    except PermissionError as e:
        window.showErrorMessage(("Cannot create folder \"" + new_folder_name + "\" permission denied"))
        return None

#Load file
def loadFile(window, file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            #load the file into the text editor window
            window.textEditor.setPlainText(text)
            window.textEditor.document().setModified(False)
            window.setWindowTitle(f"Editing - {file_path}")
    except Exception as e:
        window.showErrorMessage("Error loading: {e}")

#Delete File
def deleteFile(window, file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError as e:
        window.showErrorMessage("Error: File not found!")
    except PermissionError as e:
        window.showErrorMessage(("Cannot delete file \"" + file_path + "\" permission denied"))
        
#Delete Folder
def deleteFolder(window, folder_path):
    try:
        shutil.rmtree(folder_path)
    except FileNotFoundError as e:
        window.showErrorMessage("Error: Folder not found!")
    except PermissionError as e:
        window.showErrorMessage(("Cannot delete folder \"" + folder_path + "\" permission denied"))

#Rename Folder
def renameFolder(window, folder_path, new_folder_name):
    try:
        new_folder_path = str(Path(folder_path).parent) + "/" + new_folder_name
        new_folder_path = Path(new_folder_path)
        renamed_folder_path = folder_path.rename(new_folder_path)
        return renamed_folder_path
    except FileNotFoundError as e:
        window.showErrorMessage("Error: Folder not found!")
    except PermissionError as e:
        window.showErrorMessage(("Cannot rename folder \"" + folder_path + "\" permission denied"))
    except FileExistsError as e:
        window.showErrorMessage("Error: Folder alread exists")

#Rename File
def renameFile(window, file_path, new_file_name):
    try:
        new_file_path = str(Path(file_path).parent) + "/" + new_file_name
        new_file_path = Path(new_file_path)
        renamed_file_path = file_path.rename(new_file_path)
        return renamed_file_path
    except FileNotFoundError as e:
        window.showErrorMessage("Error: File not found!")
    except PermissionError as e:
        window.showErrorMessage(("Cannot rename file \"" + file_path + "\" permission denied"))
    except FileExistsError as e:
        window.showErrorMessage("Error: File already exists")

#Save file
def saveFile(window, file_path):
    try:
        #grab text from editor window
        text = window.textEditor.toPlainText()
        #open the file in write mode and write what was in the editor window
        with open(file_path, "w", encoding = "utf-8") as file:
            file.write(text)
        #Reset the modified flag after a successful save
        window.textEditor.document().setModified(False)
        window.showErrorMessage("File saved successfully")
    except Exception as e:
        window.showErrorMessage(f"Error saving: {e}")