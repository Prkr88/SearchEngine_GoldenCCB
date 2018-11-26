# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Golden_First_UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from Model.ReadFile import ReadFile
from PyQt5 import QtCore, QtGui, QtWidgets  # noinspection PyUnresolvedReferences

class Ui_MainWindow(object):

    lineEdit_counter = 0
    lineEdit_2_counter = 0
    def browse_one(self):
        self.lineEdit.clear()
        self.lineEdit.setText(QtWidgets.QFileDialog.getExistingDirectory(None ,"Select Directory"))

    def browse_two(self):
        self.lineEdit_2.clear()
        self.lineEdit_2.setText(QtWidgets.QFileDialog.getExistingDirectory(None ,"Select Directory"))

    def start_program(self):
        if '\\' in self.lineEdit.text() and '\\' in self.lineEdit_2.text():
            read_file = ReadFile(self.lineEdit.text(),self.lineEdit_2.text())
        else:
            error_one = ""
            error_two = ""
            if '\\' not in self.lineEdit.text():
                error_one = "*** Data Path is empty or invalid.\n"
            if '\\' not in self.lineEdit_2.text():
                error_two = "*** Posting destination is empty or invalid."
            error_message = "Error:\n" + error_one + error_two
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setWindowTitle("Input Error")
            msgBox.setText(error_message)
            msgBox.exec()
    def clear_text_field_one(self):
        if self.lineEdit_counter == 0:
            self.lineEdit_counter = 1
            self.lineEdit.clear()

    def clear_text_field_two(self):
        if self.lineEdit_counter == 0:
            self.lineEdit_2_counter = 1
            self.lineEdit.clear()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1418, 1087)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("..//resources/goldenccb_icon_E7q_icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-image: url(..//resources//intro-bg.jpg);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(1000, 490, 151, 57))
        ######################## Bottun Event ##############################
        self.pushButton1.clicked.connect(self.browse_one)
        ######################## Bottun Event ##############################
        self.pushButton1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton1.setStyleSheet("QPushButton {\n"
"    color: #BEBEBE;\n"
"    border: 2px solid #555;\n"
"    border-radius: 20px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #F5F5F5, stop: 1 #F5F5F5\n"
"        );\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    color: #404040;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #F5F5F5, stop: 1 #F5F5F5\n"
"        );\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
"        );\n"
"    }")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("..//resources/iconfinder_icon-101-folder-search_314678.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton1.setIcon(icon1)
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1000, 580, 151, 57))
        ######################## Bottun Event ##############################
        self.pushButton_2.clicked.connect(self.start_program)
        ######################## Bottun Event ##############################
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("QPushButton {\n"
"    color: #BEBEBE;\n"
"    border: 2px solid #555;\n"
"    border-radius: 20px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #F5F5F5, stop: 1 #F5F5F5\n"
"        );\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    color: #404040;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #F5F5F5, stop: 1 #F5F5F5\n"
"        );\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
"        );\n"
"    }")
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(270, 590, 711, 39))
        ######################## Text Field Event ##############################
        self.lineEdit_2.keyPressEvent(self.clear_text_field_one())
        ######################## Text Field Event ##############################
        self.lineEdit_2.setStyleSheet("QLineEdit {\n"
" color: #BEBEBE; \n"
"border: 2px solid #cccccc;\n"
"border-radius: 10px;\n"
" }")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(270, 500, 711, 39))
        ######################## Text Field Event ##############################
        self.lineEdit.clicked.connect(self.clear_text_field_one)
        ######################## Text Field Event ##############################
        self.lineEdit.setStyleSheet("QLineEdit {\n"
" color: #BEBEBE; \n"
"border: 2px solid #cccccc;\n"
"border-radius: 10px;\n"
" }")
        self.lineEdit.setInputMask("")
        self.lineEdit.setObjectName("lineEdit")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(270, 450, 181, 37))
        self.checkBox.setStyleSheet("background-image: url(..//resources//transparent.png);\n"
"font: 81 8pt \"Raleway ExtraBold\";")
        self.checkBox.setObjectName("checkBox")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(570, 690, 191, 81))
        ######################## Bottun Event ##############################
        self.pushButton_3.clicked.connect(self.start_program)
        ######################## Bottun Event ##############################
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("QPushButton {\n"
"    color: #F5F5F5;\n"
"    border: 2px solid #555;\n"
"    border-radius: 20px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0     #68abfd, stop: 1 #157efb\n"
"        );\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #cde3fe, stop: 1 #68abfd\n"
"        );\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
"        );\n"
"    }")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 20, 1001, 411))
        self.label.setStyleSheet("background-image: url(..//resources//white_goldenCCB_logo.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1418, 47))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        #self.pushButton1.pressed.connect(self.lineEdit.paste)
        #self.pushButton_2.pressed.connect(self.lineEdit_2.paste)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton1.setText(_translate("MainWindow", "browse"))
        self.pushButton_2.setText(_translate("MainWindow", "browse"))
        self.lineEdit_2.setText(_translate("MainWindow", "Enter Posting Destination Path"))
        self.lineEdit.setText(_translate("MainWindow", "Enter Corpus and StopWords Path"))
        self.checkBox.setText(_translate("MainWindow", "Stemmer"))
        self.pushButton_3.setText(_translate("MainWindow", "Start"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

