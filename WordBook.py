from PySide6.QtCore import (QCoreApplication, QFile, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QTimer, Slot, QModelIndex)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient, QStandardItem,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform, QStandardItem, QStandardItemModel, QDesktopServices)
from PySide6.QtWidgets import (QApplication, QMessageBox, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QListView, QListWidget, QListWidgetItem, QComboBox,
    QMainWindow, QMenu, QMenuBar, QProgressBar, QStyledItemDelegate,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar, QTreeWidget, QTreeWidgetItem, 
    QTabWidget, QTextEdit, QToolBox, QVBoxLayout, QSpinBox, QTimeEdit, QStyleFactory,
    QWidget, QFileDialog, QInputDialog, QDateTimeEdit, QDialog, QFontComboBox, QHeaderView)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimedia import QMediaFormat
from wordbookUI import Ui_MainWindow
from functools import partial
import sys
import os
import json
import re
import sqlite3
import random
import numpy as np
import pandas as pd
import time
from InternetState import Internet
from TimeState import Worker
from Completer import MyCompleter
import InternetSearch
import pyperclip
from picture import picture_ocr
import InternetTranslation
import subprocess
import MP3
from PySide6.QtUiTools import QUiLoader
from qt_material import apply_stylesheet
class WordBook(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(WordBook, self).__init__()
        self.setupUi(self)
        icon = QIcon("book.png")
        self.setWindowIcon(icon)
        self.label.setText("")
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.count_down)
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        num_path = d + "/resource/number.txt"
        countdown_path = d + "/resource/countdown.txt"
        paste_png = d + "/resource/Change.png"
        theme_path = d + "/resource/Theme.txt"
        icon = QIcon(paste_png)
        with open(theme_path,"r") as f:
            theme_ = f.read()
        self.pushButton_28.setIcon(icon)
        self.pushButton_29.setIcon(icon)
        self.pushButton_30.setIcon(icon)
        self.pushButton_31.setIcon(icon)
        with open(num_path,"r") as f:
            current_num = f.read()
        with open(countdown_path,"r") as f:
            countdown_num = f.read()
        countdown_num = int(countdown_num)
        self.progressBar.setMaximum(countdown_num)
        self.spinBox.setValue(countdown_num)
        if current_num != "0":
            current_num = "0"
        with open(num_path,"w") as f:
            f.write(current_num)
        self.pushButton_17.setEnabled(False)
        self.pushButton_21.setEnabled(False)
        self.pushButton_22.setEnabled(False)
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput() # 不能实例化为临时变量，否则被自动回收导致无法播放
        self.player.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(1)
        self.pushButton_12.setText("\n开始\n")
        completer = MyCompleter()
        completer.setWidget(self.lineEdit)
        self.lineEdit.setCompleter(completer)
        self.lineEdit.textChanged.connect(completer.update)
        self.lineEdit.editingFinished.connect(self.refresh_TextEdit)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_5.setReadOnly(True)
        self.progressBar.setStyleSheet("QProgressBar { border: 2px solid orange; border-radius: 10px; color: rgb(20,20,20);  background-color: #FFFFFF; text-align: center;}QProgressBar::chunk {background-color: rgb(100,200,200); border-radius: 25px; margin: 0.1px;  width: 1px;}")
        self.progressBar.setValue(0)
        self.worker = Worker()
        self.worker.current_time.connect(self._current_time)
        self.internet = Internet()
        self.internet.host_name_S.connect(partial(self._internet_state))
        self.worker.start()
        self.internet.start()
        self.spinBox.valueChanged.connect(self.on_spinbox_value_changed)
        item_state = ["本地优先","联网优先"]
        self.comboBox_4.addItems(item_state)
        self.pushButton_10.setEnabled(False)
        self.pushButton_11.setEnabled(False)
        theme_items = ["default_theme",'dark_amber.xml',
         'dark_blue.xml',
         'dark_cyan.xml',
         'dark_lightgreen.xml',
         'dark_pink.xml',
         'dark_purple.xml',
         'dark_red.xml',
         'dark_teal.xml',
         'dark_yellow.xml',
         'light_amber.xml',
         'light_blue.xml',
         'light_cyan.xml',
         'light_cyan_500.xml',
         'light_lightgreen.xml',
         'light_pink.xml',
         'light_purple.xml',
         'light_red.xml',
         'light_teal.xml',
         'light_yellow.xml']
        self.comboBox_3.addItems(theme_items)
        if theme_ == "default_theme":
            fusion_style = QStyleFactory.create("Fusion")
            self.setStyle(fusion_style)
        else:
            apply_stylesheet(self, theme=theme_)
        self.pushButton.clicked.connect(self.search_word)
        self.pushButton_2.clicked.connect(self.gb_mp3_get)
        self.pushButton_3.clicked.connect(self.us_mp3_get)
        self.pushButton_4.clicked.connect(self.add_new_wordbook)
        self.pushButton_5.clicked.connect(self.creat_new_file)
        self.pushButton_6.clicked.connect(self.open_file)
        self.pushButton_7.clicked.connect(self.save_json)
        self.pushButton_12.clicked.connect(self.start)
        self.pushButton_13.clicked.connect(self.open_folder)
        self.pushButton_14.clicked.connect(self.paste_conntent)
        self.pushButton_15.clicked.connect(self.open_ocr)
        self.pushButton_16.clicked.connect(self.import_raw_text)
        self.pushButton_18.clicked.connect(self.translate_text)
        self.pushButton_19.clicked.connect(self.website_jump)
        self.pushButton_8.clicked.connect(self.gb_mp3_get_2)
        self.pushButton_9.clicked.connect(self.us_mp3_get_2)
        self.pushButton_10.clicked.connect(self.access)
        self.pushButton_11.clicked.connect(self.fail)
        self.pushButton_28.clicked.connect(self.refresh_IDText_4)
        self.pushButton_29.clicked.connect(self.refresh_IDText_5)
        self.pushButton_30.clicked.connect(self.refresh_IDText_6)
        self.pushButton_31.clicked.connect(self.refresh_IDText_7)
        self.pushButton_24.clicked.connect(self.website_jump_2)
        self.pushButton_25.clicked.connect(self.website_jump_3)
        self.pushButton_26.clicked.connect(self.website_jump_4)
        self.pushButton_27.clicked.connect(self.website_jump_5)
        self.pushButton_34.clicked.connect(self.website_jump_6)
        self.pushButton_20.clicked.connect(self.search)
        self.pushButton_23.clicked.connect(self.combination)
        self.pushButton_21.clicked.connect(self.gb_download)
        self.pushButton_22.clicked.connect(self.us_download)
        self.pushButton_32.clicked.connect(self.clear_cache)
        self.pushButton_33.clicked.connect(self.get_selected_items)
        self.treeWidget.itemClicked.connect(self.on_item_clicked_1)
        self.treeWidget_3.itemClicked.connect(self.on_item_clicked_1)
        self.checkBox.stateChanged.connect(self.on_checkbox_state_changed)
        self.comboBox_3.currentIndexChanged.connect(self.on_combobox_changed)
        self.line_text_show()
        self.combox_show()
        self.setup_context_menu_treeWidget()
        self.setup_context_menu_textedit()
        self.history_list()
    def on_combobox_changed(self,index):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        theme_path = d + "/resource/Theme.txt"
        selected_text = self.comboBox_3.currentText()
        if selected_text == "default_theme":
            fusion_style = QStyleFactory.create("Fusion")
            self.setStyle(fusion_style)
        else:
            apply_stylesheet(self, theme=selected_text)
        with open(theme_path,"w") as f:
            f.write(selected_text)
    def setup_context_menu_textedit(self):
        self.tab_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tab_2.customContextMenuRequested.connect(self.show_context_menu_textedit)
        self.hide_action = QAction("隐藏释义",self)
        self.show_action = QAction("显示释义",self)
        self.hide_action.triggered.connect(self.hide_text)
        self.show_action.triggered.connect(self.show_text)
    def show_context_menu_textedit(self, position):
        self.menu = QMenu(self.tab_2)
        self.menu.addAction(self.show_action)
        self.menu.addAction(self.hide_action)
        self.menu.exec_(self.tab_2.mapToGlobal(position))
    def hide_text(self):
        self.textEdit_2.setHidden(True)
    def show_text(self):
        self.textEdit_2.setHidden(False)
    def access(self):
        self.progressBar.setValue(0)
        self.label_6.setText("0")
    def fail(self):
        self.timer1.stop()
        self.progressBar.setValue(0)
        self.label_6.setText("0")
        self.pushButton_12.setText("\n开始\n")
        self.textEdit_2.setHidden(False)
        word_book_path = self.lineEdit_3.text()
        if word_book_path:
            word_book_path_ = QFile(word_book_path)
            if word_book_path_.exists():
                word = self.label_4.text()
                text = word
                top_level_item_count = self.treeWidget.topLevelItemCount()
                for i in range(top_level_item_count):
                    top_level_item = self.treeWidget.topLevelItem(i)
                    if top_level_item is not None:
                        for i in range(top_level_item.childCount()):
                            item2 = top_level_item.child(i)
                            if item2 is not None:
                                item2_T = item2.text(0)
                                if item2_T == text:
                                    red_color = QColor(255, 0, 0)
                                    item2.setForeground(0, red_color)
                                    self.treeWidget.setCurrentItem(item2)  # 选中子项2
                                    break
                top_level_item_count = self.treeWidget_3.topLevelItemCount()
                word_list_temp = []
                for i in range(top_level_item_count):
                    top_level_item = self.treeWidget_3.topLevelItem(i)
                    if top_level_item is not None:
                        for i in range(top_level_item.childCount()):
                            item2 = top_level_item.child(i)
                            if item2 is not None:
                                item2_T = item2.text(0)
                                if item2_T in word_list_temp:
                                    pass
                                else:
                                    word_list_temp.append(item2_T)
                if word in word_list_temp:
                    pass
                else:
                    word_list_temp.append(word)
                    word_list_temp.sort()
                    self.treeWidget_3.clear()
                    for word in word_list_temp:
                        parent_item = None
                        first_letter = word[0].upper()
                        for i in range(self.treeWidget_3.topLevelItemCount()):
                            item = self.treeWidget_3.topLevelItem(i)
                            if item.text(0) == first_letter:
                                parent_item = item
                                break
                        if not parent_item:
                            parent_item = QTreeWidgetItem(self.treeWidget_3, [first_letter])
                        child_item = QTreeWidgetItem(parent_item, [word])
                top_level_item_count = self.treeWidget_3.topLevelItemCount()
                word_list_temp = []
                for i in range(top_level_item_count):
                    top_level_item = self.treeWidget_3.topLevelItem(i)
                    if top_level_item is not None:
                        for i in range(top_level_item.childCount()):
                            item2 = top_level_item.child(i)
                            if item2 is not None:
                                item2_T = item2.text(0)
                                word_list_temp.append(item2_T)
                data_save = {"list":word_list_temp}
                word_book_path = self.lineEdit_3.text()
                if word_book_path:
                    word_book_path_ = QFile(word_book_path)
                    if word_book_path_.exists():
                        with open(word_book_path ,'w') as f:
                            json.dump(data_save, f)
            else:
                message_box = QMessageBox()
                message_box.setWindowTitle("警告")
                message_box.setText("该路径下单词本不存在，请检查单词本是否存在！")
                message_box.setIcon(QMessageBox.Warning)
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec()
        else:
            message_box = QMessageBox()
            message_box.setWindowTitle("警告")
            message_box.setText("添加失败，未打开单词本！")
            message_box.setIcon(QMessageBox.Warning)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()
    def on_checkbox_state_changed(self,state):
        if state == 2:
            self.comboBox_4.setCurrentIndex(1)
        else:
            self.comboBox_4.setCurrentIndex(0)
    def on_item_clicked_1(self,item):
        word_text = item.text(0)
        self.textEdit_2.setHidden(False)
        self.timer1.stop()
        self.progressBar.setValue(0)
        self.label_6.setText("0")
        self.pushButton_12.setText("\n开始\n")
        policy = self.comboBox_4.currentText()
        if policy == "联网优先":
            self.label_4.setText(word_text)
            if word_text:
                accent,meaning,sentence,phrase = InternetSearch.get_word_meaning(word_text)
                if accent != "网络状态异常，请检查网络连接！":
                    accent_t = ""
                    meaning_t = ""
                    phrase_t = ""
                    sentence_t = ""
                    for accent_ in accent:
                        accent_t += accent_
                    for meaning_ in meaning:
                        meaning_t += meaning_
                        meaning_t += "\n"
                    for phrase_ in phrase:
                        for phrase__ in phrase_:
                            phrase_t += phrase__
                            phrase_t += "\n"
                    for sentence_ in sentence:
                        for sentence__ in sentence_:
                            sentence_t += sentence__
                            sentence_t += "\n"
                    self.label_5.setText(accent_t)
                    TextT = meaning_t + "\n\n" + phrase_t + "\n\n" + sentence_t
                    self.textEdit_2.setText(TextT)
        else:
            self.label_4.setText(word_text)
            a = os.path.abspath('.')
            b = a.split("\\")
            c = tuple(b)
            d = '/'.join(c)
            word_to_lookup = word_text
            if bool(word_to_lookup):
                rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
                word = re.sub(rstr, "_", word_to_lookup)
                word = word.replace(" ", "_")
                file_path = d + f"/gb_mp3/{word}.mp3"  # 替换为你的音频文件路径
                file_path2 = d + f"/us_mp3/{word}.mp3"
                file = QFile(file_path)
                file2 = QFile(file_path2)
                if file.exists():
                    self.pushButton_8.setEnabled(True)
                else:
                    self.pushButton_8.setEnabled(False)
                if file2.exists():
                    self.pushButton_9.setEnabled(True)
                else:
                    self.pushButton_9.setEnabled(False)
                words_file = d + "/words/" + word + ".json"
                Q_words_file = QFile(words_file)
                if Q_words_file.exists():
                    try:
                        with open(f"words/{word}.json", "r") as file:
                            word_info = json.load(file)
                        multi_line_text = f"""
                        <b>单词:</b><br/>{word_info["word"]}<br/>
                        <b>中文意思:</b><br/>{word_info["mean_cn"]}<br/>
                        <b>英文解释:</b><br/>{word_info["mean_en"]}<br/>
                        <b>英文例句:</b><br/>{word_info["sentence"]}<br/>
                        <b>英文例句翻译:</b><br/>{word_info["sentence_trans"]}<br/>
                        <b>相关的短语:</b><br/>{word_info["sentence_phrase"]}<br/>
                        <b>单词词源:</b><br/>{word_info["word_etyma"]}<br/>
                        <b>其他数据:</b><br/>{word_info["cloze_data"]}<br/>
                        """
                        self.textEdit_2.clear()
                        self.textEdit_2.setHtml(multi_line_text)
                        self.label_5.setText(word_info["accent"])
                    except FileNotFoundError:
                        error_text = "The word does not exist in the word book, or please confirm that the word entered is correct！"
                        self.textEdit_2.clear()
                        self.textEdit_2.setPlainText(error_text)
                        self.label_5.setText("")
                else:
                    try:
                        with open(f"words_internet/{word}.json", "r") as file:
                            word_info = json.load(file)
                        multi_line_text = f"""
                        <b>单词:</b><br/>{word_info["word"]}<br/>
                        <b>中文意思:</b><br/>{word_info["meaning"]}<br/>
                        <b>例句:</b><br/>{word_info["sentence"]}<br/>
                        <b>相关短语:</b><br/>{word_info["phrase"]}<br/>
                        """
                        self.textEdit_2.clear()
                        self.textEdit_2.setHtml(multi_line_text)
                        self.label_5.setText(word_info["accent"])
                    except FileNotFoundError:
                        error_text = "The word does not exist in the word book, or please confirm that the word entered is correct！"
                        self.textEdit_2.clear()
                        self.textEdit_2.setPlainText(error_text)
                        self.label_5.setText("")
        self.us_mp3_get_2()
    def setup_context_menu_treeWidget(self):
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.show_context_menu_treeWidget)
        self.import_action = QAction("导入单词本",self)
        self.reset_action = QAction("重置进度",self)
        self.clear_action = QAction('清空', self)
        self.reset_action.triggered.connect(self.reset_word_test)
        self.import_action.triggered.connect(self.import_word_book)
        self.clear_action.triggered.connect(self.clear_treeWidget)
    def show_context_menu_treeWidget(self, position):
        self.menu = QMenu(self.treeWidget)
        self.menu.addAction(self.import_action)
        self.menu.addAction(self.reset_action)
        self.menu.addAction(self.clear_action)
        self.menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
    def start(self):
        top_level_item_count = self.treeWidget.topLevelItemCount()
        if top_level_item_count:
            for i in range(self.treeWidget.topLevelItemCount()):
                item = self.treeWidget.topLevelItem(i)
                if not item.isExpanded():
                    self.treeWidget.expandItem(item)
            pushButton_text = self.pushButton_12.text()
            if pushButton_text == "\n开始\n":
                self.pushButton_12.setText("\n暂停\n")
                self.pushButton_10.setEnabled(True)
                self.pushButton_11.setEnabled(True)
                self.textEdit_2.setHidden(True)
                self.timer1.start(1000)
            else:
                self.timer1.stop()
                self.pushButton_10.setEnabled(False)
                self.pushButton_11.setEnabled(False)
                self.pushButton_12.setText("\n开始\n")
        else:
            message_box = QMessageBox()
            message_box.setWindowTitle("警告")
            message_box.setText("未导入单词本，请先导入单词本！")
            message_box.setIcon(QMessageBox.Warning)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()
    def import_word_book(self):
        if 1:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, 'Open JSON File', '', 'JSON Files (*.json)')
            if file_path:
                self.treeWidget.clear()
                with open(file_path, 'r') as file:
                    data = json.load(file)["list"]
                    if bool(data):
                        data.sort()
                for word in data:
                    parent_item = None
                    first_letter = word[0].upper()
                    for i in range(self.treeWidget.topLevelItemCount()):
                        item = self.treeWidget.topLevelItem(i)
                        if item.text(0) == first_letter:
                            parent_item = item
                            break
                    if not parent_item:
                        parent_item = QTreeWidgetItem(self.treeWidget, [first_letter])
                    child_item = QTreeWidgetItem(parent_item, [word])
                data = {'list': ''}
                file_path_fail = file_path[0:-5] + "_fail.json"
                file_path_fail_q = QFile(file_path_fail)
                if file_path_fail_q.exists():
                    self.lineEdit_3.setText(file_path_fail)
                    with open(file_path_fail, 'r') as file:
                        data = json.load(file)["list"]
                        if bool(data):
                            data.sort()
                    for word in data:
                        parent_item = None
                        first_letter = word[0].upper()
                        for i in range(self.treeWidget_3.topLevelItemCount()):
                            item = self.treeWidget_3.topLevelItem(i)
                            if item.text(0) == first_letter:
                                parent_item = item
                                break
                        if not parent_item:
                            parent_item = QTreeWidgetItem(self.treeWidget_3, [first_letter])
                        child_item = QTreeWidgetItem(parent_item, [word])
                else:
                    with open(file_path_fail, 'w') as file:
                        json.dump(data, file, indent=4)
                    self.lineEdit_3.setText(file_path_fail)
    def clear_treeWidget(self):
        self.treeWidget.clear()
        self.treeWidget_3.clear()
        self.timer1.stop()
        self.progressBar.setValue(0)
        self.label_6.setText("0")
    def line_text_show(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        T_S_path = d + "/resource/Translation.txt"
        with open(T_S_path,"r") as f:
            all_ = f.readlines()
            APP_ID = all_[0][3:-1]
            APP_SECRET = all_[1][7:-1]
        self.lineEdit_4.setText(APP_ID)
        self.lineEdit_5.setText(APP_SECRET)
    def combox_show(self):
        items_from = ["自动检测-auto","中文-zh","英语-en","繁体中文-cht","粤语-yue","文言文-wyw","日语-jp",
        "韩语-kor","法语-fra","西班牙语-spa","泰语-th","阿拉伯语-ara","俄语-ru","葡萄牙语-pt","德语-de",
        "意大利语-it","希腊语-el","荷兰语-nl","波兰语-pl","保加利亚语-bul","爱沙尼亚语-est","丹麦语-dan",
        "芬兰语-fin","捷克语-cs","罗马尼亚语-rom","斯洛文尼亚语-slo","瑞典语-swe","匈牙利语-hu","越南语-vie"]
        items_to = ["中文-zh","英语-en","繁体中文-cht","粤语-yue","文言文-wyw","日语-jp",
        "韩语-kor","法语-fra","西班牙语-spa","泰语-th","阿拉伯语-ara","俄语-ru","葡萄牙语-pt","德语-de",
        "意大利语-it","希腊语-el","荷兰语-nl","波兰语-pl","保加利亚语-bul","爱沙尼亚语-est","丹麦语-dan",
        "芬兰语-fin","捷克语-cs","罗马尼亚语-rom","斯洛文尼亚语-slo","瑞典语-swe","匈牙利语-hu","越南语-vie"]
        self.comboBox.addItems(items_from)
        self.comboBox_2.addItems(items_to)
    def refresh_IDText_4(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        T_S_path = d + "/resource/Translation.txt"
        new_content = self.lineEdit_7.text()
        with open(T_S_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines[0] = "ID=" + new_content + '\n'  # 修改第一行内容
        with open(T_S_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
    def refresh_IDText_5(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        T_S_path = d + "/resource/Translation.txt"
        new_content = self.lineEdit_8.text()
        with open(T_S_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines[1] = "SECRET=" + new_content + '\n'  # 修改第二行内容
        with open(T_S_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)    
    def refresh_IDText_6(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        T_S_path = d + "/resource/Identification.txt"
        new_content = self.lineEdit_9.text()
        with open(T_S_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines[0] = "ID=" + new_content + '\n'  # 修改第一行内容
        with open(T_S_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
    def refresh_IDText_7(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        T_S_path = d + "/resource/Identification.txt"
        new_content = self.lineEdit_10.text()
        with open(T_S_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines[1] = "SECRET=" + new_content + '\n'  # 修改第二行内容
        with open(T_S_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)    
    def _current_time(self,current_datetime):
    	self.label_3.setText(current_datetime)
    def _internet_state(self,host,in_ip,out_ip,ip_address,receive_b,send_b,cpu_num):
        text = host + "\n" + in_ip + "\n" + out_ip + "\n" + ip_address + "\n" + cpu_num
        self.label_12.setText(text)
        text2 = send_b + "\n" + receive_b
        self.label_2.setText(text2)
    def refresh_TextEdit(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        word_to_lookup = self.lineEdit.text()
        if bool(word_to_lookup):
            rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
            word = re.sub(rstr, "_", word_to_lookup)
            word = word.replace(" ", "_")
            file_path = d + f"/gb_mp3/{word}.mp3"  # 替换为你的音频文件路径
            file_path2 = d + f"/us_mp3/{word}.mp3"
            file = QFile(file_path)
            file2 = QFile(file_path2)
            if file.exists():
                self.pushButton_2.setEnabled(True)
            else:
                self.pushButton_2.setEnabled(False)
            if file2.exists():
                self.pushButton_3.setEnabled(True)
            else:
                self.pushButton_3.setEnabled(False)
            try:
                with open(f"words/{word}.json", "r") as file:
                    word_info = json.load(file)
                multi_line_text = f"""
                <b>单词:</b><br/>{word_info["word"]}<br/>
                <b>中文意思:</b><br/>{word_info["mean_cn"]}<br/>
                <b>英文解释:</b><br/>{word_info["mean_en"]}<br/>
                <b>英文例句:</b><br/>{word_info["sentence"]}<br/>
                <b>英文例句翻译:</b><br/>{word_info["sentence_trans"]}<br/>
                <b>相关的短语:</b><br/>{word_info["sentence_phrase"]}<br/>
                <b>单词词源:</b><br/>{word_info["word_etyma"]}<br/>
                <b>其他数据:</b><br/>{word_info["cloze_data"]}<br/>
                """
                self.textEdit.clear()
                self.textEdit.setHtml(multi_line_text)
                self.label.setText(word_info["accent"])
            except FileNotFoundError:
                error_text = "The word does not exist in the word book, or please confirm that the word entered is correct！"
                self.textEdit.clear()
                self.textEdit.setPlainText(error_text)
                self.label.setText("")
    def gb_mp3_get(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        word_to_lookup = self.lineEdit.text()
        if bool(word_to_lookup):
            rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
            word = re.sub(rstr, "_", word_to_lookup)
            word = word.replace(" ", "_")
            file_path = d + f"/gb_mp3/{word}.mp3"  # 替换为你的音频文件路径
            file = QFile(file_path)
            if file.exists():
                self.player.setSource(QUrl.fromLocalFile(file_path))
                self.player.play()
    def us_mp3_get(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        word_to_lookup = self.lineEdit.text()
        if bool(word_to_lookup):
            rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
            word = re.sub(rstr, "_", word_to_lookup)
            word = word.replace(" ", "_")
            file_path = d + f"/us_mp3/{word}.mp3"  # 替换为你的音频文件路径
            file = QFile(file_path)
            if file.exists():
                self.player.setSource(QUrl.fromLocalFile(file_path))
                self.player.play()
    def creat_new_file(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(self, "Creat JSON File", "", "JSON Files (*.json)", options=options)
        if filePath:
            self.lineEdit_2.setText(filePath)
            data = {'list': ''}  # 要保存的 JSON 数据
            with open(filePath, 'w') as file:
                json.dump(data, file, indent=4)
            with open("history.json","r") as f:
                history_info = json.load(f)
                history_list = history_info["history"]
            if filePath in history_list:
                pass
            else:
                history_list.append(filePath)
            data = {"history":history_list}
            with open("history.json","w") as f:
                json.dump(data,f)
            self.history_list()
    def open_file(self):
        if 1:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, 'Open JSON File', '', 'JSON Files (*.json)')
            if file_path:
                self.lineEdit_2.setText(file_path)
                self.treeWidget_2.clear()
                with open(file_path, 'r') as file:
                    data = json.load(file)["list"]
                    if bool(data):
                        data.sort()
                # 添加单词到 QTreeWidget
                for word in data:
                    parent_item = None
                    first_letter = word[0].upper()
                    # 找到或创建首字母的父节点
                    for i in range(self.treeWidget_2.topLevelItemCount()):
                        item = self.treeWidget_2.topLevelItem(i)
                        if item.text(0) == first_letter:
                            parent_item = item
                            break
                    if not parent_item:
                        parent_item = QTreeWidgetItem(self.treeWidget_2, [first_letter])

                    child_item = QTreeWidgetItem(parent_item, [word])
    def search_word(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        word_internet = d + "/words_internet/"
        if self.checkBox.isChecked():
            word_text = self.lineEdit.text()
            if word_text:
                accent,meaning,sentence,phrase = InternetSearch.get_word_meaning(word_text)
                if accent != "网络状态异常，请检查网络连接！":
                    accent_t = ""
                    meaning_t = ""
                    phrase_t = ""
                    sentence_t = ""
                    for accent_ in accent:
                        accent_t += accent_
                    for meaning_ in meaning:
                        meaning_t += meaning_
                        meaning_t += "\n"
                    for phrase_ in phrase:
                        for phrase__ in phrase_:
                            phrase_t += phrase__
                            phrase_t += "\n"
                    for sentence_ in sentence:
                        for sentence__ in sentence_:
                            sentence_t += sentence__
                            sentence_t += "\n"
                    self.label.setText(accent_t)
                    TextT = meaning_t + "\n\n" + phrase_t + "\n\n" + sentence_t
                    self.textEdit.setText(TextT)
                    data = {"word":word_text,"accent":accent,"meaning": meaning, "sentence": sentence, "phrase": phrase}
                    path_open = word_internet + word_text + ".json"
                    with open(path_open,"w") as f:
                        json.dump(data,f)
        else:
            self.refresh_TextEdit()
    def add_new_wordbook(self):
        word_book_path = self.lineEdit_2.text()
        if word_book_path:
            word_book_path_ = QFile(word_book_path)
            if word_book_path_.exists():
                word = self.lineEdit.text()
                top_level_item_count = self.treeWidget_2.topLevelItemCount()
                word_list_temp = []
                for i in range(top_level_item_count):
                    top_level_item = self.treeWidget_2.topLevelItem(i)
                    if top_level_item is not None:
                        for i in range(top_level_item.childCount()):
                            item2 = top_level_item.child(i)
                            if item2 is not None:
                                item2_T = item2.text(0)
                                if item2_T in word_list_temp:
                                    pass
                                else:
                                    word_list_temp.append(item2_T)
                if word in word_list_temp:
                    pass
                else:
                    word_list_temp.append(word)
                    word_list_temp.sort()
                    self.treeWidget_2.clear()
                    for word in word_list_temp:
                        parent_item = None
                        first_letter = word[0].upper()
                            # 找到或创建首字母的父节点
                        for i in range(self.treeWidget_2.topLevelItemCount()):
                            item = self.treeWidget_2.topLevelItem(i)
                            if item.text(0) == first_letter:
                                parent_item = item
                                break
                        if not parent_item:
                            parent_item = QTreeWidgetItem(self.treeWidget_2, [first_letter])
                        child_item = QTreeWidgetItem(parent_item, [word])
            else:
                message_box = QMessageBox()
                message_box.setWindowTitle("警告")
                message_box.setText("该路径下单词本不存在，请检查单词本是否存在！")
                message_box.setIcon(QMessageBox.Warning)
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec()
        else:
            message_box = QMessageBox()
            message_box.setWindowTitle("警告")
            message_box.setText("添加失败，未打开单词本！")
            message_box.setIcon(QMessageBox.Warning)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()
    def save_json(self):
        top_level_item_count = self.treeWidget_2.topLevelItemCount()
        word_list_temp = []
        for i in range(top_level_item_count):
            top_level_item = self.treeWidget_2.topLevelItem(i)
            if top_level_item is not None:
                for i in range(top_level_item.childCount()):
                    item2 = top_level_item.child(i)
                    if item2 is not None:
                        item2_T = item2.text(0)
                        word_list_temp.append(item2_T)
        data_save = {"list":word_list_temp}
        word_book_path = self.lineEdit_2.text()
        if word_book_path:
            word_book_path_ = QFile(word_book_path)
            if word_book_path_.exists():
                with open(word_book_path ,'w') as f:
                    json.dump(data_save, f)
    def paste_conntent(self):
        clipboard_content = pyperclip.paste()
        self.textEdit_3.setText(clipboard_content)
    def open_ocr(self):
        self.picture_ocr_ = picture_ocr()
        self.picture_ocr_.show()
    def import_raw_text(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open TEXT File', '', 'TEXT Files (*.txt)')
        file_path_ = QFile(file_path)
        if file_path and file_path_.exists():
            with open(file_path,"r") as file:
                txt = file.read()
                self.textEdit_3.setText(txt)
    def translate_text(self):
        from_lang = self.comboBox.currentText()
        from_lang_l = from_lang.split("-")
        from_lang = from_lang_l[1]
        to_lang = self.comboBox_2.currentText()
        to_lang_l = to_lang.split("-")
        to_lang = to_lang_l[1]
        raw_text = self.textEdit_3.toPlainText()
        raw_text_l = raw_text.split("\n")
        ripe_text_l = []
        for sentence in raw_text_l:
            ripe_text = InternetTranslation.translation(sentence,from_lang,to_lang)
            ripe_text_l.append(ripe_text)
            time.sleep(1)
        ripe_text_l_ = "\n".join(ripe_text_l)
        self.textEdit_4.setText(ripe_text_l_)
    def count_down(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        num_path = d + "/resource/number.txt"
        countdown_path = d + "/resource/countdown.txt"
        current_value = self.progressBar.value()
        if current_value == 0:
            with open(countdown_path,"r") as f:
                countdown_num = f.read()
            countdown_num = int(countdown_num)
            current_value = countdown_num
            self.progressBar.setValue(current_value)
            self.label_6.setText(str(current_value))
            top_level_item_count = self.treeWidget.topLevelItemCount()
            word_list_temp = []
            for i in range(top_level_item_count):
                top_level_item = self.treeWidget.topLevelItem(i)
                if top_level_item is not None:
                    for i in range(top_level_item.childCount()):
                        item2 = top_level_item.child(i)
                        if item2 is not None:
                            item2_T = item2.text(0)
                            if item2_T in word_list_temp:
                                pass
                            else:
                                word_list_temp.append(item2_T)
            with open(num_path,"r") as f:
                current_num = f.read()
                current_num = int(current_num)
            text = word_list_temp[current_num]
            self.label_4.setText(text)
            for i in range(top_level_item_count):
                top_level_item = self.treeWidget.topLevelItem(i)
                if top_level_item is not None:
                    for i in range(top_level_item.childCount()):
                        item2 = top_level_item.child(i)
                        if item2 is not None:
                            item2_T = item2.text(0)
                            if item2_T == text:
                                blue_color = QColor(0, 0, 255)
                                item2.setForeground(0, blue_color)
                                self.treeWidget.setCurrentItem(item2)  # 选中子项2
                                break
            policy = self.comboBox_4.currentText()
            if policy == "联网优先":
                word_text = self.label_4.text()
                if word_text:
                    accent,meaning,sentence,phrase = InternetSearch.get_word_meaning(word_text)
                    if accent != "网络状态异常，请检查网络连接！":
                        accent_t = ""
                        meaning_t = ""
                        phrase_t = ""
                        sentence_t = ""
                        for accent_ in accent:
                            accent_t += accent_
                        for meaning_ in meaning:
                            meaning_t += meaning_
                            meaning_t += "\n"
                        for phrase_ in phrase:
                            for phrase__ in phrase_:
                                phrase_t += phrase__
                                phrase_t += "\n"
                        for sentence_ in sentence:
                            for sentence__ in sentence_:
                                sentence_t += sentence__
                                sentence_t += "\n"
                        self.label_5.setText(accent_t)
                        TextT = meaning_t + "\n\n" + phrase_t + "\n\n" + sentence_t
                        self.textEdit_2.setText(TextT)
            else:
                a = os.path.abspath('.')
                b = a.split("\\")
                c = tuple(b)
                d = '/'.join(c)
                word_to_lookup = text
                if bool(word_to_lookup):
                    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
                    word = re.sub(rstr, "_", word_to_lookup)
                    word = word.replace(" ", "_")
                    file_path = d + f"/gb_mp3/{word}.mp3"  # 替换为你的音频文件路径
                    file_path2 = d + f"/us_mp3/{word}.mp3"
                    file = QFile(file_path)
                    file2 = QFile(file_path2)
                    if file.exists():
                        self.pushButton_8.setEnabled(True)
                    else:
                        self.pushButton_8.setEnabled(False)
                    if file2.exists():
                        self.pushButton_9.setEnabled(True)
                    else:
                        self.pushButton_9.setEnabled(False)
                    words_file = d + "/words/" + word + ".json"
                    Q_words_file = QFile(words_file)
                    if Q_words_file.exists():
                        try:
                            with open(f"words/{word}.json", "r") as file:
                                word_info = json.load(file)
                            multi_line_text = f"""
                            <b>单词:</b><br/>{word_info["word"]}<br/>
                            <b>中文意思:</b><br/>{word_info["mean_cn"]}<br/>
                            <b>英文解释:</b><br/>{word_info["mean_en"]}<br/>
                            <b>英文例句:</b><br/>{word_info["sentence"]}<br/>
                            <b>英文例句翻译:</b><br/>{word_info["sentence_trans"]}<br/>
                            <b>相关的短语:</b><br/>{word_info["sentence_phrase"]}<br/>
                            <b>单词词源:</b><br/>{word_info["word_etyma"]}<br/>
                            <b>其他数据:</b><br/>{word_info["cloze_data"]}<br/>
                            """
                            self.textEdit_2.clear()
                            self.textEdit_2.setHtml(multi_line_text)
                            self.label_5.setText(word_info["accent"])
                        except FileNotFoundError:
                            error_text = "The word does not exist in the word book, or please confirm that the word entered is correct！"
                            self.textEdit_2.clear()
                            self.textEdit_2.setPlainText(error_text)
                            self.label_5.setText("")
                    else:
                        try:
                            with open(f"words_internet/{word}.json", "r") as file:
                                word_info = json.load(file)
                            multi_line_text = f"""
                            <b>单词:</b><br/>{word_info["word"]}<br/>
                            <b>中文意思:</b><br/>{word_info["meaning"]}<br/>
                            <b>例句:</b><br/>{word_info["sentence"]}<br/>
                            <b>相关短语:</b><br/>{word_info["phrase"]}<br/>
                            """
                            self.textEdit_2.clear()
                            self.textEdit_2.setHtml(multi_line_text)
                            self.label_5.setText(word_info["accent"])
                        except FileNotFoundError:
                            error_text = "The word does not exist in the word book, or please confirm that the word entered is correct！"
                            self.textEdit_2.clear()
                            self.textEdit_2.setPlainText(error_text)
                            self.label_5.setText("")
            len_all_word = len(word_list_temp)
            with open(num_path,"r") as f:
                current_num = f.read()
            current_num = int(current_num) + 1
            current_num = str(current_num)
            with open(num_path,"w") as f:
                f.write(current_num)
            self.us_mp3_get_2()
            num = len(word_list_temp)
            with open(num_path,"r") as f:
                current_num = f.read()
            current_num = int(current_num)
            if current_num == num:
                current_num = "0"
                with open(num_path,"w") as f:
                    f.write(current_num)
        else:
            current_value -= 1
            self.progressBar.setValue(current_value)
            self.label_6.setText(str(current_value))
    def reset_word_test(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        num_path = d + "/resource/number.txt"
        current_num = "0"
        with open(num_path,"w") as f:
            f.write(current_num)
        top_level_item_count = self.treeWidget.topLevelItemCount()
        for i in range(top_level_item_count):
            top_level_item = self.treeWidget.topLevelItem(i)
            if top_level_item is not None:
                for i in range(top_level_item.childCount()):
                    item2 = top_level_item.child(i)
                    black_color = QColor(0, 0, 0)
                    item2.setForeground(0, black_color)
                    self.treeWidget.setCurrentItem(item2)  # 选中子项2
        self.timer1.stop()
        self.progressBar.setValue(0)
        self.pushButton_12.setText("\n开始\n")
        self.label_6.setText("0")
    def website_jump(self):
        url = QUrl('https://fanyi-api.baidu.com/manage/developer')  # 指定要跳转的链接
        QDesktopServices.openUrl(url)
    def gb_mp3_get_2(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        word_to_lookup = self.label_4.text()
        if bool(word_to_lookup):
            rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
            word = re.sub(rstr, "_", word_to_lookup)
            word = word.replace(" ", "_")
            file_path = d + f"/gb_mp3/{word}.mp3"  # 替换为你的音频文件路径
            file = QFile(file_path)
            if file.exists():
                self.player.setSource(QUrl.fromLocalFile(file_path))
                self.player.play()
    def us_mp3_get_2(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        word_to_lookup = self.label_4.text()
        if bool(word_to_lookup):
            rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
            word = re.sub(rstr, "_", word_to_lookup)
            word = word.replace(" ", "_")
            file_path = d + f"/us_mp3/{word}.mp3"  # 替换为你的音频文件路径
            file = QFile(file_path)
            if file.exists():
                self.player.setSource(QUrl.fromLocalFile(file_path))
                self.player.play()
    def on_spinbox_value_changed(self, value):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        countdown_path = d + "/resource/countdown.txt"
        self.progressBar.setMaximum(value)
        self.progressBar.setValue(0)
        self.label_6.setText("0")
        value = str(value)
        with open(countdown_path,"w") as f:
            f.write(value)
    def website_jump_2(self):
        url = QUrl('https://fanyi-api.baidu.com/')  # 指定要跳转的链接
        QDesktopServices.openUrl(url)
    def website_jump_3(self):
        url = QUrl('https://fanyi-api.baidu.com/product/11')  # 指定要跳转的链接
        QDesktopServices.openUrl(url)
    def website_jump_4(self):
        url = QUrl('https://cloud.baidu.com/')  # 指定要跳转的链接
        QDesktopServices.openUrl(url)
    def website_jump_5(self):
        url = QUrl('https://cloud.baidu.com/products/index.html')  # 指定要跳转的链接
        QDesktopServices.openUrl(url)
    def open_folder(self):
        folder_path = self.lineEdit_3.text()  # 替换为你要打开的文件夹路径
        folder_path = folder_path.split("/")
        folder_path.pop(-1)
        folder_path = tuple(folder_path)
        folder_path = "/".join(folder_path)
        if os.path.isdir(folder_path):  # 检查文件夹路径是否存在
            os.startfile(folder_path)  # 使用默认文件管理器打开文件夹
        else:
            print("文件夹路径无效")
    def website_jump_6(self):
        url = QUrl('https://blog.csdn.net/qq_44768504/article/details/122017821')
        QDesktopServices.openUrl(url)
    def search(self):
        word = self.lineEdit_6.text()
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        word = re.sub(rstr, "_", word)
        word = word.replace(" ", "_")
        word = word[0].lower() + word[1:]
        state1 = MP3.gb_audio_state(word)
        state2 = MP3.us_audio_state(word)
        message_text = ""
        if state1 == "ok":
            self.pushButton_21.setEnabled(True)
            message_text += "英音存在资源，可下载；"
        else:
            self.pushButton_21.setEnabled(False)
            message_text += "英音不存在资源，不可下载；"
        if state2 == "ok":
            self.pushButton_22.setEnabled(True)
            message_text += "美音存在资源，可下载！"
        else:
            self.pushButton_22.setEnabled(False)
            message_text += "美音不存在资源，不可下载！"
        message_box = QMessageBox()
        message_box.setWindowTitle("查询结果")
        message_box.setText(message_text)
        message_box.setIcon(QMessageBox.Information)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()
    def gb_download(self):
        word = self.lineEdit_6.text()
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        word = re.sub(rstr, "_", word)
        word = word.replace(" ", "_")
        word = word[0].lower() + word[1:]
        w,s = MP3.download_audio_gb(word)
        if s == "gb_ok":
            message_text = "英音下载完成！"
        else:
            message_text = "英音下载失败！"
        message_box = QMessageBox()
        message_box.setWindowTitle("下载结果")
        message_box.setText(message_text)
        message_box.setIcon(QMessageBox.Information)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()
    def us_download(self):
        word = self.lineEdit_6.text()
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        word = re.sub(rstr, "_", word)
        word = word.replace(" ", "_")
        word = word[0].lower() + word[1:]
        w,s = MP3.download_audio_us(word)
        if s == "us_ok":
            message_text = "美音下载完成！"
        else:
            message_text = "美音下载失败！"
        message_box = QMessageBox()
        message_box.setWindowTitle("下载结果")
        message_box.setText(message_text)
        message_box.setIcon(QMessageBox.Information)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()
    def combination(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        exe_path = d + "/TTSMaker/TTSMaker/TTSMaker.exe"
        try:
            subprocess.Popen(exe_path)
        except Exception as e:
            message_box = QMessageBox()
            message_box.setWindowTitle("警告")
            message_box.setText(f"无法运行TTSMaker.exe文件:{e}")
            message_box.setIcon(QMessageBox.Warning)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()
    def history_list(self):
        with open("history.json","r") as f:
            history_info = json.load(f)
            history_list = history_info["history"]
        for item in history_list:
            self.listWidget.addItem(item)
    def clear_cache(self):
        data = {"history":[]}
        with open("history.json","w") as f:
            json.dump(data,f)
        message_box = QMessageBox()
        message_box.setWindowTitle("信息")
        message_box.setText("已清除历史记录！")
        message_box.setIcon(QMessageBox.Information)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()
        self.history_list()
    def get_selected_items(self):
        selected_items = self.listWidget.selectedItems()  # 获取选中的项的列表
        for item in selected_items:
            path = item.text()
            path = path.split("/")
            path.pop(-1)
            path = "/".join(path)
            if os.path.isdir(path):  # 检查文件夹路径是否存在
                os.startfile(path)  # 使用默认文件管理器打开文件夹
            else:
                print("文件夹路径无效")