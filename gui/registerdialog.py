# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QApplication, QGridLayout, QMessageBox, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt, QCryptographicHash


class RegisterDialog(QDialog):
    def __init__(self, parent = None):
        super(RegisterDialog, self).__init__(parent)
        
        userLabel = QLabel("&User:")
        self.userLineEdit = QLineEdit()
        self.userLineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.userLineEdit.setPlaceholderText("input email")
        userLabel.setBuddy(self.userLineEdit)
        
        passwordLabel = QLabel("&Password:")
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit.setPlaceholderText("input password")
        passwordLabel.setBuddy(self.passwordLineEdit)
        
        confirmPasswordLabel = QLabel("&Confirm:")
        self.confirmPasswordLineEdit = QLineEdit()
        self.confirmPasswordLineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.confirmPasswordLineEdit.setEchoMode(QLineEdit.Password)
        self.confirmPasswordLineEdit.setPlaceholderText("confirm password")
        confirmPasswordLabel.setBuddy(self.confirmPasswordLineEdit)
        
        registerPushButton = QPushButton("&Register")
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(registerPushButton)
        
        layout = QGridLayout()
        layout.addWidget(userLabel, 0, 0)
        layout.addWidget(self.userLineEdit, 0, 1)
        layout.addWidget(passwordLabel, 1, 0)
        layout.addWidget(self.passwordLineEdit, 1, 1)
        layout.addWidget(confirmPasswordLabel, 2, 0)
        layout.addWidget(self.confirmPasswordLineEdit, 2, 1)
        spacerItem = QSpacerItem(20, 48, QSizePolicy.Minimum, QSizePolicy.Expanding)  
        layout.addItem(spacerItem) 
        layout.addLayout(buttonLayout, 3, 1)
        
        self.setLayout(layout)
        
        registerPushButton.clicked.connect(self.validate)
        
        #self.setWindowFlags(Qt.WindowMinimizeButtonHint)  
        #self.setFixedSize(200, 160)
        self.setWindowTitle("Register")
    
    def validate(self):
        if not self.userLineEdit.text():
            QMessageBox.warning(self, "Error", "Please Input user") 
        elif not self.passwordLineEdit.text() or not self.confirmPasswordLineEdit.text():
            QMessageBox.warning(self, "Error", "Please input password")
        elif self.passwordLineEdit.text() == self.confirmPasswordLineEdit.text():
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "The passwords are not the same")
            self.passwordLineEdit.clear()
            self.confirmPasswordLineEdit.clear()
    
    def getIdPw(self):
        return self.userLineEdit.text(), QCryptographicHash.hash(self.passwordLineEdit.text().encode("utf-8"), QCryptographicHash.Md5).toHex()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = RegisterDialog()
    dlg.show()
    app.exec_()
