# -*- coding:utf-8 -*-

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QSplitter, QListView, QWidget, QDockWidget, QAction, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings, QVariant, QByteArray, Qt, QDir

from gui import qrc_icon
from gui.logindialog import LoginDialog
from gui.orderdialog import OrderDialog

class MainWindow(QMainWindow):
    
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        
        findAction = self.createAction("&Find", "find", "find stock by code", slot = self.findStock)
        showAction = self.createAction("&Show", "show", "show all stock", slot = self.showStock)
        stockMenu = self.menuBar().addMenu("&Stock")
        self.addActions(stockMenu, findAction, showAction)
        stockToolbar = self.addToolBar("Stock")
        stockToolbar.setObjectName("StockToolbar")
        self.addActions(stockToolbar, findAction, showAction)
        
        createAction = self.createAction("&Create", "create", "create new order", slot = self.createOrder)
        historyAction = self.createAction("&History", "history", "show historical orders", slot = self.historicalOrder)
        orderMenu = self.menuBar().addMenu("&Order")
        self.addActions(orderMenu, createAction, historyAction)
        orderToolbar = self.addToolBar("Order")
        orderToolbar.setObjectName("OrderToolbar")
        self.addActions(orderToolbar, createAction, historyAction)
        
        
        
        twapAction = self.createAction("About TWAP", slot = self.aboutTWAP)
        vwapAction = self.createAction("About VWAP", slot = self.aboutVWAP)
        strategyMenu = self.menuBar().addMenu("S&trategy")
        self.addActions(strategyMenu, twapAction, vwapAction)
        
        versionAction = self.createAction("Version", "version", slot = self.version)
        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, versionAction)
        
        self.orderList = QListView()
        self.paintWidget = QWidget()
        self.stockList = QListView()
        
        informationSplitter = QSplitter(Qt.Vertical)
        informationSplitter.addWidget(self.paintWidget)
        informationSplitter.addWidget(self.orderList)
        
        logDockWidget = QDockWidget("Stock", self)
        logDockWidget.setObjectName("LogDockWidget")
        logDockWidget.setWidget(self.stockList)
        self.addDockWidget(Qt.LeftDockWidgetArea, logDockWidget)
        
        
        
        self.setCentralWidget(informationSplitter)
        
        
        settings = QSettings()
        self.restoreGeometry( settings.value("Geometry", type = QByteArray) )
        self.restoreState( settings.value("MainWindow/State", type = QByteArray) )
        
        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)
        self.status.showMessage("Ready", 5000)
        
    def createAction(self, text, icon = None, tip = None, shortcut = None, 
                     checkable = False, slot = None, signal = "triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" %icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            if signal == "triggered()":
                action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action
    def addActions(self, target, *actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
    
    def findStock(self):
        code, ok = QInputDialog.getText(self, "Find", "Stock Code:", QLineEdit.Normal, "000000")
        if ok and code:
            pass
    def showStock(self):
        pass
    
    def historicalOrder(self):
        pass
    def createOrder(self):
        dlg = OrderDialog(self)
        if dlg.exec_():
            order = dlg.getOrder()
    def version(self):
        pass        
    def aboutVWAP(self):
        pass
    def aboutTWAP(self):
        pass
        
        
        
        
    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue("Geometry", QVariant(self.saveGeometry()))
        settings.setValue("MainWindow/State", QVariant(self.saveState()))
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("AlgoTrading")
    app.setWindowIcon(QIcon(":/appicon.png"))
    
    logindlg = LoginDialog()
    if logindlg.exec_():
        mw = MainWindow()
        mw.show()
    app.exec_()
