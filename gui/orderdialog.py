# -*-coding:utf-8 -*-

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QApplication, QGridLayout, QHBoxLayout, QComboBox, QSpinBox
from PyQt5.QtCore import Qt

class OrderDialog(QDialog):
    def __init__(self, parent = None):
        super(OrderDialog, self).__init__(parent)
        
        codeLabel = QLabel("&Stock Code:")
        self.codeLineEdit = QLineEdit()
        self.codeLineEdit.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.codeLineEdit.setPlaceholderText("input stock code")
        codeLabel.setBuddy(self.codeLineEdit)
        
        strategyLabel = QLabel("&Strategy:")
        self.strategyComboBox = QComboBox()
        self.strategyComboBox.addItems(["TWAP", "VWAP"])
        strategyLabel.setBuddy(self.strategyComboBox)
        
        volumeLabel = QLabel("&Volume:")
        self.volumeSpinBox = QSpinBox()
        self.volumeSpinBox.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.volumeSpinBox.setRange(1, 1000000)
        self.volumeSpinBox.setValue(10000)
        volumeLabel.setBuddy(self.volumeSpinBox)
        
        okButton = QPushButton("OK")
        okButton.clicked.connect(self.accept)
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.reject)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(cancelButton)
        buttonLayout.addWidget(okButton)
        
        layout = QGridLayout()
        layout.addWidget(codeLabel, 0, 0)
        layout.addWidget(self.codeLineEdit, 0, 1)
        layout.addWidget(strategyLabel, 1, 0)
        layout.addWidget(self.strategyComboBox, 1, 1)
        layout.addWidget(volumeLabel, 2, 0)
        layout.addWidget(self.volumeSpinBox, 2, 1)
        layout.addLayout(buttonLayout, 3, 1)
        
        self.setLayout(layout)
        
        self.setWindowTitle("Create order")
    
    def getOrder(self):
        return (self.codeLineEdit.text(), self.strategyComboBox.currentText(), self.volumeSpinBox.value())

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = OrderDialog()
    dlg.show()
    app.exec_() 
        
        
        
        
        
        
        
        
