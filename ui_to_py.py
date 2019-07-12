# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\sujit\OneDrive\Documents\Work\Job Finder\ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 646)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.refresh_board_btn = QtWidgets.QPushButton(self.centralwidget)
        self.refresh_board_btn.setGeometry(QtCore.QRect(230, 540, 131, 23))
        self.refresh_board_btn.setAutoFillBackground(False)
        self.refresh_board_btn.setObjectName("refresh_board_btn")
        self.savecancel_board_btn = QtWidgets.QPushButton(self.centralwidget)
        self.savecancel_board_btn.setGeometry(QtCore.QRect(360, 540, 141, 23))
        self.savecancel_board_btn.setObjectName("savecancel_board_btn")
        self.job_table_view = QtWidgets.QTableView(self.centralwidget)
        self.job_table_view.setGeometry(QtCore.QRect(10, 0, 781, 531))
        self.job_table_view.setSortingEnabled(True)
        self.job_table_view.setObjectName("job_table_view")
        self.scrape_all_pages = QtWidgets.QCheckBox(self.centralwidget)
        self.scrape_all_pages.setGeometry(QtCore.QRect(10, 540, 121, 17))
        self.scrape_all_pages.setObjectName("scrape_all_pages")
        self.num_pages_to_scrape = QtWidgets.QSlider(self.centralwidget)
        self.num_pages_to_scrape.setGeometry(QtCore.QRect(10, 560, 160, 22))
        self.num_pages_to_scrape.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.num_pages_to_scrape.setMinimum(1)
        self.num_pages_to_scrape.setMaximum(100)
        self.num_pages_to_scrape.setPageStep(5)
        self.num_pages_to_scrape.setOrientation(QtCore.Qt.Horizontal)
        self.num_pages_to_scrape.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.num_pages_to_scrape.setTickInterval(10)
        self.num_pages_to_scrape.setObjectName("num_pages_to_scrape")
        self.page_desc_label = QtWidgets.QLabel(self.centralwidget)
        self.page_desc_label.setGeometry(QtCore.QRect(10, 580, 211, 16))
        self.page_desc_label.setObjectName("page_desc_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Job Board"))
        self.refresh_board_btn.setText(_translate("MainWindow", "Refresh Board"))
        self.savecancel_board_btn.setText(_translate("MainWindow", "Save and Cancel"))
        self.scrape_all_pages.setText(_translate("MainWindow", "Scrape all pages"))
        self.page_desc_label.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

