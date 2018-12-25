from PyQt5 import QtGui, QtWidgets, uic, QtCore
from Model.ReadFile import ReadFile
from View.Dictionary_windowUI import Ui_dictionaty_window
from View.FeaturesUI import Ui_Features
from Controller.Controller import Controller
import time
import pickle
import json
import gc


class Gu(QtWidgets.QMainWindow):
    def __init__(self, path):
        super(Gu, self).__init__()
        icon = QtGui.QIcon()
        uic.loadUi(path, self)
        self.vocabulary = {}
        self.controller = None
        self.vocabulary_display_mode = None

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
        self.lineEdit_data_path.setText("C:/Users/Prkr_Xps/Documents/InformationSystems/Year_C/SearchEngine/corpus")
        self.lineEdit_posting_dest_path.setText("C:/Users/Prkr_Xps/Documents/InformationSystems/Year_C/SearchEngine")
        if any(c in self.lineEdit_data_path.text() for c in ('\\', '/')) and \
                any(c in self.lineEdit_posting_dest_path.text() for c in ('\\', '/')):
            stemmer = self.stemmer_checkBox.isChecked()
            self.controller = Controller(self.vocabulary)
            self.controller.start(self.lineEdit_data_path.text(), self.lineEdit_posting_dest_path.text(), stemmer)
            summary_message = '#Num of Docs Indexed: ' + '\n\t' + str(self.controller.doc_counter) + \
                              '\n#Num of Unique Terms: ' + '\n\t' + str(self.controller.unique_terms) + \
                              '\nTotal Time: ' + '\n\t' + str(int(self.controller.total_time)) + ' seconds'
            self.vocabulary_display_mode = self.controller.vocabulary_display_mode
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setWindowTitle("Summary")
            msgBox.setText(summary_message)
            msgBox.exec()
            self.results_screen()
        else:
            error_one = ""
            error_two = ""
            if not any(c in self.lineEdit_data_path.text() for c in ('\\', '/')):
                error_one = "*** Data Path is empty or invalid.                    \n"
            if not any(c in self.lineEdit_posting_dest_path.text() for c in ('\\', '/')):
                error_two = "*** Posting destination is empty or invalid.               "
            error_message = "Error:                     \n" + error_one + error_two
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setWindowTitle("Input Error")
            msgBox.setText(error_message)
            msgBox.exec()

    def search_query(self):
        if self.controller is None:

            path_voc = 'C:/Users/edoli/Desktop/SE_PA/Engine_Data/Vocabulary/Vocabulary.pkl'
            with open(path_voc, 'rb') as input:
                vocabulary = pickle.load(input)
        else:
            vocabulary = self.controller.vocabulary
        self.controller = Controller(vocabulary)
        self.controller.search(vocabulary)

    def show_dictionary(self):
        self.window = QtWidgets.QScrollArea()
        self.uiD = Ui_dictionaty_window()
        self.uiD.setupUi(self.window)
        vocab = self.vocabulary_display_mode
        if len(vocab) > 0:
            self.uiD.dictionary_terms.setText(vocab)
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
        with open(path, 'r', encoding='utf-8') as vocab:
            vocabulary_to_load = vocab.read()
        self.vocabulary_display_mode = vocabulary_to_load
        print("Dictionary loaded")

    def reset_system(self):
        quit_msg = "Are you sure you want to Reset the System?"
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            if self.controller != None:
                op = self.controller.reset_system()
                self.controller = None
                gc.collect()
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

    # Show entities

    def show_doc_entities(self):
        print('show entities')
        '''show Doc ID label'''
    # Save Results to file

    def save_results_to_file(self):
        print('save results')

    # @Save_screen load Queries from file
    def load_Query_file(self):
        print('load queries')
        '''show indication'''

    # @Save_screen set city limit
    def limit_by_city(self):
        print('limit_results')

    # @Save_screen save limit
    def submit_city_limit(self):
        print('save limit')
        '''show indication'''

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

    def create_index_screen(self):
        self.stackedWidget.setCurrentIndex(1)

    def search_screen(self):
        self.stackedWidget.setCurrentIndex(2)

    def results_screen(self):
        self.stackedWidget.setCurrentIndex(3)
        # Add Docs to ListWidget
        ''''''


    def back_to_menu(self):
        self.stackedWidget.setCurrentIndex(0)

    # Setup GUI
    def setup_ui(self):
        # set Background
        self.setStyleSheet("background-image: url(resources//intro-bg.jpg);")

        # Set Main window
        self.stackedWidget.setCurrentIndex(0)
        # Set logos
        self.logo_label_2.setStyleSheet("image: url(resources//white_goldenCCB_logo.png);")
        self.logo_label_3.setStyleSheet("image: url(resources//white_goldenCCB_logo.png);")
        self.logo_label_4.setStyleSheet("image: url(resources//white_goldenCCB_logo.png);")

        # Set NavButtons

        self.jump_to_rst_btn.setStyleSheet("QPushButton {\n"
                                           "image: url(resources//nav_btn_A.png);\n"
                                           "    border: none;\n"
                                           "    background: none;\n"
                                           "    padding: 5px;\n"
                                           "    }\n"
                                           "\n"
                                           "QPushButton:hover {\n"
                                           "image: url(resources//nav_btn_B.png);\n"
                                           " border: none;\n"
                                           "    background: none;\n"
                                           "    padding: 5px;\n"
                                           "    }\n"
                                           "\n"
                                           "QPushButton:pressed {\n"
                                           "image: url(resources//nav_btn_C.png);\n"
                                           "   border: none;\n"
                                           "    background: none;\n"
                                           "    padding: 5px;\n"
                                           "    }")
        self.back_btn_create.setStyleSheet(self.get_back_btn_style())
        self.back_btn_search.setStyleSheet(self.get_back_btn_style())
        self.back_btn_results.setStyleSheet(self.get_back_btn_style())

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
        self.actionMeet_the_Tem.setIcon(team_icon)
        features_icon = QtGui.QIcon()
        features_icon.addPixmap(QtGui.QPixmap("resources/iconfinder_star_1054969.ico"), QtGui.QIcon.Normal,
                                QtGui.QIcon.Off)
        self.actionFeatures.setIcon(features_icon)
        Reset_icon = QtGui.QIcon()
        Reset_icon.addPixmap(QtGui.QPixmap("resources/iconfinder_close_1282956.ico"), QtGui.QIcon.Normal,
                             QtGui.QIcon.Off)
        self.actionReset_System_Data.setIcon(Reset_icon)
        load_icon = QtGui.QIcon()
        load_icon.addPixmap(QtGui.QPixmap("resources/iconfinder_9_330409.ico"), QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
        self.actionLoad_Dicationary_from_file.setIcon(load_icon)
        current_dic_icon = QtGui.QIcon()
        current_dic_icon.addPixmap(QtGui.QPixmap("resources/iconfinder_note_1296370.ico"), QtGui.QIcon.Normal,
                                   QtGui.QIcon.Off)
        self.actionShow_current_dictionary.setIcon(current_dic_icon)

        # Init ProgressBar
        # self.progressBar.setVisible(False)
        # self.time_label.setVisible(False)

        # Set Functionality
        self.browse_data_btn.clicked.connect(self.browse_one)
        self.browse_post_dest_btn.clicked.connect(self.browse_two)
        self.start_btn.clicked.connect(self.start_program)
        self.search_query_btn.clicked.connect(self.search_query)
        self.actionShow_current_dictionary.triggered.connect(self.show_dictionary)
        self.actionLoad_Dicationary_from_file.triggered.connect(self.load_dictionary)
        self.actionReset_System_Data.triggered.connect(self.reset_system)
        self.actionFeatures.triggered.connect(self.show_features)
        self.actionMeet_the_Tem.triggered.connect(self.show_team)

        # Connect Buttons Screen Navigation
        self.create_index_btn.clicked.connect(self.create_index_screen)
        self.search_btn.clicked.connect(self.search_screen)
        self.jump_to_rst_btn.clicked.connect(self.results_screen)
        self.back_btn_create.clicked.connect(self.back_to_menu)
        self.back_btn_search.clicked.connect(self.back_to_menu)
        self.back_btn_results.clicked.connect(self.back_to_menu)

        # setUp search screen
        self.browse_Query_btn.setIcon(folder_icon)
        self.query_loaded_lbl.setVisible(False)
        self.city_limited_lbl.setVisible(False)
        self.city_limited_lbl.setVisible(False)
        self.listWidget_cities.setVisible(False)
        self.submit_limit_btn.setVisible(False)

        # setUp Results screen
        self.label_DocNUm_entities.setVisible(False)
        self.listWidget_entities.setVisible(False)

    def get_back_btn_style(self):
        return ("QPushButton {\n"
                "image: url(resources//nav_back_btn_A.png);\n"
                "    border: none;\n"
                "    background: none;\n"
                "    padding: 5px;\n"
                "    }\n"
                "\n"
                "QPushButton:hover {\n"
                "image: url(resources//nav_back_btn_B.png);\n"
                " border: none;\n"
                "    background: none;\n"
                "    padding: 5px;\n"
                "    }\n"
                "\n"
                "QPushButton:pressed {\n"
                "image: url(resources//nav_back_btn_C.png);\n"
                "   border: none;\n"
                "    background: none;\n"
                "    padding: 5px;\n"
                "    }")
