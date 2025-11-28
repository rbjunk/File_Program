import os
import shutil
from pathlib import Path


#Create file
def createNewFile(creation_location):
    Path.touch(creation_location)