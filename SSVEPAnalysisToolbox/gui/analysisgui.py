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
        # program parameters
        self.dataset_container = None
        self.trial_container = None
        self.model_container = None
        self.performance_container = None
        self.trained_model_container = None
        # get gui elements
        self.NewEvaluatorButton = self.findChild(QtWidgets.QPushButton, 'NewEvaluatorButton')
        self.NewEvaluatorButton.setDisabled(False)
        self.MethodSelectButton = self.findChild(QtWidgets.QPushButton, 'MethodSelectButton')
        self.RunButton = self.findChild(QtWidgets.QPushButton, 'RunButton')
        self.RunTimeDisplay = self.findChild(QtWidgets.QLineEdit, 'RunTimeDisplay')
        self.RunTimeDisplay.setReadOnly(True)
        self.ProgressBar = self.findChild(QtWidgets.QProgressBar, 'ProgressBar')
        self.StatusTable = self.findChild(QtWidgets.QTableWidget, 'StatusTable')
        self.PerformTable = self.findChild(QtWidgets.QTableWidget, 'PerformTable')
        self.updateButtons()
        self.updateTables()
        self.updateTime(0)
        self.updateProgress(0)
        # display window
        self.show()
    def updateButtons(self):
        if self.trial_container is None:
            self.NewEvaluatorButton.setText("New Evaluator")
        else:
            self.NewEvaluatorButton.setText("Edit Evaluator")
        if self.trial_container is None:
            self.MethodSelectButton.setDisabled(True)
        else:
            self.MethodSelectButton.setDisabled(False)
        if self.model_container is None:
            self.RunButton.setDisabled(True)
        else:
            self.RunButton.setDisabled(False)
    def updateTime(self, TimeStr):
        if type(TimeStr) is not str:
            TimeStr = str(TimeStr)
        self.RunTimeDisplay.setText(TimeStr)
    def updateProgress(self, val):
        self.ProgressBar.setValue(val)
    def updateStatusTable(self):
        if self.trial_container is None:
            self.StatusTable.clear()
    def updatePerformTable(self):
        if self.performance_container is None:
            self.PerformTable.clear()
    def updateTables(self):
        self.updateStatusTable()
        self.updatePerformTable()
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