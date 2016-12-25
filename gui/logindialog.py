# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QCheckBox, QPushButton, QApplication, QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt, QCryptographicHash, QByteArray, QSettings, QVariant

from gui.registerdialog import RegisterDialog

class LoginDialog(QDialog):
    
    def __init__(self, parent = None):
        super(LoginDialog, self).__init__(parent)
        
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
        
        self.rememberCheckBox = QCheckBox("&remember the password")
        
        loginPushButton = QPushButton("&Login")
        registerPushButton = QPushButton("&Register")
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(loginPushButton)
        buttonLayout.addWidget(registerPushButton)
        
        layout = QGridLayout()
        layout.addWidget(userLabel, 0, 0)
        layout.addWidget(self.userLineEdit, 0, 1)
        layout.addWidget(passwordLabel, 1, 0)
        layout.addWidget(self.passwordLineEdit, 1, 1)
        layout.addWidget(self.rememberCheckBox, 2, 1)
        spacerItem = QSpacerItem(20, 48, QSizePolicy.Minimum, QSizePolicy.Expanding)  
        layout.addItem(spacerItem)  
        layout.addLayout(buttonLayout, 3, 0, 1, 3)
        
        self.setLayout(layout)
        
        loginPushButton.clicked.connect(self.login)
        registerPushButton.clicked.connect(self.register)
        
        settings = QSettings()
        self.rememberCheckBox.setChecked( settings.value("Checked", type = bool) )
        self.userLineEdit.setText(settings.value("User", type = str))
        if settings.value("Checked", type = bool):
            self.passwordLineEdit.setText(settings.value("Password", type = str))
        
        #self.setWindowFlags(Qt.WindowMinimizeButtonHint)  
        #self.setFixedSize(250, 160)
        self.setWindowTitle("Login")
        
    
    def login(self): 
        if not self.userLineEdit.text():
            QMessageBox.warning(self, "Error", "Please Input user")
            return
        if not self.passwordLineEdit.text():
            QMessageBox.warning(self, "Error", "Please input password")
            return
            
        user = self.userLineEdit.text()
        plainpw = self.passwordLineEdit.text()
        password = QCryptographicHash.hash(plainpw.encode("utf-8"), QCryptographicHash.Md5).toHex()
        """
        login operating...
        """
        if True:  
            settings = QSettings()            
            settings.setValue("User", QVariant(user))
            settings.setValue("Password", QVariant(plainpw))
            settings.setValue("Checked", QVariant(self.rememberCheckBox.isChecked()))
            QMessageBox.information(self, "Sucess", "Successful login")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to login")
            self.reject()
        
       
        
    def register(self):
        rdlg = RegisterDialog(self)
        if rdlg.exec_():
            user, password = rdlg.getIdPw()
            """
            register operating...
            """
            QMessageBox.information(self, "Sucess", "Successfully registered")
            
    
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = LoginDialog()
    dlg.show()
    app.exec_()
