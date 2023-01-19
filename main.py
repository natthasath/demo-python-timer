import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QIntValidator)
from PySide2.QtWidgets import *
from datetime import datetime, timedelta
import pytimeparse
import webbrowser

from ui_main import Ui_MainWindow
from ui_styles import Style
from ui_functions import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('RENDER TIME CALCULATOR')
        UIFunctions.labelTitle(self, 'RENDER TIME CALCULATOR')
        UIFunctions.labelDescription(self, 'Calculate a rendering time estimate')
        UIFunctions.removeTitleBar(True)
        self.resize(500, 800)
        self.setMinimumSize(QSize(500, 800))
        UIFunctions.enableMaximumSize(self, 500, 800)
        def moveWindow(event):
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)

            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        def dobleClickMaximizeRestore(event):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        UIFunctions.uiDefinitions(self)
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 240, True))
        self.ui.stackedWidget.setMinimumWidth(400)
        UIFunctions.addNewMenu(self, "Render Time Calculator", "btn_home", "url(:/16x16/icons/16x16/cil-av-timer.png)", True)
        UIFunctions.addNewMenu(self, "About", "btn_settings", "url(:/16x16/icons/16x16/cil-options.png)", False)
        UIFunctions.selectStandardMenu(self, "btn_home")
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        self.ui.label_user_icon.hide()
        self.ui.tableWidget_renders.hide()
        self.ui.label_current_render.hide()
        self.ui.frame_div_table_widget.setMaximumSize(400, 50)
        self.ui.tableWidget_renders.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget_renders.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        self.ui.tableWidget_renders.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        self.ui.tableWidget_renders.setColumnWidth(0, QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget_renders.setColumnWidth(1, 120)
        self.ui.tableWidget_renders.setColumnWidth(2, 50)
        delegate = AlignDelegate(self.ui.tableWidget_renders)
        self.ui.tableWidget_renders.setItemDelegateForColumn(1, delegate)
        self.ui.tableWidget_renders.setItemDelegateForColumn(2, delegate)
        self.ui.pushButton_add_render.clicked.connect(lambda: Functions.addTableRow(self))
        self.onlyInt = QIntValidator()
        self.ui.lineEdit_hours.setValidator(self.onlyInt)
        self.ui.lineEdit_minutes.setValidator(self.onlyInt)
        self.ui.lineEdit_seconds.setValidator(self.onlyInt)
        self.ui.lineEdit_frames.setValidator(self.onlyInt)
        self.ui.lineEdit_machines.setValidator(self.onlyInt)
        Functions.calculateTime(self)
        self.timer = QtCore.QTimer(self)
        self.timer.start(500)
        self.timer.timeout.connect(lambda: Functions.calculateTime(self))
        self.ui.btn_artstation.clicked.connect(lambda: webbrowser.open('https://www.artstation.com/vfxonfire'))
        self.ui.btn_gumroad.clicked.connect(lambda: webbrowser.open('https://gumroad.com/blender_addons'))
        self.show()

    def deleteClicked(self):
        button = self.sender()
        table = self.ui.tableWidget_renders
        count = table.rowCount()

        if button:
            row = self.ui.tableWidget_renders.indexAt(button.pos()).row()
            self.ui.tableWidget_renders.removeRow(row)

        if count == 1:
            Functions.toggleTable(self)
            QtCore.QTimer.singleShot(600, lambda: self.ui.tableWidget_renders.hide())
            QtCore.QTimer.singleShot(600, lambda: self.ui.label_current_render.hide())
    
    def Button(self):

        btnWidget = self.sender()

        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            UIFunctions.labelPage(self, "Home")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_settings":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_info)
            UIFunctions.resetStyle(self, "btn_settings")
            UIFunctions.labelPage(self, "About")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

    def eventFilter(self, obj, event):
        pass

    def keyReleaseEvent(self, event):
        pass

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def keyPressEvent(self, event):
        pass

    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('./font/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('./font/segoeuib.ttf')
    QtGui.QFontDatabase.addApplicationFont('./font/Roboto-Regular.ttf')
    QtGui.QFontDatabase.addApplicationFont('./font/Roboto-Thin.ttf')
    window = MainWindow()
    sys.exit(app.exec_())