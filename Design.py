"""
    Battery_Management_App  Copyright (C) 2023 Krishna Reddy
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
"""


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BatteryManager(object):
    def setupUi(self, BatteryManager):
        BatteryManager.setObjectName("Battery Manager")
        BatteryManager.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(BatteryManager)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(110, 70, 71, 20))
        self.horizontalSlider.setMaximum(50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(180, 70, 71, 20))
        self.horizontalSlider_2.setMinimum(50)
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.lbl_main = QtWidgets.QLabel(self.centralwidget)
        self.lbl_main.setGeometry(QtCore.QRect(20, 10, 400, 20))
        self.lbl_main.setObjectName("lbl_main")
        self.lbl_L = QtWidgets.QLabel(self.centralwidget)
        self.lbl_L.setGeometry(QtCore.QRect(60, 110, 150, 20))
        self.lbl_L.setObjectName("lbl_L")
        self.lbl_U = QtWidgets.QLabel(self.centralwidget)
        self.lbl_U.setGeometry(QtCore.QRect(190, 110, 150, 20))
        self.lbl_U.setObjectName("lbl_U")
        
        self.lbl_Bs = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Bs.setGeometry(QtCore.QRect(40, 200, 200, 20))
        self.lbl_Bs.setObjectName("lbl_Bs")
        self.lbl_Bp = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Bp.setGeometry(QtCore.QRect(40, 250, 200, 20))
        self.lbl_Bp.setObjectName("lbl_Bp")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 310, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 310, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(260, 310, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(44, 350, 350, 31))
        self.label.setObjectName("label")
        BatteryManager.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(BatteryManager)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 639, 26))
        self.menubar.setObjectName("menubar")
        BatteryManager.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(BatteryManager)
        self.statusbar.setObjectName("statusbar")
        BatteryManager.setStatusBar(self.statusbar)

        self.retranslateUi(BatteryManager)
        QtCore.QMetaObject.connectSlotsByName(BatteryManager)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_main.setText(_translate("MainWindow", "Adjust your AC on/off Limit  to Manage your Battterylife"))
        self.lbl_L.setText(_translate("MainWindow", "LowerLimit:"))
        self.lbl_U.setText(_translate("MainWindow", "UpperLimit:"))
        
        self.lbl_Bs.setText(_translate("MainWindow", "Battery Status :"))
        self.lbl_Bp.setText(_translate("MainWindow", "Battery Percentage :"))
        self.pushButton.setText(_translate("MainWindow", "Trigger"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))
        self.pushButton_3.setText(_translate("MainWindow", "Connect"))
        self.label.setText(_translate("MainWindow", "\"Message Conncted to Bluetooth or not\""))
