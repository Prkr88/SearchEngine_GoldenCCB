from PyQt5 import QtGui, QtWidgets, uic, QtCore
from Model.ReadFile import ReadFile
from View.Dictionary_windowUI import Ui_dictionaty_window
from View.FeaturesUI import Ui_Features
from Controller.Controller import Controller
import time


class Gu(QtWidgets.QMainWindow):
    def __init__(self, path):
        super(Gu, self).__init__()
        icon = QtGui.QIcon()
        uic.loadUi(path, self)


    # Methods
    def browse_one(self):
        self.lineEdit_data_path.clear()
        self.lineEdit_data_path.setText(QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory"))

    def browse_two(self):
        self.lineEdit_posting_dest_path.clear()
        self.lineEdit_posting_dest_path.setText(QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory"))

    def start_program(self):
        if '\\' or '/' in self.lineEdit_posting_dest_path.text() and '\\' or '/' in self.lineEdit_posting_dest_path.text():
            stemmer = self.stemmer_checkBox.isChecked()
            controller = Controller(self)
            controller.start(self.lineEdit_data_path.text(), self.lineEdit_posting_dest_path.text(), stemmer)

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

    def update_time_progress(self,prog,time):
        time_text = 'ETA: '
        prog = QtWidgets.QLabel
        if self.progressBar.isVisible() == False or self.time_label.isVisible() == False:
            self.progressBar.setVisible(True)
            self.time_label.setVisible(True)
        self.progressBar.setValue(prog)
        self.time_label.setText(time)


    def show_dictionary(self):
        self.window = QtWidgets.QScrollArea()
        self.ui = Ui_dictionaty_window()
        self.ui.setupUi(self.window)
        self.window.show()

    def load_dictionary(self):
        print("Dictionary loaded")
        self.window = QtWidgets.QScrollArea()
        self.ui = Ui_dictionaty_window()
        self.ui.setupUi(self.window)
        self.window.show()

    def reset_system(self):
        print("Holy shit System has been reset!")

    def show_features(self):
        print("Crazy Features")
        self.window = QtWidgets.QScrollArea()
        self.ui = Ui_Features()
        self.ui.setupUi(self.window)
        self.window.show()

    def show_team(self):
        print("Amazing Team")
        self.window = QtWidgets.QScrollArea()
        self.ui = Ui_dictionaty_window()
        self.ui.setupUi(self.window)
        self.window.show()


    # Setup GUI
    def setup_ui(self):
        # set Background
        self.setStyleSheet("background-image: url(resources//intro-bg.jpg);")

        # Set Program Icons
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/goldenccb_icon_E7q_icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        folder_icon = QtGui.QIcon()
        folder_icon.addPixmap(QtGui.QPixmap("resources/iconfinder_icon-101-folder-search_314678.ico"),
                              QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.browse_data_btn.setIcon(folder_icon)
        self.browse_post_dest_btn.setIcon(folder_icon)
        self.logo_label.setStyleSheet("background-image: url(resources//white_goldenCCB_logo.png);")
        team_icon = QtGui.QIcon()
        team_icon.addPixmap(QtGui.QPixmap("resources/iconfinder_ramen_3377055.ico"), QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
        self.actionThe_Team.setIcon(team_icon)
        features_icon = QtGui.QIcon()
        features_icon.addPixmap(QtGui.QPixmap("resources/iconfinder_star_1054969.ico"), QtGui.QIcon.Normal,
                                QtGui.QIcon.Off)
        self.actionFeatures.setIcon(features_icon)
        Reset_icon = QtGui.QIcon()
        Reset_icon.addPixmap(QtGui.QPixmap("resources/iconfinder_close_1282956.ico"), QtGui.QIcon.Normal,
                             QtGui.QIcon.Off)
        self.actionReset_System.setIcon(Reset_icon)
        load_icon = QtGui.QIcon()
        load_icon.addPixmap(QtGui.QPixmap("resources/iconfinder_9_330409.ico"), QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
        self.actionLoad_dicationary_from_file.setIcon(load_icon)
        current_dic_icon = QtGui.QIcon()
        current_dic_icon.addPixmap(QtGui.QPixmap("resources/iconfinder_note_1296370.ico"), QtGui.QIcon.Normal,
                                   QtGui.QIcon.Off)
        self.actionShow_current_dictionary.setIcon(current_dic_icon)

        # Init ProgressBar
        self.progressBar.setVisible(False)
        self.time_label.setVisible(False)

        # Set Functionality
        self.browse_data_btn.clicked.connect(self.browse_one)
        self.browse_post_dest_btn.clicked.connect(self.browse_two)
        self.start_btn.clicked.connect(self.start_program)
        self.actionShow_current_dictionary.triggered.connect(self.show_dictionary)
        self.actionLoad_dicationary_from_file.triggered.connect(self.load_dictionary)
        self.actionReset_System.triggered.connect(self.reset_system)
        self.actionFeatures.triggered.connect(self.show_features)
        self.actionThe_Team.triggered.connect(self.show_team)


