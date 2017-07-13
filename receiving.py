
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox,\
     QFormLayout, QLineEdit
from PyQt5.QtGui import QIntValidator
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

        centralWidget.setLayout(mainLayout)

        self.setWindowTitle('Vendor Receiving')
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

        self.horizontalLabels.setLayout(layout)


    def createMainInputs(self):

        self.inputLayout = QHBoxLayout()
        leftForm = QFormLayout()
        rightForm = QFormLayout()

        intValidator = QIntValidator()

        poLine = QLineEdit()
        poLine.setValidator(intValidator)
        vendorLine = QLineEdit()
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
        psUnitsLine = QLineEdit()
        psUnitsLine.setValidator(intValidator)
        depLabel = QLabel('<D1>')
        coordNumLine = QLineEdit()
        coordNumLine.setValidator(intValidator)

        rightForm.addRow('Bill of Landing ', bolLine)
        rightForm.addRow('Packing Slip ', pacSlipLine)
        rightForm.addRow('Total Units ', totUnitsLine)
        rightForm.addRow('PS Units ', psUnitsLine)
        rightForm.addRow('Department ', depLabel)
        rightForm.addRow('Receiving Coordinator ', coordNumLine)

        self.inputLayout.addLayout(leftForm)
        self.inputLayout.addLayout(rightForm)

        


    def createMainTable(self):

        pass
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    receiver = Receiving()
    sys.exit(app.exec_())
