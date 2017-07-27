from PyQt5.QtWidgets import QLineEdit, QStyledItemDelegate
from PyQt5.QtGui import QValidator, QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp


#based on https://stackoverflow.com/questions/22708623/qtablewidget-only-numbers-permitted
class Delegate(QStyledItemDelegate):

    def __init__(self):
        super().__init__()


    def createEditor(self, parent, option, index):

        lineEdit = QLineEdit(parent)
        regex = QRegExp(r"\d{0,12}")
        #lineEdit.setValidator(QIntValidator(0, 1000000000000, lineEdit))
        lineEdit.setValidator(QRegExpValidator(regex, lineEdit))
        return lineEdit


class NoEditValidator(QValidator):

    def __init__(self):
        super().__init__()


    def validate(self, input_string, position):
        return QValidator.Invalid
