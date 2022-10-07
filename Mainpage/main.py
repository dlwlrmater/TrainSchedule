from PyQt5.QtWidgets import *
from mainwindow import MainWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

