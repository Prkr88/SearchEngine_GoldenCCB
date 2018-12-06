from PyQt5 import QtGui, QtWidgets, uic, QtCore
from Model.ReadFile import ReadFile
from View.Dictionary_windowUI import Ui_dictionaty_window
from View.FeaturesUI import Ui_Features
from Controller.Controller import Controller
import time
import pickle
import json


class Gu(QtWidgets.QMainWindow):
    def __init__(self, path):
        super(Gu, self).__init__()
        icon = QtGui.QIcon()
        uic.loadUi(path, self)
        self.vocabulary = {}
        self.vocabulary_display_mode = None
        self.controller = None

    # Methods
    def browse_one(self):
        self.lineEdit_data_path.clear()
        self.lineEdit_data_path.setText(QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory"))

    def browse_two(self):
        self.lineEdit_posting_dest_path.clear()
        self.lineEdit_posting_dest_path.setText(QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory"))

    # self.lineEdit_data_path.setText("C:/Users/Prkr_Xps/Documents/InformationSystems/Year_C/SearchEngine/corpus")
    # self.lineEdit_posting_dest_path.setText("C:/Users/Prkr_Xps/Documents/InformationSystems/Year_C/SearchEngine")
    # self.lineEdit_data_path.setText("C:/Users/edoli/Desktop/SE_PA/corpus")
    # self.lineEdit_posting_dest_path.setText("C:/Users/edoli/Desktop/SE_PA/")

    def start_program(self):
        # if any(c in self.lineEdit_data_path.text() for c in('\\' , '/')) and \
        # any(c in self.lineEdit_posting_dest_path.text() for c in('\\' , '/')):
        stemmer = self.stemmer_checkBox.isChecked()
        self.controller = Controller(self.vocabulary)
        self.lineEdit_data_path.setText("C:/Users/edoli/Desktop/SE_PA/corpus")
        self.lineEdit_posting_dest_path.setText("C:/Users/edoli/Desktop/SE_PA/")
        self.controller.start(self.lineEdit_data_path.text(), self.lineEdit_posting_dest_path.text(), stemmer)
        summary_message = '#Num of Docs Indexed: ' + '\n\t' + str(
            self.controller.doc_counter) + '\n#Num of Unique Terms: ' + \
                          '\n\t' + str(self.controller.unique_terms) + '\nTotal Time: ' + '\n\t' + str(
            int(self.controller.total_time) +' seconds')
        self.vocabulary_display_mode = self.controller.vocabulary_display_mode
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle("Summary")
        msgBox.setText(summary_message)
        msgBox.exec()
        # else:
        #     error_one = ""
        #     error_two = ""
        #     if not any(c in self.lineEdit_data_path.text() for c in ('\\', '/')):
        #         error_one = "*** Data Path is empty or invalid.                    \n"
        #     if not any(c in self.lineEdit_posting_dest_path.text() for c in('\\' , '/')):
        #         error_two = "*** Posting destination is empty or invalid.               "
        #     error_message = "Error:                     \n" + error_one + error_two
        #     msgBox = QtWidgets.QMessageBox()
        #     msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        #     msgBox.setWindowTitle("Input Error")
        #     msgBox.setText(error_message)
        #     msgBox.exec()

    def show_dictionary(self):
        self.window = QtWidgets.QScrollArea()
        self.uiD = Ui_dictionaty_window()
        self.uiD.setupUi(self.window)
        ans = ""
        vocab = self.vocabulary_display_mode
        if len(vocab) > 0:
            ans = ',\n'.join(str(item) for item in vocab)
            self.uiD.dictionary_terms.setText(ans)
            self.window.show()
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setWindowTitle("Error")
            msgBox.setText("No dictionary to show")
            msgBox.exec()

    def load_dictionary(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        print(path)
        with open(path, 'rb') as vocab:
            vocabulary_to_load = pickle.load(vocab)
        self.vocabulary_display_mode = vocabulary_to_load
        print("Dictionary loaded")

    def reset_system(self):
        op = self.controller.reset_system()
        if op != None:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setWindowTitle("Reset")
            msgBox.setText("System has been rested Successfuly.")
            msgBox.exec()
            print("Holy shit System has been reset!")
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setWindowTitle("Reset")
            msgBox.setText("Nothing to Delete.")
            msgBox.exec()

    def show_features(self):
        print("Crazy Features")
        self.window = QtWidgets.QScrollArea()
        self.uiF = Ui_Features()
        self.uiF.setupUi(self.window)
        self.uiF.label.setStyleSheet("image: url(..//resources//features.PNG);")
        self.window.show()

    def show_team(self):
        print("Amazing Team")
        self.window = QtWidgets.QScrollArea()
        self.uiT = Ui_dictionaty_window()
        self.uiT.setupUi(self.window)
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
