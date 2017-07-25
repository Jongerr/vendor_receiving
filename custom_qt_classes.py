from PyQt5.QtWidgets import QLineEdit, QItemDelegate
from PyQt5.QtGui import QValidator, QIntValidator


#based on https://stackoverflow.com/questions/22708623/qtablewidget-only-numbers-permitted
class Delegate(QItemDelegate):

    def __init__(self):
        super().__init__()


    def createEditor(self, parent, option, index):

        lineEdit = QLineEdit(parent)
        lineEdit.setValidator(QIntValidator(lineEdit))
        return lineEdit


class NoEditValidator(QValidator):

    def __init__(self):
        super().__init__()


    def validate(self, input_string, position):
        return QValidator.Invalid
