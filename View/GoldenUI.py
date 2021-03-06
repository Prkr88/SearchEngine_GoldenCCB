from PyQt5 import QtGui, QtWidgets, uic, QtCore
from Model.ReadFile import ReadFile
from View.Dictionary_windowUI import Ui_dictionaty_window
from View.FeaturesUI import Ui_Features
from Controller.Controller import Controller
import time
import pickle
import json
import datetime
import gc
import os
import gensim


class Gu(QtWidgets.QMainWindow):
    def __init__(self, path):
        super(Gu, self).__init__()
        icon = QtGui.QIcon()
        uic.loadUi(path, self)
        self.vocabulary = {}
        self.controller = None
        self.vocabulary_display_mode = None
        self.city_limit_list = None
        self.queries_file_path = ""
        self.results = ""
        self.docs_data = {}
        self.semantic_model = None


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
        # self.lineEdit_data_path.setText("C:/Users/Prkr_Xps/Documents/InformationSystems/Year_C/SearchEngine/corpus")
        # self.lineEdit_posting_dest_path.setText("C:/Users/Prkr_Xps/Documents/InformationSystems/Year_C/SearchEngine")
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
        # if self.controller is None:
        #     hash_path = 'C:/Users/edoli/Desktop/SE_PA/Engine_Data/Vocabulary/Vocabulary.pkl'
        #     with open(hash_path, 'rb') as input_object:
        #         vocabulary = pickle.load(input_object)
        #     self.controller = Controller(vocabulary)
        # else:
        #     vocabulary = self.controller.vocabulary
        query = ''
        if self.serach_query_lineEdit.text() != '':
            query = self.serach_query_lineEdit.text()
        mode_semantic = self.stemmer_checkBox_2.isChecked()
        self.controller.search(self.controller.vocabulary, self.semantic_model, query, self.city_limit_list, mode_semantic)
        #self.controller.search(self.controller.vocabulary, self.semantic_model, query, self.city_limit_list , mode_semantic)
        self.results_screen()

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
        docs_entities = {}
        s = QtWidgets.QListWidgetItem()
        selected = self.listWidget_results.selectedItems()
        item = selected[0]
        doc_id = item.text()
        if 'Query_ID:' not in doc_id:
            self.label_DocNUm_entities.setVisible(True)
            self.listWidget_entities.setVisible(True)
            entities = self.controller.hash_docs_data[doc_id][3]
            entities_list = []
            for entity in entities:
                to_add = (entity[0] + ' , rank: ' + str(entity[1]) , '')
                entities_list.append(to_add)
            self.feed_listWidget(entities_list,self.listWidget_entities,0)
            self.label_DocNUm_entities.setText("Entities for Doc:  " + doc_id)
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setWindowTitle("Bad Choice")
            msgBox.setText("Are you trying to crash the program?  Please choose valid doc")
            msgBox.exec()

    # Save Results to file
    def save_results_to_file(self):
        self.controller.searcher.save_final_results()
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle("Results saved!")
        msgBox.setText("Results saved to ../Engine_data/Results.")
        msgBox.exec()

    # @Save_screen load Queries from file
    def load_Query_file(self):
        print('load queries')
        path = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if path != '':
            self.controller.queries_file_path = path
            self.query_loaded_lbl.setVisible(True)
            self.serach_query_lineEdit.setDisabled(True)

    # @Save_screen set city limit
    def limit_by_city(self):
        print('limit_results')
        self.listWidget_cities.setVisible(True)
        self.submit_limit_btn.setVisible(True)
        self.controller.set_cities_list_limit()
        limit_list = self.controller.city_list_to_limit
        self.feed_listWidget(limit_list,self.listWidget_cities,0)

    # @Save_screen save limit
    def submit_city_limit(self):
        print('save limit')
        selected = self.listWidget_cities.selectedItems()
        for item in selected:
            self.city_limit_list.append(item.text())
        self.city_limited_lbl.setVisible(True)

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

    # if os.path.exists('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\Engine_Data'):
    #     engine_data_path = 'C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\Engine_Data'
    # if os.path.exists('C:\\Users\\edoli\\Desktop\\SE_PA\\Engine_Data'):
    #     engine_data_path = 'C:\\Users\\edoli\\Desktop\\SE_PA\\Engine_Data'

    def search_screen(self):
        self.query_loaded_lbl.setVisible(False)
        self.city_limited_lbl.setVisible(False)
        self.city_limited_lbl.setVisible(False)
        self.listWidget_cities.setVisible(False)
        self.submit_limit_btn.setVisible(False)
        if self.controller == None:
            if os.path.exists('C:\\Users\\edoli\\Desktop\\SE_PA\\Engine_Data'):
                engine_data_path = 'C:\\Users\\edoli\\Desktop\\SE_PA\\Engine_Data'
            else:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setWindowTitle("User input needed")
                msgBox.setText("Please provide Engine_Data folder location.")
                msgBox.exec()
                engine_data_path = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
            self.load_files(engine_data_path)
        else:
            if self.controller.searcher != None:
                self.controller.searcher.all_tuple_results = []
                self.controller.searcher.all_hash_results = []
                self.controller.searcher.tuple_results = []
                self.controller.searcher.hash_docs = {}
        self.stackedWidget.setCurrentIndex(2)

    def results_screen(self):
        self.controller.searcher.write_to_trec_eval()
        self.label_DocNUm_entities.setVisible(False)
        self.listWidget_entities.setVisible(False)
        #result_list = Bring me the Fucking List!
        listW = QtWidgets.QListWidget()
       # item = listW.selectedItems()
        #result_list = [('FBIS4-9640',156.1),('FBI2',16.1),('FBI3',156.1)]
        result_list = self.controller.searcher.all_tuple_results
        self.feed_listWidget(result_list,self.listWidget_results,0)
        self.stackedWidget.setCurrentIndex(3)
        # Add Docs to ListWidget
        ''''''

    def feed_listWidget(self,result_list,list_widget,type):
        _translate = QtCore.QCoreApplication.translate
        list_widget.clear()
        for idx, doc in enumerate(result_list):
            item = QtWidgets.QListWidgetItem()
            list_widget.addItem(item)
            # item = self.listWidget_results.item(idx)
            to_add = doc[type]
            if to_add == 'Query_ID:':
                to_add = to_add + ' ' + str(doc[1])
                item.setBackground(QtGui.QColor("black"))
            item.setText(_translate("GoldenMainWindow", to_add))

    def back_to_menu(self):
        self.stackedWidget.setCurrentIndex(0)
        if self.controller is not None:
            if self.controller.searcher is not None:
                btn = QtWidgets.QPushButton()
                self.jump_to_rst_btn.setVisible(True)
        else:
            self.jump_to_rst_btn.setVisible(False)

    # Setup GUI
    def setup_ui(self):
        # set Background
        self.setStyleSheet("background-image: url(resources//intro-bg.jpg);")

        # Set Main window
        #self.stackedWidget.setCurrentIndex(0)
        self.back_to_menu()
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
        self.limit_by_city_btn.clicked.connect(self.limit_by_city)
        self.browse_Query_btn.clicked.connect(self.load_Query_file)
        self.submit_limit_btn.clicked.connect(self.submit_city_limit)

        # setUp Results screen
        self.label_DocNUm_entities.setVisible(False)
        self.listWidget_entities.setVisible(False)
        self.show_entities_btn.clicked.connect(self.show_doc_entities)
        self.save_results_btn.clicked.connect(self.save_results_to_file)

    def load_files(self,path):
        if path!='':
            with open(path +'/Vocabulary/hash_docs_data.pkl', 'rb') as file:
                docs_data = pickle.load(file)
            with open(path +'/Vocabulary/Vocabulary.pkl', 'rb') as file:
                vocabulary = pickle.load(file)
            with open(path + '/Vocabulary/docs_cos_data.pkl', 'rb') as file:
                cos_data = pickle.load(file)
            self.semantic_model = gensim.models.Word2Vec.load(path + '/Semantics/word2vec.model')
            self.controller = Controller(vocabulary)
            self.controller.post_path = path
            self.controller.hash_docs_data = docs_data
            self.controller.hash_cos_data = cos_data
        else:
            self.search_screen()

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
