import time
import numpy as np
import requests
from lxml import etree
import sys
import datetime

from ctrip.ctripmainpage import Ui_MainWindow_ctrip
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import networkx as nx
from coordinate_transform.coordinate_Transform import *
import re
import itertools


class ctripPageWindow(QWidget,Ui_MainWindow_ctrip):
    #声明信号
    returnSignal = pyqtSignal()

    def __init__(self,parent=None):
        super(ctripPageWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # <高级>隐藏
        self.groupBox_ctrip_more.hide()
        # 替换output图片
        self.pushButton_ctrip_output_address.setStyleSheet(
            "QPushButton{border-image:url(../img/output_not_selection_icon.png)}"
            "QPushButton:hover{border-image:url(../img/output_selection_icon.png)}")
        self.pushButton_ctrip_output_address.setToolTip('output')

        # 如果不点“联系城市统计” 则 特定车站研究不会出现
        self.groupBox_2.setHidden(True)

        # 如果不点 所在地市及坐标 则 特定研究城市不会出现
        self.label_ctrip_targetcity.setHidden(True)
        self.lineEdit_ctrip_targetcity.setHidden(True)

        self.lineEdit_ctrip_typestatisticalindicators.setHidden(True)

        # 等时圈输入默认为隐藏
        self.lineEdit_ctrip_ischrones.setHidden(True)
        # 中心性 隐藏
        self.checkBox_ctrip_betweencentrality.setHidden(True)
        self.checkBox_ctrip_closenesscentrality.setHidden(True)
        self.checkBox_ctrip_degreecentrality.setHidden(True)
        # 坐标选项默认 隐藏
        self.checkBox_ctrip_provincecitylocation.setHidden(True)
        self.checkBox_ctrip_provincecitylocation_wgs84.setHidden(True)
        self.checkBox_ctrip_provincecitylocation_bd09.setHidden(True)

        # targetcity
        self.checkBox_ctrip_targetcity_provincecitylocation.setHidden(True)
        self.checkBox_ctrip_targetcity_provincecitylocation_wgs84.setHidden(True)
        self.checkBox_ctrip_targetcity_provincecitylocation_bd09.setHidden(True)





        # 设置输入数字only
        reg = QRegExp('[0-9]{4}')
        validator = QRegExpValidator(self)
        validator.setRegExp(reg)
        self.lineEdit_ctrip_G_start.setValidator(validator)
        self.lineEdit_ctrip_D_start.setValidator(validator)
        self.lineEdit_ctrip_C_start.setValidator(validator)
        self.lineEdit_ctrip_Z_start.setValidator(validator)
        self.lineEdit_ctrip_T_start.setValidator(validator)
        self.lineEdit_ctrip_K_start.setValidator(validator)
        self.lineEdit_ctrip_Y_start.setValidator(validator)
        self.lineEdit_ctrip_P_start.setValidator(validator)
        self.lineEdit_ctrip_G_end.setValidator(validator)
        self.lineEdit_ctrip_D_end.setValidator(validator)
        self.lineEdit_ctrip_C_end.setValidator(validator)
        self.lineEdit_ctrip_Z_end.setValidator(validator)
        self.lineEdit_ctrip_T_end.setValidator(validator)
        self.lineEdit_ctrip_K_end.setValidator(validator)
        self.lineEdit_ctrip_Y_end.setValidator(validator)
        self.lineEdit_ctrip_P_end.setValidator(validator)
        self.lineEdit_ctrip_timeout.setValidator(QDoubleValidator(0.0, 60.0, 1))

        self.pushButton_ctrip_output_address.clicked.connect(self.openFileaddress)
        self.pushButton_ctrip_output.clicked.connect(self.checkTorF)
        self.pushButton_ctrip_backmainpage.clicked.connect(self.returnSignal)

        self.checkBox_ctrip_targetcity_ischrones.clicked.connect(self.ischrones_timezoneinput)
        self.checkBox_ctrip_directconncetstatistics.clicked.connect(self.statisticsandtargetstation_show)
        self.checkBox_ctrip_provincecitylocation.clicked.connect(self.coordinateandtargetcity_show)
        self.checkBox_ctrip_targetcity_directconncetstatistics.clicked.connect(self.statistics_target_show)
        self.checkBox_ctrip_targetcity_provincecitylocation.clicked.connect(self.coordinate_target_show)
        self.checkBox_ctrip_typestatisticalindicators.clicked.connect(self.typestatisticalindicators)



    def ischrones_timezoneinput(self):
        # self.lineEdit_ctrip_ischrones.setHidden(False)
        if self.checkBox_ctrip_targetcity_ischrones.isChecked():
            self.lineEdit_ctrip_ischrones.setHidden(False)

        else:
            self.lineEdit_ctrip_ischrones.setHidden(True)

    def statisticsandtargetstation_show(self):
        '''
        :return: 勾选 联系城市统计 → 度中心性/中介中心性/接近中心性/特定车站研究出现
        '''
        if self.checkBox_ctrip_directconncetstatistics.isChecked():
            self.checkBox_ctrip_betweencentrality.setHidden(False)
            self.checkBox_ctrip_closenesscentrality.setHidden(False)
            self.checkBox_ctrip_degreecentrality.setHidden(False)
            self.checkBox_ctrip_provincecitylocation.setHidden(False)
            self.groupBox_2.setHidden(False)
        else:

            self.groupBox_2.setHidden(True)
            self.checkBox_ctrip_betweencentrality.setHidden(True)
            self.checkBox_ctrip_closenesscentrality.setHidden(True)
            self.checkBox_ctrip_degreecentrality.setHidden(True)
            self.checkBox_ctrip_provincecitylocation.setHidden(True)

            self.checkBox_ctrip_betweencentrality.setChecked(False)
            self.checkBox_ctrip_closenesscentrality.setChecked(False)
            self.checkBox_ctrip_degreecentrality.setChecked(False)
            self.checkBox_ctrip_provincecitylocation.setChecked(False)

            self.checkBox_ctrip_provincecitylocation_wgs84.setHidden(True)
            self.checkBox_ctrip_provincecitylocation_bd09.setHidden(True)
            self.checkBox_ctrip_provincecitylocation_wgs84.setChecked(False)
            self.checkBox_ctrip_provincecitylocation_bd09.setChecked(False)

    def statistics_target_show(self):
        if self.checkBox_ctrip_targetcity_directconncetstatistics.isChecked():
            self.checkBox_ctrip_targetcity_provincecitylocation.setHidden(False)
        else:
            self.checkBox_ctrip_targetcity_provincecitylocation_wgs84.setHidden(True)
            self.checkBox_ctrip_targetcity_provincecitylocation_bd09.setHidden(True)
            self.checkBox_ctrip_targetcity_provincecitylocation.setHidden(True)
            self.checkBox_ctrip_targetcity_provincecitylocation_wgs84.setChecked(False)
            self.checkBox_ctrip_targetcity_provincecitylocation_bd09.setChecked(False)
            self.checkBox_ctrip_targetcity_provincecitylocation.setChecked(False)

    def typestatisticalindicators(self):
        if self.checkBox_ctrip_typestatisticalindicators.isChecked():
            self.lineEdit_ctrip_typestatisticalindicators.setHidden(False)
        else:
            self.lineEdit_ctrip_typestatisticalindicators.setHidden(True)

    def coordinateandtargetcity_show(self):
        if self.checkBox_ctrip_provincecitylocation.isChecked():
            self.checkBox_ctrip_provincecitylocation_wgs84.setHidden(False)
            self.checkBox_ctrip_provincecitylocation_bd09.setHidden(False)
            self.label_ctrip_targetcity.setHidden(False)
            self.lineEdit_ctrip_targetcity.setHidden(False)
        else:
            self.checkBox_ctrip_provincecitylocation_wgs84.setHidden(True)
            self.checkBox_ctrip_provincecitylocation_bd09.setHidden(True)
            self.checkBox_ctrip_provincecitylocation_wgs84.setChecked(False)
            self.checkBox_ctrip_provincecitylocation_bd09.setChecked(False)
            self.label_ctrip_targetcity.setHidden(True)
            self.lineEdit_ctrip_targetcity.setHidden(True)

    def coordinate_target_show(self):
        if self.checkBox_ctrip_targetcity_provincecitylocation.isChecked():
            self.checkBox_ctrip_targetcity_provincecitylocation_wgs84.setHidden(False)
            self.checkBox_ctrip_targetcity_provincecitylocation_bd09.setHidden(False)
        else:
            self.checkBox_ctrip_targetcity_provincecitylocation_wgs84.setHidden(True)
            self.checkBox_ctrip_targetcity_provincecitylocation_bd09.setHidden(True)
            self.checkBox_ctrip_targetcity_provincecitylocation_wgs84.setChecked(False)
            self.checkBox_ctrip_targetcity_provincecitylocation_bd09.setChecked(False)

    def openFileaddress(self):
        self.cwd = os.getcwd()
        fd, ok = QFileDialog.getOpenFileName(self, '文件保存', self.cwd,
                                             'Excel Files (*.xlsx);;Text Files (*.txt);;All Files (*.*)')
        self.lineEdit_ctrip_output_address.setText(fd)

    # 1.在导出之前检查各项指标是否合乎规则
    def checkTorF(self):
        '''
        如果在<特定研究车站>lines里面输入了文字 确保起码勾选了一个targetcity_checkbox
        ！如果模块里面有更新新的checkbox,还需要更新
        '''
        if self.checkBox_ctrip_targetcity_odlines.isChecked() == False and self.checkBox_ctrip_targetcity_directconncetstatistics.isChecked() == False and self.checkBox_ctrip_targetcity_ischrones.isChecked() == False and self.checkBox_ctrip_targetcity_directconncetmatrix.isChecked() == False and self.checkBox_ctrip_directconncetmatrix.isChecked() == False:
            # print('a')
            self.label_ctrip_targetstations_model.setStyleSheet('color:red')
            QMessageBox.warning(self, 'error', '没选择')
        else:
            self.label_ctrip_targetstations_model.setStyleSheet('color:black')
            if self.lineEdit_ctrip_timeout.text() == '' or (float(self.lineEdit_ctrip_timeout.text()) >= 0 and float(self.lineEdit_ctrip_timeout.text()) <= 60):
                wrongcount = 0
                if self.checkBox_ctrip_G.isChecked() == False and self.checkBox_ctrip_D.isChecked() == False and self.checkBox_ctrip_C.isChecked() == False and self.checkBox_ctrip_Z.isChecked() == False and self.checkBox_ctrip_T.isChecked() == False and self.checkBox_ctrip_K.isChecked() == False and self.checkBox_ctrip_Y.isChecked() == False and self.checkBox_ctrip_P.isChecked() == False and self.checkBox_ctrip_S.isChecked() == False:
                    QMessageBox.warning(self, 'Error', '未选择类型')
                else:
                    if self.checkBox_ctrip_G.isChecked() == False:
                        if self.lineEdit_ctrip_G_start.text() != '' or self.lineEdit_ctrip_G_end.text() != '':
                            QMessageBox.warning(self, 'G', 'G打钩')
                            self.checkBox_ctrip_G.setStyleSheet('color:red')
                            wrongcount += 1
                    else:
                        if self.lineEdit_ctrip_G_start.text() != '' and self.lineEdit_ctrip_G_end.text() != '' and int(self.lineEdit_ctrip_G_start.text()) > int(self.lineEdit_ctrip_G_end.text()):
                            QMessageBox.warning(self, 'G开头高级选项', 'start数值应小于end')
                            self.lineEdit_ctrip_G_start.setStyleSheet('color:red')
                            self.lineEdit_ctrip_G_end.setStyleSheet('color:red')
                            wrongcount += 1

                    if self.checkBox_ctrip_D.isChecked() == False:
                        if self.lineEdit_ctrip_D_start.text() != '' or self.lineEdit_ctrip_D_end.text() != '':
                            QMessageBox.warning(self, 'D', 'D打钩')
                            self.checkBox_ctrip_D.setStyleSheet('color:red')
                            wrongcount += 1
                    else:
                        if self.lineEdit_ctrip_D_start.text() != '' and self.lineEdit_ctrip_D_end.text() != '' and int(
                                self.lineEdit_ctrip_D_start.text()) > int(self.lineEdit_ctrip_D_end.text()):
                            QMessageBox.warning(self, 'D开头高级选项', 'start数值应小于end')
                            self.lineEdit_ctrip_D_start.setStyleSheet('color:red')
                            self.lineEdit_ctrip_D_end.setStyleSheet('color:red')
                            wrongcount += 1

                    if self.checkBox_ctrip_C.isChecked() == False:
                        if self.lineEdit_ctrip_C_start.text() != '' or self.lineEdit_ctrip_C_end.text() != '':
                            QMessageBox.warning(self, 'C', 'C打钩')
                            self.checkBox_ctrip_C.setStyleSheet('color:red')
                            wrongcount += 1
                    else:
                        if self.lineEdit_ctrip_C_start.text() != '' and self.lineEdit_ctrip_C_end.text() != '' and int(
                                self.lineEdit_ctrip_C_start.text()) > int(self.lineEdit_ctrip_C_end.text()):
                            QMessageBox.warning(self, 'C开头高级选项', 'start数值应小于end')
                            self.lineEdit_ctrip_C_start.setStyleSheet('color:red')
                            self.lineEdit_ctrip_C_end.setStyleSheet('color:red')
                            wrongcount += 1

                    if self.checkBox_ctrip_Z.isChecked() == False:
                        if self.lineEdit_ctrip_Z_start.text() != '' or self.lineEdit_ctrip_Z_end.text() != '':
                            QMessageBox.warning(self, 'Z', 'Z打钩')
                            self.checkBox_ctrip_Z.setStyleSheet('color:red')
                            wrongcount += 1
                    else:
                        if self.lineEdit_ctrip_Z_start.text() != '' and self.lineEdit_ctrip_Z_end.text() != '' and int(
                                self.lineEdit_ctrip_Z_start.text()) > int(self.lineEdit_ctrip_Z_end.text()):
                            QMessageBox.warning(self, 'Z开头高级选项', 'start数值应小于end')
                            self.lineEdit_ctrip_Z_start.setStyleSheet('color:red')
                            self.lineEdit_ctrip_Z_end.setStyleSheet('color:red')
                            wrongcount += 1

                    if self.checkBox_ctrip_T.isChecked() == False:
                        if self.lineEdit_ctrip_T_start.text() != '' or self.lineEdit_ctrip_T_end.text() != '':
                            QMessageBox.warning(self, 'T', 'T打钩')
                            self.checkBox_ctrip_T.setStyleSheet('color:red')
                            wrongcount += 1
                    else:
                        if self.lineEdit_ctrip_T_start.text() != '' and self.lineEdit_ctrip_T_end.text() != '' and int(
                                self.lineEdit_ctrip_T_start.text()) > int(self.lineEdit_ctrip_T_end.text()):
                            QMessageBox.warning(self, 'T开头高级选项', 'start数值应小于end')
                            self.lineEdit_ctrip_T_start.setStyleSheet('color:red')
                            self.lineEdit_ctrip_T_end.setStyleSheet('color:red')
                            wrongcount += 1

                    if self.checkBox_ctrip_K.isChecked() == False:
                        if self.lineEdit_ctrip_K_start.text() != '' or self.lineEdit_ctrip_K_end.text() != '':
                            QMessageBox.warning(self, 'K', 'K打钩')
                            self.checkBox_ctrip_K.setStyleSheet('color:red')
                            wrongcount += 1
                    else:
                        if self.lineEdit_ctrip_K_start.text() != '' and self.lineEdit_ctrip_K_end.text() != '' and int(
                                self.lineEdit_ctrip_K_start.text()) > int(self.lineEdit_ctrip_K_end.text()):
                            QMessageBox.warning(self, 'K开头高级选项', 'start数值应小于end')
                            self.lineEdit_ctrip_K_start.setStyleSheet('color:red')
                            self.lineEdit_ctrip_K_end.setStyleSheet('color:red')
                            wrongcount += 1

                    if self.checkBox_ctrip_Y.isChecked() == False:
                        if self.lineEdit_ctrip_Y_start.text() != '' or self.lineEdit_ctrip_Y_end.text() != '':
                            QMessageBox.warning(self, 'Y', 'Y打钩')
                            self.checkBox_ctrip_Y.setStyleSheet('color:red')
                            wrongcount += 1
                    else:
                        if self.lineEdit_ctrip_Y_start.text() != '' and self.lineEdit_ctrip_Y_end.text() != '' and int(
                                self.lineEdit_ctrip_Y_start.text()) > int(self.lineEdit_ctrip_Y_end.text()):
                            QMessageBox.warning(self, 'Y开头高级选项', 'start数值应小于end')
                            self.lineEdit_ctrip_Y_start.setStyleSheet('color:red')
                            self.lineEdit_ctrip_Y_end.setStyleSheet('color:red')
                            wrongcount += 1

                    if self.checkBox_ctrip_P.isChecked() == False:
                        if self.lineEdit_ctrip_P_start.text() != '' or self.lineEdit_ctrip_P_end.text() != '':
                            QMessageBox.warning(self, '普', '普打钩')
                            self.checkBox_ctrip_P.setStyleSheet('color:red')
                            wrongcount += 1
                    else:
                        if self.lineEdit_ctrip_P_start.text() != '' and self.lineEdit_ctrip_P_end.text() != '' and int(
                                self.lineEdit_ctrip_P_start.text()) > int(self.lineEdit_ctrip_P_end.text()):
                            QMessageBox.warning(self, 'P开头高级选项', 'start数值应小于end')
                            self.lineEdit_ctrip_P_start.setStyleSheet('color:red')
                            self.lineEdit_ctrip_P_end.setStyleSheet('color:red')
                            wrongcount += 1

                    if self.checkBox_ctrip_S.isChecked() == False:
                        if self.lineEdit_ctrip_S_start.text() != '' or self.lineEdit_ctrip_S_end.text() != '':
                            QMessageBox.warning(self, 'S', 'S打钩')
                            self.checkBox_ctrip_S.setStyleSheet('color:red')
                            wrongcount += 1
                    else:
                        if self.lineEdit_ctrip_S_start.text() != '' and self.lineEdit_ctrip_S_end.text() != '' and int(
                                self.lineEdit_ctrip_S_start.text()) > int(self.lineEdit_ctrip_S_end.text()):
                            QMessageBox.warning(self, 'S开头高级选项', 'start数值应小于end')
                            self.lineEdit_ctrip_S_start.setStyleSheet('color:red')
                            self.lineEdit_ctrip_S_end.setStyleSheet('color:red')
                            wrongcount += 1

                    if self.checkBox_ctrip_targetcity_ischrones.isChecked():
                        input_ischrones = self.lineEdit_ctrip_ischrones.text()
                        sp = input_ischrones.split(',')
                        for i in sp:
                            if ('mins' not in i) and ('h' not in i):
                                QMessageBox.warning(self,'等时圈输入Error','输入数据只能以mins/h结尾')
                                self.lineEdit_ctrip_ischrones.setStyleSheet('color:red')
                                wrongcount += 1

                    if self.checkBox_ctrip_typestatisticalindicators.isChecked():
                        if self.lineEdit_ctrip_typestatisticalindicators.text() != '':
                            # 正则表达式 以[GDCZTKYSP]开头 [GDCZTKYSP]结尾
                            pattern = '^[GDCZTKYSP][GDCZTKYSP/]*[GDCZTKYSP]$'
                            prog = re.compile(pattern)
                            ReE = prog.match(self.lineEdit_ctrip_typestatisticalindicators.text())
                            if ReE != None:
                                self.lineEdit_ctrip_typestatisticalindicators.setStyleSheet('color:black')
                                self.typelist = self.lineEdit_ctrip_typestatisticalindicators.text().split('/')
                            else:
                                self.lineEdit_ctrip_typestatisticalindicators.setStyleSheet('color:red')
                                QMessageBox.warning(self, 'Error', '根据数据类型分别统计指标输入错误，不符合要求')
                                wrongcount +=1
                        else:
                            self.typelist = []

                    if wrongcount == 0:
                        _ = self.beforewebcrawler()
            else:
                QMessageBox.warning(self, '暂停时间', '时间范围为0.0~60.0')
                self.lineEdit_ctrip_timeout.setStyleSheet('color:red')

    # 2.根据'高级'设置 数据爬取前期准备
    def beforewebcrawler(self):
        # 得到要爬取的范围
        l = {}
        if self.checkBox_ctrip_G.isChecked():
            st = self.lineEdit_ctrip_G_start.placeholderText()[1:]
            en = self.lineEdit_ctrip_G_end.placeholderText()[1:]
            if self.lineEdit_ctrip_G_start.text() != '':
                l['G'] = [int(self.lineEdit_ctrip_G_start.text()), int(en) + 1]
                if self.lineEdit_ctrip_G_end.text() != '':
                    l['G'] = [int(self.lineEdit_ctrip_G_start.text()), int(self.lineEdit_ctrip_G_end.text()) + 1]
            else:
                if self.lineEdit_ctrip_G_end.text() != '':
                    l['G'] = [int(st), int(self.lineEdit_ctrip_G_end.text()) + 1]
                else:
                    l['G'] = [int(st), int(en) + 1]
            self.checkBox_ctrip_G.setStyleSheet('color:black')

        if self.checkBox_ctrip_D.isChecked():
            st = self.lineEdit_ctrip_D_start.placeholderText()[1:]
            en = self.lineEdit_ctrip_D_end.placeholderText()[1:]
            if self.lineEdit_ctrip_D_start.text() != '':
                l['D'] = [int(self.lineEdit_ctrip_D_start.text()), int(en) + 1]
                if self.lineEdit_ctrip_D_end.text() != '':
                    l['D'] = [int(self.lineEdit_ctrip_D_start.text()), int(self.lineEdit_ctrip_D_end.text()) + 1]
            else:
                if self.lineEdit_ctrip_D_end.text() != '':
                    l['D'] = [int(st), int(self.lineEdit_ctrip_D_end.text()) + 1]
                else:
                    l['D'] = [int(st), int(en) + 1]
            self.checkBox_ctrip_D.setStyleSheet('color:black')

        if self.checkBox_ctrip_C.isChecked():
            st = self.lineEdit_ctrip_C_start.placeholderText()[1:]
            en = self.lineEdit_ctrip_C_end.placeholderText()[1:]
            if self.lineEdit_ctrip_C_start.text() != '':
                l['C'] = [int(self.lineEdit_ctrip_C_start.text()), int(en) + 1]
                if self.lineEdit_ctrip_C_end.text() != '':
                    l['C'] = [int(self.lineEdit_ctrip_C_start.text()), int(self.lineEdit_ctrip_C_end.text()) + 1]
            else:
                if self.lineEdit_ctrip_C_end.text() != '':
                    l['C'] = [int(st), int(self.lineEdit_ctrip_C_end.text()) + 1]
                else:
                    l['C'] = [int(st), int(en) + 1]
            self.checkBox_ctrip_C.setStyleSheet('color:black')

        if self.checkBox_ctrip_Z.isChecked():
            st = self.lineEdit_ctrip_Z_start.placeholderText()[1:]
            en = self.lineEdit_ctrip_Z_end.placeholderText()[1:]
            if self.lineEdit_ctrip_Z_start.text() != '':
                l['Z'] = [int(self.lineEdit_ctrip_Z_start.text()), int(en) + 1]
                if self.lineEdit_ctrip_Z_end.text() != '':
                    l['Z'] = [int(self.lineEdit_ctrip_Z_start.text()), int(self.lineEdit_ctrip_Z_end.text()) + 1]
            else:
                if self.lineEdit_ctrip_Z_end.text() != '':
                    l['Z'] = [int(st), int(self.lineEdit_ctrip_Z_end.text()) + 1]
                else:
                    l['Z'] = [int(st), int(en) + 1]
            self.checkBox_ctrip_Z.setStyleSheet('color:black')

        if self.checkBox_ctrip_T.isChecked():
            st = self.lineEdit_ctrip_T_start.placeholderText()[1:]
            en = self.lineEdit_ctrip_T_end.placeholderText()[1:]
            if self.lineEdit_ctrip_T_start.text() != '':
                l['T'] = [int(self.lineEdit_ctrip_T_start.text()), int(en) + 1]
                if self.lineEdit_ctrip_T_end.text() != '':
                    l['T'] = [int(self.lineEdit_ctrip_T_start.text()), int(self.lineEdit_ctrip_T_end.text()) + 1]
            else:
                if self.lineEdit_ctrip_T_end.text() != '':
                    l['T'] = [int(st), int(self.lineEdit_ctrip_T_end.text()) + 1]
                else:
                    l['T'] = [int(st), int(en) + 1]
            self.checkBox_ctrip_T.setStyleSheet('color:black')

        if self.checkBox_ctrip_K.isChecked():
            st = self.lineEdit_ctrip_K_start.placeholderText()[1:]
            en = self.lineEdit_ctrip_K_end.placeholderText()[1:]
            if self.lineEdit_ctrip_K_start.text() != '':
                l['K'] = [int(self.lineEdit_ctrip_K_start.text()), int(en) + 1]
                if self.lineEdit_ctrip_K_end.text() != '':
                    l['K'] = [int(self.lineEdit_ctrip_K_start.text()), int(self.lineEdit_ctrip_K_end.text()) + 1]
            else:
                if self.lineEdit_ctrip_K_end.text() != '':
                    l['K'] = [int(st), int(self.lineEdit_ctrip_K_end.text()) + 1]
                else:
                    l['K'] = [int(st), int(en) + 1]
            self.checkBox_ctrip_K.setStyleSheet('color:black')

        if self.checkBox_ctrip_Y.isChecked():
            st = self.lineEdit_ctrip_Y_start.placeholderText()[1:]
            en = self.lineEdit_ctrip_Y_end.placeholderText()[1:]
            if self.lineEdit_ctrip_Y_start.text() != '':
                l['Y'] = [int(self.lineEdit_ctrip_Y_start.text()), int(en) + 1]
                if self.lineEdit_ctrip_Y_end.text() != '':
                    l['Y'] = [int(self.lineEdit_ctrip_Y_start.text()), int(self.lineEdit_ctrip_Y_end.text()) + 1]
            else:
                if self.lineEdit_ctrip_Y_end.text() != '':
                    l['Y'] = [int(st), int(self.lineEdit_ctrip_Y_end.text()) + 1]
                else:
                    l['Y'] = [int(st), int(en) + 1]
            self.checkBox_ctrip_Y.setStyleSheet('color:black')

        if self.checkBox_ctrip_P.isChecked():
            st = self.lineEdit_ctrip_P_start.placeholderText()
            en = self.lineEdit_ctrip_P_end.placeholderText()
            if self.lineEdit_ctrip_P_start.text() != '':
                l[''] = [int(self.lineEdit_ctrip_P_start.text()), int(en) + 1]
                if self.lineEdit_ctrip_P_end.text() != '':
                    l[''] = [int(self.lineEdit_ctrip_P_start.text()), int(self.lineEdit_ctrip_P_end.text()) + 1]
            else:
                if self.lineEdit_ctrip_P_end.text() != '':
                    l[''] = [int(st), int(self.lineEdit_ctrip_P_end.text()) + 1]
                else:
                    l[''] = [int(st), int(en) + 1]
            self.checkBox_ctrip_P.setStyleSheet('color:black')

        if self.checkBox_ctrip_S.isChecked():
            st = self.lineEdit_ctrip_S_start.placeholderText()[1:]
            en = self.lineEdit_ctrip_S_end.placeholderText()[1:]
            if self.lineEdit_ctrip_S_start.text() != '':
                l['S'] = [int(self.lineEdit_ctrip_S_start.text()), int(en) + 1]
                if self.lineEdit_ctrip_S_end.text() != '':
                    l['S'] = [int(self.lineEdit_ctrip_S_start.text()), int(self.lineEdit_ctrip_S_end.text()) + 1]
            else:
                if self.lineEdit_ctrip_S_end.text() != '':
                    l['S'] = [int(st), int(self.lineEdit_ctrip_S_end.text()) + 1]
                else:
                    l['S'] = [int(st), int(en) + 1]
            self.checkBox_ctrip_S.setStyleSheet('color:black')

        # 爬取时间间隔
        if self.lineEdit_ctrip_timeout.text() == '':
            self.timebreak = self.lineEdit_ctrip_timeout.placeholderText()[3:].split('s')[0]
        else:
            self.timebreak = self.lineEdit_ctrip_timeout.text()


        # 基础sheet
        _ = self.gdb(l)

    # 3.检查路径输出
    def checkoutputaddress(self):
        QMessageBox.warning(self, 'ERROR', '无输出路径')

    # 4.基础数据(getdatabase) 包含target
    def gdb(self,l):
        '''
        :param l:为需要爬去的车次名 like G1~G101
        :return: 输出 sheet-base
        '''
        # 路径输出检查
        if self.lineEdit_ctrip_output_address.text() == '':
            _ = self.checkoutputaddress()
        else:
            filename = self.lineEdit_ctrip_output_address.text()
            name = []
            OD = []
            result_lst = []
            result_str = []
            pathid = 0
            linetype = []
            jinzhantime = []
            fachetime = []
            for i in list(l.keys()):
                for j in trange(l[i][0], l[i][1]):
                    checi = str(i) + str(j)
                    pathid += 1
                    url = 'https://trains.ctrip.com/trainbooking/TrainSchedule/' + checi + '/'
                    r = requests.get(url, timeout=100)
                    et = etree.HTML(r.content.decode('utf-8'))
                    # 查看多少个站
                    line = et.xpath('//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[2]/tbody//tr')
                    length = len(line)
                    if line == []:
                        pass
                    else:
                        lline = []
                        jinzhantime1 = []
                        fachetime1 = []
                        for a in range(length):
                            lline.append(et.xpath('//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[2]/tbody//tr[' + str(a + 1) + '] / td[3]/text()')[0])
                            jinzhantime1.append(et.xpath('//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[2]/tbody//tr[' + str(a + 1) + '] / td[4]/text()')[0])
                            fachetime1.append(et.xpath('//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[2]/tbody//tr[' + str(a + 1) + '] / td[5]/text()')[0])
                        name.append(checi)
                        OD.append(lline[0]+','+lline[-1])
                        result_lst.append(lline)
                        jinzhantime.append(jinzhantime1)
                        fachetime.append(fachetime1)
                        linetype.append(i)
                    if pathid % 10 == 0:
                        time.sleep(float(self.timebreak))
            # result1为str 方便在csv里面看
            for i in result_lst:
                z = ','.join(i)
                result_str.append(z)
            df = pd.DataFrame({'banci': name, 'od': OD, 'way': result_str, 'linetype':linetype, '进站时间':jinzhantime, '发车时间':fachetime})
            df_forstatistics = pd.DataFrame({'banci':name,'linetype':linetype,'way_lst':result_lst})

            writer = pd.ExcelWriter(filename)
            # base sheet
            df.to_excel(writer, sheet_name='base')

            # ！做个测试
            # df = pd.read_csv(r'携程铁路_GDC.csv',index_col=0)
            # df_forstatistics = pd.read_csv(r'携程铁路_GDC.csv',index_col=0)

            '''
            根据模块勾选，选择def
            '''
            # 分析matrix
            if self.checkBox_ctrip_directconncetmatrix.isChecked():
                _ = self.directconnectmatrix(result_lst, writer)
            # 分析lines
            '''
            三种情况
            1.点了 没填任何东西 → G/D/C/Z/T
            2.点了 填了GD/DC → GD / DC
            2.没点 → GDCZT
            中心性：
            1.分开统计/多个sheet
            2.根据typelist合并统计/根据分类多个sheet
            3.合起来统计/一个sheet
            所在地市及坐标
            合并去重统计
            
            '''
            if self.checkBox_ctrip_directconncetstatistics.isChecked():
                if self.checkBox_ctrip_provincecitylocation.isChecked():
                    self.df_provincecitylocation = self.getcoordinate(result_lst, linetype, writer)
                if self.checkBox_ctrip_typestatisticalindicators.isChecked() and len(self.typelist) == 0:
                    for i in ['G','D','C','Z','T','K','Y','S','P']:
                        result_lst = df_forstatistics[df_forstatistics['linetype'] == i]['way_lst'].values
                        if len(result_lst) == 0:
                            pass
                        else:
                            df_directconnect = self.directconnectstatistics(result_lst, writer)
                            # 度中心性
                            if self.checkBox_ctrip_degreecentrality.isChecked():
                                _ = self.degreecentrality(df_directconnect, writer,i)
                            # 中介中心性
                            if self.checkBox_ctrip_betweencentrality.isChecked():
                                _ = self.betweennesscentrality(df_directconnect,writer,i)
                            # 接近中心性
                            if self.checkBox_ctrip_closenesscentrality.isChecked():
                                _ = self.closenesscentrality(df_directconnect,writer,i)
                            df_provincecitylocation_selection = self.df_provincecitylocation[self.df_provincecitylocation['linetype'] == i]
                            df_provincecitylocation_selection.to_excel(writer,sheet_name=i+'_涉及城市及坐标')
                elif self.checkBox_ctrip_typestatisticalindicators.isChecked() and len(self.typelist) > 0:
                    for i in self.typelist:
                        # df_directconnect_typelist like 北京,上海,10 上海,北京,10
                        result_lst = df_forstatistics[df_forstatistics['linetype'].map(lambda x: x in set(i))]['way_lst'].values
                        df_directconnect_typelist = self.directconnectstatistics(result_lst, writer, i)
                        # 度中心性
                        if self.checkBox_ctrip_degreecentrality.isChecked():
                            _ = self.degreecentrality(df_directconnect_typelist, writer,i)
                        # 中介中心性
                        if self.checkBox_ctrip_betweencentrality.isChecked():
                            _ = self.betweennesscentrality(df_directconnect_typelist, writer,i)
                        # 接近中心性
                        if self.checkBox_ctrip_closenesscentrality.isChecked():
                            _ = self.closenesscentrality(df_directconnect_typelist, writer,i)
                        # 坐标转换
                        df_provincecitylocation_selection = self.df_provincecitylocation[self.df_provincecitylocation['linetype'].map(lambda x:x in set(i))]
                        df_provincecitylocation_selection.to_excel(writer, sheet_name=i + '_涉及车站所在城市及坐标')
                        # if self.checkBox_ctrip_provincecitylocation.isChecked():
                        #     # result_lst = df_forstatistics[df_forstatistics['linetype'].map(lambda x:x in set(i))]
                        #     self.df_provincecitylocation = self.getcoordinate(result_lst, writer,i)
                elif self.checkBox_ctrip_typestatisticalindicators.isChecked() == False:
                    df_directconnect = self.directconnectstatistics(result_lst, writer)
                    # 度中心性
                    if self.checkBox_ctrip_degreecentrality.isChecked():
                        _ = self.degreecentrality(df_directconnect, writer)
                    # 中介中心性
                    if self.checkBox_ctrip_betweencentrality.isChecked():
                        _ = self.betweennesscentrality(df_directconnect,writer)
                    # 接近中心性
                    if self.checkBox_ctrip_closenesscentrality.isChecked():
                        _ = self.closenesscentrality(df_directconnect,writer)
                    self.df_provincecitylocation.to_excel(writer,sheet_name='涉及车站所在城市及坐标')



            '''
            需要研究的城市
            都在这个if下面解决
            ！target_city是否需要centrality
            '''
            if self.lineEdit_ctrip_targetstations.text() != '':
                self.targetline = self.lineEdit_ctrip_targetstations.text().replace('站', '').replace('，', ',').split(',')
                for i in self.targetline:
                    writer_target = pd.ExcelWriter(filename.split('.')[0]+'_'+i+'站.xlsx')
                    df_target = df[[i in j for j in df['way']]]
                    df_target_lst = df_forstatistics[[i in j for j in df_forstatistics['way_lst']]]

                    result_lst_target = df_target_lst['way_lst'].tolist()
                    linetype_target = df_target_lst['linetype'].tolist()
                    df_target.to_excel(writer_target,sheet_name='爬取数据中包含'+i+'站字段的')
                    # 为起终点线路
                    if self.checkBox_ctrip_targetcity_odlines.isChecked():
                        _ = self.targetcity_odlines(i,df_target, writer_target)
                    # 直联车站统计
                    if self.checkBox_ctrip_targetcity_directconncetstatistics.isChecked():
                        df_targetcity_directconnect = self.targetcity_directconnectstatistics(i, result_lst, writer_target)
                    # timezone = '30mins,1h,1.5h,120mins'
                    # 等时圈
                    if self.checkBox_ctrip_targetcity_ischrones.isChecked():
                        _ = self.targetcity_ischrones(i, result_lst, jinzhantime, fachetime, self.lineEdit_ctrip_ischrones.text(), writer_target)
                    # 所在地市及坐标
                    df_target_station = []
                    for i in df_target:
                        z = i.split(',')
                        for j in z:
                            if j not in df_target_station:
                                df_target_station.append(j)
                    '''
                    关于车站坐标取得的3种情景
                    1.整体模块√,特定车站√
                        那只需要根据目标研究车站/目标研究城市从整理好的self.df_provincecitylocation拿即可
                           name   linetype  province  city    adname   lng_gcj02  lat_gcj02  lng_wgs84  lat_wgs84    lng_bd09   lat_bd09
                        0  广州北  G         广东省     广州市   花都区  113.203846  23.377273  113.19847   23.37984  113.210374  23.383044
                    2.整体模块×,特定车站√
                        
                    '''

                    if self.checkBox_ctrip_targetcity_provincecitylocation.isChecked():
                        if self.checkBox_ctrip_provincecitylocation.isChecked():
                            df_provincecitylocation_target = self.df_provincecitylocation[self.df_provincecitylocation['name'].map(lambda x:x in df_target_station)]
                            df_provincecitylocation_target.to_excel(writer,sheet_name=i+'站_涉及城市及坐标')
                        else:
                            df_provincecitylocation_sum_target = self.getcoordinate(result_lst_target,linetype,writer_target)

                        # _ = self.getcoordinate(result_lst, writer_target)


                    writer_target.save()

            # 保存excel
            writer.save()
            QMessageBox.about(self, 'output', 'successed!')
            self.lineEdit_ctrip_timeout.setStyleSheet('color:black')


    # 直接联系城市矩阵
    def directconnectmatrix(self,result,writer):
        '''
        :param result: [['北京','上海'],['上海','武汉']]
        :param writer:xlsx文件
        :return:
        '''
        # 路径里头所有的站名
        lst_all = []
        # 路径里头按每个班次分的list
        lst_all2 = []
        for x in pd.Series(result):
            lst_all.extend(x)
            lst_all2.append(x)
        # 做matrix行列的值
        lst_unique = pd.unique(lst_all)
        # 所需要的度中心性格式的list 坐标格式
        lst_all3 = []
        for a in range(len(lst_all2)):
            for b, c in zip(range(len(lst_all2[a])), range(1, len(lst_all2[a]))):
                zuobiao = [lst_all2[a][b], lst_all2[a][c]]
                lst_all3.append(zuobiao)
        zero_matrix = np.zeros((len(lst_unique), len(lst_unique)))
        result_matrix = pd.DataFrame(zero_matrix, columns=lst_unique, index=lst_unique)
        for d, e in lst_all3:
            f = list(lst_unique).index(d)
            g = list(lst_unique).index(e)
            result_matrix.iloc[f, g] += 1
        result_matrix.to_excel(writer, sheet_name='matrix')

    # 直接联系城市统计
    def directconnectstatistics(self,result,writer,i=None):
        '''
        :param result: list  [['北京','上海'],['上海','武汉']]
        :param writer:xlsx文件
        :return: df_directconnect ['武汉','咸宁北',14]
        '''
        # 路径里头按每个班次分的list
        lst_all2 = []
        lst = []
        for x in result:
            lst_all2.append(x)
        for i in result:
            for j in range(len(i)-1):
                lst.append([i[j],i[j+1]])
        # print(lst)
        df = pd.Series(lst).value_counts()
        ddf = pd.DataFrame()
        ddf['o'] = [i[0] for i in df.index.tolist()]
        ddf['d'] = [i[1] for i in df.index.tolist()]
        ddf['统计次数'] = df.values
        if i == None:
            ddf.to_excel(writer, sheet_name='直接联系车站之间统计')
        else:
            ddf.to_excel(writer,sheet_name=i+'类型_直接联系车站之间统计')
        # if self.checkBox_ctrip_degreecentrality.isChecked():
        return ddf
        # if 1 ==1 :
        #     lines
        #     O = []
        #     D = []
        #     nums = []
        #     for a1 in range(len(lst_unique)):
        #         for a2 in range(len(lst_unique)):
        #             if a1 == a2:
        #                 pass
        #             else:
        #                 h1 = lst_unique[a1]
        #                 h2 = lst_unique[a2]
        #
        #                 h3 = list(lst_unique).index(h1)
        #                 h4 = list(lst_unique).index(h2)
        #                 num = result_matrix.iloc[h3, h4]
        #                 if num == 0:
        #                     pass
        #                 else:
        #                     O.append(h1)
        #                     D.append(h2)
        #                     nums.append(num)
        #     result_line = pd.DataFrame(list(zip(O, D, nums)), columns=['O', 'D', 'nums'])
        #     result_line = result_line.sort_values(by='nums', ascending=False)
        #     result_line.to_excel(writer, sheet_name='lines')

    # 坐标
    def getcoordinate(self,result,linetype,writer):
        '''
        :param result: list [['北京','上海'],['上海','北京']
        :param linetype: list [['G'],['G']]
        :param writer:
        :param i: 需要研究的类型 like G/D/C
        :return:
        '''
        lst_unique_station = []
        city_type = []
        # len_result = len(result)
        # for i in range(len_result):
        #     for j in result[i]:
        #         print(j)
        #         if j not in lst_unique_station:
        #             lst_unique_station.append(j)

        # ！
        for x,j in zip(result,linetype):
            for z in itertools.product(x,j):
                city_type.append(z)
                if z[0] not in lst_unique_station:
                    lst_unique_station.append(z[0])
        df = pd.DataFrame(set(city_type),columns=['name','linetype'])

        # for i in result:
        #     z = i.replace(' ', '').split(',')
        #     for j in z:
        #         if j not in lst_unique_station:
        #             lst_unique_station.append(j)
        province = []
        city = []
        adname = []
        lng = []
        lat = []
        for s in lst_unique_station:
            url = 'https://restapi.amap.com/v3/place/text?'
            param = {
                'keywords': s+'站',
                'types': 150200,
                'extensions': 'all',
                'output': 'json',
                'key': '',
                'offset': 25
            }
            # print(requests.get(url,param).url)
            cities_len = len(requests.get(url, param).json()['suggestion']['cities'])
            if cities_len == 0:
                r = requests.get(url, param).json()['pois']
                for i in range(len(r)):
                    if r[i]['name'] == s + '站':
                        # print(s)
                        province.append(r[i]['pname'])
                        city.append(r[i]['cityname'])
                        adname.append(r[i]['adname'])
                        lng.append(r[i]['location'].split(',')[0])
                        lat.append(r[i]['location'].split(',')[1])
                        break
                    # if i == len(r)-1:
                    #     if r[i]['name'] != s + '站':
                    #         province.append('')
                    #         city.append('')
                    #         adname.append('')
                    #         lng.append('')
                    #         lat.append('')
                    #         # print(s)
            else:
                for i in range(cities_len):
                    station_city = requests.get(url, param).json()['suggestion']['cities'][i]['name']
                    param1 = param.copy()
                    param1['city'] = station_city
                    r = requests.get(requests.get(url, param1).json())
                    if r[i]['name'] == s + '站':
                        # print(s)
                        province.append(r[i]['pname'])
                        city.append(r[i]['cityname'])
                        adname.append(r[i]['adname'])
                        lng.append(r[i]['location'].split(',')[0])
                        lat.append(r[i]['location'].split(',')[1])
                        break


        print(len(lst_unique_station),len(province),len(city),len(adname),len(lng),len(lat))
        df_provincecitylocation = pd.DataFrame({'name': lst_unique_station, 'province': province, 'city': city,'adname':adname, 'lng_gcj02': lng, 'lat_gcj02': lat})
        if self.checkBox_ctrip_provincecitylocation_wgs84.isChecked():
            lst_wgs84 = list(map(gcj02_to_wgs84,df_provincecitylocation['lng_gcj02'].apply(lambda x:float(x)),df_provincecitylocation['lat_gcj02'].apply(lambda x:float(x))))
            df_provincecitylocation_wgs84 = pd.DataFrame(lst_wgs84, columns=['lng_wgs84', 'lat_wgs84'])
            df_provincecitylocation = df_provincecitylocation.join(df_provincecitylocation_wgs84)
        if self.checkBox_ctrip_provincecitylocation_bd09.isChecked():
            lst_bd09 = list(map(gcj02_to_bd09,df_provincecitylocation['lng_gcj02'].apply(lambda x:float(x)),df_provincecitylocation['lat_gcj02'].apply(lambda x:float(x))))
            df_provincecitylocation_bd09 = pd.DataFrame(lst_bd09, columns=['lng_bd09', 'lat_bd09'])
            df_provincecitylocation = df_provincecitylocation.join(df_provincecitylocation_bd09)
        # 所有站点的合并表
        df_provincecitylocation_sum = df.merge(df_provincecitylocation,how='left',on='name')
        # if i == '':
        #     df_provincecitylocation_sum.to_excel(writer,sheet_name='涉及车站位置')
        # else:
        #     df_provincecitylocation_sum.to_excel(writer, sheet_name=i+'_涉及车站位置')
        return df_provincecitylocation_sum

    # 度中心性
    def degreecentrality(self,ddf,writer,i=None):
        # 连接到的节点数
        G = nx.from_pandas_edgelist(ddf, source='o', target='d', edge_attr='统计次数')
        degree_dict = nx.degree_centrality(G)
        df_degreecentrality = pd.DataFrame.from_dict(degree_dict, orient='index')
        df_degreecentrality = df_degreecentrality.sort_values(by=0, ascending=False)
        if i == None:
            df_degreecentrality.to_excel(writer,sheet_name='度中心性')
        else:
            df_degreecentrality.to_excel(writer, sheet_name=i+'_度中心性')
    # 中介中心性
    def betweennesscentrality(self,ddf,writer,i=None):
        # 计算所有网络间节点的最短路，然后对每条边统计最短路经过的次数，并以每对节点间的最短路条数进行归一
        G = nx.from_pandas_edgelist(ddf, source='o', target='d', edge_attr='统计次数')
        betweenness_dict = nx.betweenness_centrality(G)
        df_betweennesscentrality = pd.DataFrame.from_dict(betweenness_dict, orient='index')
        df_betweennesscentrality = df_betweennesscentrality.sort_values(by=0, ascending=False)
        if i == None:
            df_betweennesscentrality.to_excel(writer,sheet_name='中介中心性')
        else:
            df_betweennesscentrality.to_excel(writer, sheet_name=i+'中介中心性')
    # 接近中心性
    def closenesscentrality(self,ddf,writer,i=None):
        # 所有可达节点的平均最短路径距离的倒数
        G = nx.from_pandas_edgelist(ddf, source='o', target='d', edge_attr='统计次数')
        closeness_dict = nx.closeness_centrality(G)
        df_closenesscentrality = pd.DataFrame.from_dict(closeness_dict, orient='index')
        df_closenesscentrality = df_closenesscentrality.sort_values(by=0, ascending=False)
        if i == None:
            df_closenesscentrality.to_excel(writer,sheet_name='接近中心性')
        else:
            df_closenesscentrality.to_excel(writer,sheet_name=i+'接近中心性')

    # target为起终点的线路
    def targetcity_odlines(self,i,df_target,writer_target):
        '''
        :param i: 目标城市名
        :param df_target: 包含目标城市的dataframe
        :param writer_target:需要写入的excel文件名称
        :return:
        '''
        df_target_o = df_target[[ i == x.split(',')[0] for x in df_target['od']]]
        df_target_o.to_excel(writer_target,sheet_name=i+'站为起点城市线路')
        df_target_d = df_target[[ i == x.split(',')[1] for x in df_target['od']]]
        df_target_d.to_excel(writer_target,sheet_name=i+'站为终点城市线路')

    # target_直接联系城市统计
    def targetcity_directconnectstatistics(self,i,result,writer_target):
        lst = []
        for j in result:
            if i in j:
                if j.index(i) == 0:
                    lst.append([j[0],j[1]])
                elif j.index(i) == len(j)-1:
                    lst.append([j[-2],j[-1]])
                else:
                    lst.append([j[j.index(i)-1],j[j.index(i)]])
                    lst.append([j[j.index(i)],j[j.index(i)+1]])
            else:
                pass
        df = pd.Series(lst).value_counts()
        ddf = pd.DataFrame()
        ddf['o']  = [i[0] for i in df.index.tolist()]
        ddf['d']  = [i[1] for i in df.index.tolist()]
        ddf['统计次数']  = df.values
        ddf.to_excel(writer_target,sheet_name=i+'站直接联系车站及统计次数（分方向）')
        return ddf

    '''
    target 几小时覆盖 
    待更新:区分G D 普铁
    '''
    def targetcity_ischrones(self,name,result,jinzhantime,fachetime,timezone,writer_target):
        '''
        :param name:  天门南
        :param result:  [['宜昌东', '荆州', '潜江', '天门南', '汉川', '汉口', '武汉', '咸宁北', '赤壁北', '岳阳东', '汨罗东', '长沙南', '衡山西', '郴州西', '韶关', '广州南', '虎门', '深圳北']]
        :param jinzhantime:[['----', '08:10', '08:37', '08:59', '09:16', '09:44', '10:14', '10:46', '11:05', '11:28', '11:53', '12:14', '12:48', '13:31', '14:09', '15:08', '15:33', '15:57']]
        :param fachetime:[['07:35', '08:12', '08:39', '09:01', '09:18', '09:51', '10:22', '10:51', '11:07', '11:33', '11:55', '12:19', '12:50', '13:38', '14:11', '15:16', '15:39', '15:57']]
        :param timezone:等时圈范围
        :return: xlsx sheet
        '''
        # 根据提供的等时圈分区时间，判断到达各站索引区间
        def compare(s):
            '''
            :param s: 'time'  1200
            :param z: [1800.0, 3600.0, 5400.0, 7200.0]
            :return: z.index
            '''
            # 把输入的等时圈范围str变list
            timez = timezone.split(',')
            def htosec(x):
                # 输入为h或者mins结尾
                if x[-1] == 'h':
                    return float(x[:-1]) * 60 * 60
                elif x[-4:] == 'mins':
                    return float(x[:-4]) * 60
                # else:
                #     return QMessageBox.warning(self,'Error','输入错误')

            # 把h/mins换算成seconds
            compare_list = list(map(htosec, timez))
            if len(compare_list) != 1:
                len_compare_list = len(compare_list)  # 4
                # 返回到达车站所需时间在list里面的index
                i = 0
                while i < len_compare_list:
                    if s < compare_list[i]:
                        return i
                    else:
                        i += 1
                return i
            else:
                return int(s // compare_list[0])


        deltaa = []
        # 字典 key:车站 values:最快到达时间(s)
        dic = {}
        for s in range(len(result)):
            deltatime = []
            if name in result[s]:
                ind = result[s].index(name)
                if ind == 0:
                    deltatime.append(0)
                    for i in range(1, len(result[s])):
                        timedelta = (datetime.datetime.strptime(jinzhantime[s][i], '%H:%M') - (
                            datetime.datetime.strptime(fachetime[s][0], '%H:%M'))).seconds
                        if result[s][i] not in dic.keys():
                            dic[result[s][i]] = timedelta
                        else:
                            if dic[result[s][i]] > timedelta:
                                dic[result[s][i]] = timedelta

                elif ind == len(result[s]) - 1:
                    for i in range(len(result[s])):
                        if i == 0:
                            pass
                        else:
                            timedelta = (datetime.datetime.strptime(fachetime[s][-1], '%H:%M') - datetime.datetime.strptime(
                                jinzhantime[s][i], '%H:%M')).seconds
                            if result[s][i] not in dic.keys():
                                dic[result[s][i]] = timedelta
                            else:
                                if dic[result[s][i]] > timedelta:
                                    dic[result[s][i]] = timedelta
                else:
                    for i in range(len(result[s])):
                        if i < ind:
                            timedelta = (datetime.datetime.strptime(jinzhantime[s][ind],
                                                                    '%H:%M') - datetime.datetime.strptime(fachetime[s][i],
                                                                                                          '%H:%M')).seconds
                        elif i > ind:
                            timedelta = (datetime.datetime.strptime(jinzhantime[s][i], '%H:%M') - datetime.datetime.strptime(fachetime[s][ind], '%H:%M')).seconds
                        else:
                            pass
                        if result[s][i] not in dic.keys():
                            dic[result[s][i]] = timedelta
                        else:
                            if dic[result[s][i]] > timedelta:
                                dic[result[s][i]] = timedelta
                deltaa.append(deltatime)
            else:
                pass
        dic1 = pd.DataFrame(list(dic.items()), columns=['name', 'time']).sort_values(by='time', ascending=True)


        dic1['compare'] = dic1['time'].map(compare)
        dic1.to_excel(writer_target,sheet_name = name+'到周围城市的时间和时圈索引')

    # def city_distance(self,,writer_target):



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ctripPageWindow()
    mainWindow.show()
    sys.exit(app.exec_())