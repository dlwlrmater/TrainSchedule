from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from call_mainpage import MainPageWindow
from Amap.call_amap import AmapPageWindow
from ctrip.call_ctrip import ctripPageWindow
from keysetting import Ui_Form_mainpage_setkeys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        # self.resize(950, 600)
        # 固定大小
        self.setFixedSize(950, 600)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.Stack = QStackedWidget()
        self.layout.addWidget(self.Stack)
        self.mainPageUi = MainPageWindow()
        self.amapPageUi = AmapPageWindow()
        self.ctripPageUi = ctripPageWindow()

        self.Stack.addWidget(self.mainPageUi)
        self.Stack.addWidget(self.amapPageUi)
        self.Stack.addWidget(self.ctripPageUi)


        # self.ctripPageUi.pushButton_ctrip_more.clicked.connect(self.openmore)
        self.ctripPageUi.pushButton_ctrip_more.setCheckable(True)
        self.ctripPageUi.pushButton_ctrip_more.toggle()
        self.ctripPageUi.pushButton_ctrip_more.clicked.connect(self.btnstate)

        # self.ctripPageUi.pushButton_ctrip_more_confirm.clicked.connect(self.donemore)


        self.mainPageUi.chooseSignal.connect(self.showDialog)


        self.amapPageUi.returnSignal.connect(self.backDialog)
        self.ctripPageUi.returnSignal.connect(self.backDialog)




    def showDialog(self,msg):
        if msg == 'amap':
            self.Stack.setCurrentWidget(self.amapPageUi)
        elif msg == 'ctrip':
            self.Stack.setCurrentWidget(self.ctripPageUi)

    def backDialog(self):
        # self.Stack.setCurrentIndex(0)

        self.ctripPageUi.groupBox_ctrip_more.setHidden(True)
        self.setFixedSize(950, 600)
        self.Stack.setCurrentWidget(self.mainPageUi)

    def btnstate(self):
        if self.ctripPageUi.pushButton_ctrip_more.isChecked():
            # print('checked')
            self.closemore()
        else:
            # print('un checked')
            self.openmore()
            # _ = self.donemore()

    def openmore(self):
        # 如果想隐藏，先调整stack大小
        self.Stack.setFixedSize(1473,600)
        self.setFixedSize(1473, 600)
        self.ctripPageUi.groupBox_ctrip_more.setHidden(False)

    def closemore(self):
        self.Stack.setFixedSize(950, 600)
        self.setFixedSize(950, 600)
        self.ctripPageUi.groupBox_ctrip_more.setHidden(True)


