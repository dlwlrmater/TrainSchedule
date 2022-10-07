from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from mainpage import Ui_MainWindow
from keysetting import Ui_Form_mainpage_setkeys
from PyQt5.QtCore import pyqtSignal,Qt

class MainPageWindow(QMainWindow,Ui_MainWindow):
    #定义点击信号
    chooseSignal = pyqtSignal(str)
    def __init__(self,parent=None):
        super(MainPageWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.ex = Ui_Form_mainpage_setkeys()
        self.pushButton_mainpage_amap.clicked.connect(self.showDialog)
        self.pushButton_mainpage_ctrip.clicked.connect(self.showDialog)
        # self.pushButton_mainpage_baidu.clicked.connect(self.keysettingshow)
        # self.actionkey.triggered.conncet(self.a.show())

    def showDialog(self):
        sender = self.sender()
        if sender == self.pushButton_mainpage_amap:
            #发射点击信号
            self.chooseSignal.emit('amap')
        elif sender == self.pushButton_mainpage_ctrip:
            self.chooseSignal.emit('ctrip')

    # def keysettingshow(self):
    #     self.a = Ui_Form_mainpage_setkeys()
    #     self.a.show()






import sys
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainPageWindow()
    mainWindow.show()
    sys.exit(app.exec_())
