from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal,Qt
from Amap.amap import Ui_MainWindow_amap

class AmapPageWindow(QWidget,Ui_MainWindow_amap):
    #声明信号
    returnSignal = pyqtSignal()

    def __init__(self,parent=None):
        super(AmapPageWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # self.setLayout(self.Form)
        self.pushButton_amap_backmainpage.clicked.connect(self.returnSignal)
        # self.pushButton_amap_routeplan.clicked.connect(self.)
