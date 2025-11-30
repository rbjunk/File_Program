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
    except FileExistsError as e:
        window.showErrorMessage(("Cannot create file \"" + new_file_name + "\" when that file already exists in " + current_directory))

#Create folder
def createNewFolder(window, current_directory, new_folder_name):
    try:
        #attempt to create the new file, otherwise display a message describing the error
        new_folder_location = current_directory+ "/" + new_folder_name
        Path.mkdir(new_folder_location)
    except FileExistsError as e:
        window.showErrorMessage(("Cannot create folder \"" + new_folder_name + "\" when that folder already exists in " + current_directory))