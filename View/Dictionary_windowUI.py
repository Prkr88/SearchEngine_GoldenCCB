# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dictionary_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dictionaty_window(object):
    def setupUi(self, dictionaty_window):
        dictionaty_window.setObjectName("dictionaty_window")
        dictionaty_window.resize(1107, 932)
        dictionaty_window.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1105, 930))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.dictionary_terms = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.dictionary_terms.setObjectName("dictionary_terms")
        self.verticalLayout.addWidget(self.dictionary_terms)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        dictionaty_window.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(dictionaty_window)
        QtCore.QMetaObject.connectSlotsByName(dictionaty_window)

    def retranslateUi(self, dictionaty_window):
        _translate = QtCore.QCoreApplication.translate
        dictionaty_window.setWindowTitle(_translate("dictionaty_window", "Current Dictionary"))
        self.dictionary_terms.setHtml(_translate("dictionaty_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.1pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">what what</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">what what </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">what what</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     dictionaty_window = QtWidgets.QScrollArea()
#     ui = Ui_dictionaty_window()
#     ui.setupUi(dictionaty_window)
#     dictionaty_window.show()
#     sys.exit(app.exec_())

