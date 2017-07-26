import json
import sys
from custom_qt_classes import Delegate, NoEditValidator
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


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


class Receiving(QMainWindow):

    def __init__(self, username, password):
        super().__init__()
        
        self.username = username
        self.password = password
        self.po_dict = {}
        self.initDB()
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


    def initDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('C:\\receiving_project\\vendor_receiving\\inventory.db')
        if not self.db.open():
            print('Database could not be opened.')
            print(QSqlDatabase.lastError().text())
            self.close()
        self.query = QSqlQuery()


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

        #Left Side Inputs
        self.poLine = QLineEdit()
        self.poLine.setValidator(intValidator)
        self.poLine.setMaximumWidth(windowWidth / 6)
        self.poLine.editingFinished.connect(self.lookupPO)
        self.vendorLine = QLineEdit()
        self.vendorLine.setMaximumWidth(windowWidth / 8)
        self.vendorNameLabel = QLabel('<Example Vendor Name>')
        addrLabel = QLabel('<Example Address>')
        ctstLabel = QLabel('<Example City/State>')
        zipLabel = QLabel('<Example Zip Code>')

        leftForm.addRow('&P.O.# ', self.poLine)
        leftForm.addRow('Vendor ', self.vendorLine)
        leftForm.addRow('Name ', self.vendorNameLabel)
        leftForm.addRow('Address ', addrLabel)
        leftForm.addRow('City, St ', ctstLabel)
        leftForm.addRow('Zip ', zipLabel)

        #Right Side Inputs
        self.bolLine = QLineEdit()
        self.bolLine.setMaximumWidth(windowWidth / 4)
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
        self.depLabel = QLabel('Department <  >')
        
        locHorizontalLayout = QHBoxLayout()
        locHorizontalLayout.setSpacing(3)
        locHorizontalLayout.addWidget(storeLocation)
        locHorizontalLayout.addWidget(self.depLabel)
        locHorizontalLayout.addSpacing(180)
        
        self.coordNumLine = QLineEdit()
        self.coordNumLine.setValidator(intValidator)
        self.coordNumLine.setMaximumWidth(windowWidth / 8)
        self.coordNumLine.editingFinished.connect(self.verifyCoordNum)

        rightForm.addRow('&Bill of Landing ', self.bolLine)
        rightForm.addRow('Packing &Slip ', pacSlipLine)
        rightForm.addRow('&Total Units Received', totUnitsLine)
        rightForm.addRow(psHorizontalLayout)
        rightForm.addRow(locHorizontalLayout)
        rightForm.addRow('Receiving &Coordinator ', self.coordNumLine)

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
        self.mainTable.cellChanged.connect(self.cellChangeSlot)


    def lookupPO(self):          
        po_num = self.poLine.text()
        if not self.query.exec_("select * from purchase_order where po = {}".format(po_num)):
            print(self.query.lastError().text())
            return False
        elif not self.query.next():
            self.poLine.setText('')
            QMessageBox.warning(self, 'PO not found', 'Could not find PO# {}.'.format(po_num))
            return False
        else:
            po = self.query.value(0)
            vendor = self.query.value(1)
            department = self.query.value(2)
            items = self.query.value(3)
            items = json.loads(items)
            self.po_dict[po] = {'vendor': vendor, 'department': department, 'items': items}
            self.vendorLine.setText(vendor)
            self.vendorLine.setReadOnly(True)
            self.vendorNameLabel.setText('<{}>'.format(vendor))
            self.depLabel.setText('<D{}>'.format(department))
            self.bolLine.setFocus()
            return True
            

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


    def verifyCoordNum(self):
        coord = self.coordNumLine.text()
        if coord == self.username:
            QMessageBox.warning(self, 'Invalid Coordinator Number', 'Cannot receive your own scans.')
            return
        if not self.query.exec_("select id from employee where id = {}".format(coord)):
            print(self.query.lastError().text())
        elif not self.query.next():
            self.coordNumLine.setText('')
            QMessageBox.warning(self, 'Invalid Coordinator Number', 'Coordinator does not have rights to this program.')
        else:
            self.coordNumLine.setReadOnly(True)
            self.mainTable.setFocus()


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
