from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QErrorMessage, QStyle
from PyQt5.QtCore import pyqtSignal, QTimer, QThread
from PyQt5.QtGui import QImage, QPixmap

import sys
import os

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        ui_design_path = os.path.join(self.current_file_path(),'analysisgui.ui')
        uic.loadUi(ui_design_path, self)
        uic.closeEvent = self.closeEvent
        self.setWindowTitle('SSVEP Analysis Toolbox')
        # get gui elements
        
        # display window
        self.show()
    def current_file_path(self):
        return os.path.dirname(os.path.abspath(__file__))
    def closeEvent(self, event):
        print("Close Main Window")
        event.accept()

def analysisgui():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()

if __name__ == '__main__':
    analysisgui()