from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QApplication, QLineEdit, QCompleter
import json
import os
class MyCompleter(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCaseSensitivity(Qt.CaseInsensitive)
    def update(self, text):
        suggestions = get_suggestions(text)
        model = QStandardItemModel()
        for suggestion in suggestions:
            item = QStandardItem(suggestion)
            model.appendRow(item)
        self.setModel(model)
def get_suggestions(prefix):
    a = os.path.abspath('.')
    b = a.split("\\")
    c = tuple(b)
    d = '/'.join(c)
    list_json_path = d + "/list.json"
    with open(list_json_path, "r") as file:
        word_list = json.load(file)["list"]
        word_list.sort()
    return word_list