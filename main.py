import sys
from gui import *
def main():
    app = QApplication(sys.argv)
    controlWindow = mainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()