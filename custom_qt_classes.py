from passlib.hash import pbkdf2_sha256 as pbk
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QValidator, QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class Login(QDialog):

    def __init__(self):
        super().__init__()

        self.initDB()
        self.initUI()


    def initUI(self):
        self.usernameLine = QLineEdit('Username')
        self.passwordLine = QLineEdit('Password')
        
        loginButton = QPushButton('Login')
        loginButton.clicked.connect(self.checkCredentials)

        loginBox = QGroupBox('Login Form', self)
        loginLayout = QVBoxLayout()
        loginLayout.addWidget(self.usernameLine)
        loginLayout.addWidget(self.passwordLine)
        loginLayout.addWidget(loginButton)

        loginBox.setLayout(loginLayout)

        self.setGeometry(300, 300, 200, 150)
        self.show()


    def initDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('C:\\receiving_project\\vendor_receiving\\inventory.db')
        if not self.db.open():
            print('Database could not be opened.')
            print(QSqlDatabase.lastError().text())
            self.close()
        self.query = QSqlQuery()


    def checkCredentials(self, checked):
        if not self.query.exec_("select * from employee where id = {}".format(self.usernameLine.text())):
            self.usernameLine.setText('')
            self.passwordLine.setText('')
            QMessageBox.warning(self, 'Invalid Credentials', 'Coordinator number or password were incorrect.')
            print(self.query.lastError().text())
        elif not self.query.next():
            self.usernameLine.setText('')
            self.passwordLine.setText('')
            QMessageBox.warning(self, 'Invalid Credentials', 'Coordinator number or password were incorrect.')
        else:
            pass_hash = self.query.value(4)
            if pbk.verify(self.passwordLine.text(), pass_hash):
                self.username = str(self.query.value(0))
                self.password = self.passwordLine.text()
                self.fullname = (self.query.value(1), self.query.value(2))
                self.accept()
            else:
                self.usernameLine.setText('')
                self.passwordLine.setText('')
                QMessageBox.warning(self, 'Invalid Credentials', 'Coordinator number or password were incorrect.')


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
