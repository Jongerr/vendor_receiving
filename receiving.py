import json
import sys
from custom_qt_classes import Delegate, Login
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class Receiving(QMainWindow):

    def __init__(self, username, password, fullname):
        super().__init__()
        
        self.username = username
        self.password = password
        self.fullname = fullname
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
        passLabel = QLabel('Password:[{} ]'.format('*' * len(self.password)))
        nameLabel = QLabel('Name: <{}, {} >'.format(self.fullname[1], self.fullname[0]))

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
        self.mainTable.delegate = Delegate()
        self.mainTable.setItemDelegateForColumn(0, self.mainTable.delegate)
        self.mainTable.setItemDelegateForColumn(1, self.mainTable.delegate)
        self.mainTable.listen_to_signals = True

        columns = (2, 3, 4, 5)
        rows = self.mainTable.rowCount()
        for column in columns:
            for row in range(rows):
                self.mainTable.setRowHeight(row, 30)
                placeholderCell = QTableWidgetItem('')
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
        if not self.mainTable.listen_to_signals:
            return
        if column == 0 or column == 1:
            self.updateModelInfo(row, column)   
        elif column == 3:
            self.updateTotalUnits()            
        else:
            pass


    def lookupItemByUPC(self, upc):
        if not self.query.exec_("select * from items where upc = {}".format(upc)):
            print(self.query.lastError().text())
            return ()
        elif not self.query.next():
            return ()
        else:
            plu_num = self.query.value(0)
            upc = self.query.value(1)
            model = self.query.value(2)
            department = self.query.value(3)
            return (upc, plu_num, model, department)


    def lookupItemByPLU(self, plu):
        if not self.query.exec_("select * from items where plu = {}".format(plu)):
            print(self.query.lastError().text())
            return ()
        elif not self.query.next():
            return ()
        else:
            plu_num = self.query.value(0)
            upc = self.query.value(1)
            model = self.query.value(2)
            department = self.query.value(3)
            return (upc, plu_num, model, department)
        

    def itemInCurrentPO(self, plu):
        if not self.po_dict:
            return False
        po_num = int(self.poLine.text())
        items = list(self.po_dict[po_num]['items'].keys())
        if str(plu) in items:
            return True
        else:
            return False


    def checkDuplicateItem(self, plu, exempt_row):
        rows = self.mainTable.rowCount()
        duplicate_row = None
        for row in range(rows):
            if row == exempt_row:
                continue
            current_cell = self.mainTable.item(row, 1)
            if not current_cell or not current_cell.text():
                continue
            if int(current_cell.text()) == plu:
                duplicate_row = row
                break
        return duplicate_row
        

    def updateItemRow(self, row, item_info, plu_entered=True):
        if plu_entered:
            initial_val = 0
            upc = QTableWidgetItem(item_info[0])
            upc.setFlags(upc.flags() ^ Qt.ItemIsEditable)
            self.mainTable.setItem(row, 0, upc)
            plu = self.mainTable.item(row, 1)
            plu.setFlags(plu.flags() ^ Qt.ItemIsEditable)
        else:
            initial_val = 1
            plu = QTableWidgetItem(item_info[1])
            plu.setFlags(plu.flags() ^ Qt.ItemIsEditable)
            self.mainTable.setItem(row, 1, plu)
            upc = self.mainTable.item(row, 0)
            upc.setFlags(upc.flags() ^ Qt.ItemIsEditable)
            
        description = self.mainTable.item(row, 2)
        description.setText('Example Description')
        
        physical_units = self.mainTable.item(row, 3)
        physical_units.setFlags(physical_units.flags() | Qt.ItemIsEditable)
        physical_units.setText(str(initial_val))
        
        packingslip_units = self.mainTable.item(row, 4)
        packingslip_units.setFlags(packingslip_units.flags() | Qt.ItemIsEditable)
        packingslip_units.setText(str(initial_val))
        
        model = self.mainTable.item(row, 5)
        model.setText(item_info[2])
        

    def updateModelInfo(self, row, column):
        self.mainTable.listen_to_signals = False
        if not self.mainTable.item(row, column).text():
            self.mainTable.listen_to_signals = True
            return
        
        if column == 0:
            upc = int(self.mainTable.item(row, column).text())
            item_info = self.lookupItemByUPC(upc)
            plu_entered = False
        else:
            print(self.mainTable.item(row, column).text())
            plu = int(self.mainTable.item(row, column).text())
            item_info = self.lookupItemByPLU(plu)
            plu_entered = True

        if not item_info:
            QMessageBox().warning(self, 'Item not found', 'Could not find given item.')
            self.mainTable.item(row, 0) and self.mainTable.item(row, 0).setText('')
            self.mainTable.item(row, 1) and self.mainTable.item(row, 1).setText('')
            self.mainTable.listen_to_signals = True
            return

        duplicate_row = self.checkDuplicateItem(item_info[1], row)
        if duplicate_row != None:
            self.mainTable.item(row, column).setText('')
            print(duplicate_row)
            physical_units = int(self.mainTable.item(duplicate_row, 3).text())
            physical_units += 1
            self.mainTable.item(duplicate_row, 3).setText(str(physical_units))
            packingslip_units = int(self.mainTable.item(duplicate_row, 4).text())
            packingslip_units += 1
            self.mainTable.item(duplicate_row, 4).setText(str(packingslip_units))
        elif self.po_dict and self.itemInCurrentPO(item_info[1]):
            self.updateItemRow(row, item_info, plu_entered)
            print('Item in PO, updating....')
        elif self.po_dict and not self.itemInCurrentPO(item_info[1]):
            print('Item not in PO.')
            QMessageBox().warning(self, 'Item not on PO', 'Given item does not belong on PO.')
            self.mainTable.item(row, 0) and self.mainTable.item(row, 0).setText('')
            self.mainTable.item(row, 1) and self.mainTable.item(row, 1).setText('')
        elif not self.po_dict:
            print('No PO, updating row...')
            self.updateItemRow(row, item_info, plu_entered)

        self.mainTable.listen_to_signals = True


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


    def getTotalPSUnits(self):
        total = 0       
        rows = self.mainTable.rowCount()
        for row in range(rows):
            cell = self.mainTable.item(row, 4)
            if cell:
                cellVal = int(cell.text())
                total = total + cellVal
        self.totUnitsLabel.setText('Total <{}>'.format(total))


    def resizeEvent(self, e):
        size = e.size()
        print(size)
    
       

if __name__ == '__main__':

    app = QApplication(sys.argv)
    login = Login()
    if(login.exec_() == QDialog.Accepted):
        receiver = Receiving(login.username, login.password, login.fullname)
        receiver.show()
        
    sys.exit(app.exec_())
