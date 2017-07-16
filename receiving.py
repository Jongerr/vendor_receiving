
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox,\
     QFormLayout, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import Qt


class Receiving(QMainWindow):

    def __init__(self):
        super().__init__()

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
        self.setGeometry(300, 300, 1080, 640)
        self.setMinimumSize(1080, 640)
        self.show()


    def createTopLabels(self):
        
        self.horizontalLabels = QGroupBox('Vendor Receiving Entry')
        self.horizontalLabels.setAlignment(Qt.AlignHCenter)
        layout = QHBoxLayout()

        idLabel = QLabel('Clerk ID:[           ]')
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
        poLine.setMaximumWidth(windowWidth / 3)
        vendorLine = QLineEdit()
        vendorLine.setMaximumWidth(windowWidth / 3)
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
        pacSlipLine = QLineEdit()
        totUnitsLine = QLineEdit()
        totUnitsLine.setValidator(intValidator)

        psUnitsLabel = QLabel('PS &Units')
        psUnitsLine = QLineEdit()
        psUnitsLine.setValidator(intValidator)
        psUnitsLabel.setBuddy(psUnitsLine)
        totUnitsLabel = QLabel('Total <   0>')
        
        psHorizontalLayout = QHBoxLayout()
        psHorizontalLayout.addWidget(psUnitsLabel)
        psHorizontalLayout.addWidget(psUnitsLine)
        psHorizontalLayout.addWidget(totUnitsLabel)
        
        storeLocation = QLabel('Location < 22>')
        depLabel = QLabel('Department <D1>')
        
        locHorizontalLayout = QHBoxLayout()
        locHorizontalLayout.addWidget(storeLocation)
        locHorizontalLayout.addWidget(depLabel)
        
        coordNumLine = QLineEdit()
        coordNumLine.setValidator(intValidator)

        rightForm.addRow('&Bill of Landing ', bolLine)
        rightForm.addRow('Packing &Slip ', pacSlipLine)
        rightForm.addRow('&Total Units Received', totUnitsLine)
        rightForm.addRow(psHorizontalLayout)
        rightForm.addRow(locHorizontalLayout)
        rightForm.addRow('Receiving &Coordinator ', coordNumLine)

        self.inputLayout.addLayout(leftForm)
        self.inputLayout.addLayout(rightForm)


    def setupTable(self, qtable):

        #Make the 3rd and 6th columns read-only 
        columns = (2, 5)
        rows = qtable.rowCount()

        for column in columns:
            for row in range(rows):
                qtable.setRowHeight(row, 30)
                placeholderCell = QTableWidgetItem('###')
                placeholderCell.setFlags(placeholderCell.flags() ^ Qt.ItemIsEditable) 
                qtable.setItem(row, column, placeholderCell)
                
        
        headers = ['UPC', 'PLU', 'DESCRIPTION', 'UNITS RECEIVED', 'PS UNITS', 'VENDOR MODEL']
        qtable.setHorizontalHeaderLabels(headers)

        fontSize = 8
        font = qtable.horizontalHeader().font()
        font.setPointSize(fontSize)
        qtable.horizontalHeader().setFont(font)
        qtable.setFont(font)

        columnSizes = {headers[0]: 120, headers[1]: 85, headers[2]: 300, headers[3]: 140, headers[4]: 100, headers[5]: 250} 
        for i, column in enumerate(headers):
            qtable.setColumnWidth(i, columnSizes[column])
        
        qtable.setShowGrid(False)


    def createMainTable(self):

        self.mainTable = QTableWidget(50, 6)
        self.setupTable(self.mainTable)
        

    def resizeEvent(self, e):

        newSize = e.size()
        print(str(newSize))
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    receiver = Receiving()
    sys.exit(app.exec_())
