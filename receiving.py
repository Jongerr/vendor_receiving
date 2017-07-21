
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox,\
     QFormLayout, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QPushButton, QLayout, QItemDelegate
     
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import Qt


class Login(QDialog):

    def __init__(self):
        super().__init__()
        
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


    def checkCredentials(self, checked):

        self.username = self.usernameLine.text()
        self.password = self.passwordLine.text()

        if self.username == 'test' and self.password == 'test':
            self.accept()

        else:
            QMessageBox.warning(self, 'Login', 'Login Failed')

#based on https://stackoverflow.com/questions/22708623/qtablewidget-only-numbers-permitted
class Delegate(QItemDelegate):

    def __init__(self):
        super().__init__()


    def createEditor(self, parent, option, index):

        lineEdit = QLineEdit(parent)
        lineEdit.setValidator(QIntValidator(lineEdit))
        return lineEdit


class Receiving(QMainWindow):

    def __init__(self, username, password):
        super().__init__()
        
        self.username = username
        self.password = password
        self.initUI()
        

    def initUI(self):

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.createTopLabels()
        self.createMainInputs()
        self.createMainTable()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.horizontalLabels)
        mainLayout.addLayout(self.inputLayout)
        mainLayout.addWidget(self.mainTable)

        centralWidget.setLayout(mainLayout)

        self.setWindowTitle('Vendor Receiving')
        self.setGeometry(300, 300, 800, 585)
        self.setMinimumSize(800, 585)


    def setUserPass(self, username, password):

        self.username = username
        self.password = password


    def createTopLabels(self):
        
        self.horizontalLabels = QGroupBox('Vendor Receiving Entry')
        self.horizontalLabels.setAlignment(Qt.AlignHCenter)
        layout = QHBoxLayout()

        idLabel = QLabel('Clerk ID:[{}]'.format(self.username))
        passLabel = QLabel('Password:[********* ]')
        nameLabel = QLabel('Name: <Michie, Jon T.   >')

        layout.addWidget(idLabel)
        layout.addWidget(passLabel)
        layout.addWidget(nameLabel)

        layout.setAlignment(idLabel, Qt.AlignHCenter)
        layout.setAlignment(passLabel, Qt.AlignHCenter)
        layout.setAlignment(nameLabel, Qt.AlignHCenter)

        self.horizontalLabels.setLayout(layout)


    def createMainInputs(self):

        self.inputLayout = QHBoxLayout()
        leftForm = QFormLayout()
        rightForm = QFormLayout()

        intValidator = QIntValidator()
        windowWidth = self.width()

        poLine = QLineEdit()
        poLine.setValidator(intValidator)
        poLine.setMaximumWidth(windowWidth / 6)
        vendorLine = QLineEdit()
        vendorLine.setMaximumWidth(windowWidth / 8)
        vendorNameLabel = QLabel('<Example Vendor Name>')
        addrLabel = QLabel('<Example Address>')
        ctstLabel = QLabel('<Example City/State>')
        zipLabel = QLabel('<Example Zip Code>')

        leftForm.addRow('&P.O.# ', poLine)
        leftForm.addRow('Vendor ', vendorLine)
        leftForm.addRow('Name ', vendorNameLabel)
        leftForm.addRow('Address ', addrLabel)
        leftForm.addRow('City, St ', ctstLabel)
        leftForm.addRow('Zip ', zipLabel)

        bolLine = QLineEdit()
        bolLine.setMaximumWidth(windowWidth / 4)
        pacSlipLine = QLineEdit()
        pacSlipLine.setMaximumWidth(windowWidth / 4)
        totUnitsLine = QLineEdit()
        totUnitsLine.setValidator(intValidator)
        totUnitsLine.setMaximumWidth(windowWidth / 8)

        psUnitsLabel = QLabel('PS &Units')
        psUnitsLine = QLineEdit()
        psUnitsLine.setValidator(intValidator)
        psUnitsLine.setMaximumWidth(windowWidth / 8)
        psUnitsLabel.setBuddy(psUnitsLine)
        self.totUnitsLabel = QLabel('Total <   0>')
        
        psHorizontalLayout = QHBoxLayout()
        #QLayout.setAlignment(psHorizontalLayout, Qt.AlignJustify)
        psHorizontalLayout.addWidget(psUnitsLabel)
        psHorizontalLayout.addWidget(psUnitsLine)
        psHorizontalLayout.addWidget(self.totUnitsLabel)
        ulabel = psHorizontalLayout.setAlignment(psUnitsLabel, Qt.AlignLeft)
        uline = psHorizontalLayout.setAlignment(psUnitsLine, Qt.AlignLeft)
        totulabel = psHorizontalLayout.setAlignment(self.totUnitsLabel, Qt.AlignLeft)
        psHorizontalLayout.addSpacing(180)
        
        storeLocation = QLabel('Location < 22>')
        depLabel = QLabel('Department <D1>')
        
        locHorizontalLayout = QHBoxLayout()
        locHorizontalLayout.setSpacing(3)
        locHorizontalLayout.addWidget(storeLocation)
        locHorizontalLayout.addWidget(depLabel)
        locHorizontalLayout.addSpacing(180)
        
        coordNumLine = QLineEdit()
        coordNumLine.setValidator(intValidator)
        coordNumLine.setMaximumWidth(windowWidth / 8)

        rightForm.addRow('&Bill of Landing ', bolLine)
        rightForm.addRow('Packing &Slip ', pacSlipLine)
        rightForm.addRow('&Total Units Received', totUnitsLine)
        rightForm.addRow(psHorizontalLayout)
        rightForm.addRow(locHorizontalLayout)
        rightForm.addRow('Receiving &Coordinator ', coordNumLine)

        self.inputLayout.addLayout(leftForm)
        self.inputLayout.addLayout(rightForm)


    def createMainTable(self):

        self.mainTable = QTableWidget(50, 6)
        self.mainTable.setItemDelegate(Delegate())

        #Make the 3rd and 6th columns read-only 
        columns = (2, 5)
        rows = self.mainTable.rowCount()

        for column in columns:
            for row in range(rows):
                self.mainTable.setRowHeight(row, 30)
                placeholderCell = QTableWidgetItem('###')
                placeholderCell.setFlags(placeholderCell.flags() ^ Qt.ItemIsEditable) 
                self.mainTable.setItem(row, column, placeholderCell)
                
        #Setting table headers
        headers = ['UPC', 'PLU', 'DESCRIPTION', 'UNITS', 'PS UNITS', 'VENDOR MODEL']
        self.mainTable.setHorizontalHeaderLabels(headers)

        #Settting font size
        fontSize = 8
        font = self.mainTable.horizontalHeader().font()
        font.setPointSize(fontSize)
        self.mainTable.horizontalHeader().setFont(font)
        self.mainTable.setFont(font)

        #Setting column widths
        columnSizes = {headers[0]: 120, headers[1]: 85, headers[2]: 200, headers[3]: 70, headers[4]: 70, headers[5]: 175} 
        for i, column in enumerate(headers):
            self.mainTable.setColumnWidth(i, columnSizes[column])
        
        self.mainTable.setShowGrid(False)

        #Making connections
        self.mainTable.cellChanged.connect(self.cellChangeSlot)


    def cellChangeSlot(self, row, column):

        if column == 0:
            self.updateModelInfo(row, column)
            
        elif column == 3:
            self.updateTotalUnits()
            
        elif column == 4:
            self.updateTotalPS()

        else:
            pass


    def updateModelInfo(self, row, column):

        upcNum = int(self.mainTable.item(row, column).text())

        if upcNum == 123456:

            cellItem = QTableWidgetItem('Example Model')
            cellItem.setFlags(cellItem.flags() ^ Qt.ItemIsEditable)
            self.mainTable.setItem(row, 2, cellItem)

        else:

            cellItem = QTableWidgetItem('')
            cellItem.setFlags(cellItem.flags() ^ Qt.ItemIsEditable)
            self.mainTable.setItem(row, 2, cellItem)


    def updateTotalUnits(self):

        total = 0
        
        rows = self.mainTable.rowCount()
        for row in range(rows):
            cell = self.mainTable.item(row, 3)

            if cell:
                cellVal = int(cell.text())
                total = total + cellVal

        self.totUnitsLabel.setText('Total <{}>'.format(total))


    def updateTotalPS(self):

        pass


    def resizeEvent(self, e):

        size = e.size()
        print(size)
    
       

if __name__ == '__main__':

    app = QApplication(sys.argv)
    login = Login()
    #receiver = Receiving()
    if(login.exec_() == QDialog.Accepted):
        receiver = Receiving(login.username, login.password)
        receiver.show()
        
    sys.exit(app.exec_())
