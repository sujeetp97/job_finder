from scrapers import indeed as scraper
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from enum import Enum, unique

@unique
class JobStatus(Enum):
    UNOPENED = 'UNOPENED'
    OPENED = 'OPENED'
    
@unique
class JobStatusColors(Enum):
    UNOPENED = '#ffffcc'
    OPENED = '#ff9478'

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
        self.save_board_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_board_btn.setGeometry(QtCore.QRect(360, 540, 141, 23))
        self.save_board_btn.setObjectName("savecancel_board_btn")
        
        self.job_table_widget = QtWidgets.QTableWidget(self.centralwidget)
        self.job_table_widget.setGeometry(QtCore.QRect(10, 0, 781, 531))
        self.job_table_widget.setObjectName("job_table_widget")
        self.job_table_widget.setColumnCount(0)
        self.job_table_widget.setRowCount(0)
        self.job_table_widget.setSortingEnabled(True)
        
   
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
        
        ### Code
        self.refresh_board_btn.clicked.connect(self.refresh_job_board)
        self.save_board_btn.clicked.connect(self.save_job_results)
        
        self.scrape_all_pages.setChecked(True)
        self.num_pages_to_scrape.setEnabled(False)
        self.scrape_all_pages.toggled.connect(self.toggle_page_field)
        
        self.num_pages_to_scrape.sliderMoved.connect(self.update_page_desc)
        self.job_table_widget.itemDoubleClicked.connect(self.open_job_link)
        
    
    def color_row(self, row_index, color = QtGui.QColor):
        for col_index in range(self.job_table_widget.columnCount()):
            self.job_table_widget.item(row_index, col_index).setBackground(color)
    
    
    def refresh_status_colors(self):
        for i in range(self.job_table_widget.rowCount()):
            self.color_row(i, QtGui.QColor(JobStatusColors[JobStatus(self.job_table_widget.item(i,5).text()).name].value))
    
    
    def open_job_link(self, item):
        print("\nTable Double Clicked\n")
        if item.column() == 2:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://www.indeed.com" + item.text()))
            self.job_table_widget.setItem(item.row(), 5, QtWidgets.QTableWidgetItem(JobStatus.OPENED.value))
            self.color_row(item.row(), QtGui.QColor(JobStatusColors.OPENED.value))
   
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Job Board"))
        self.refresh_board_btn.setText(_translate("MainWindow", "Refresh Board"))
        self.save_board_btn.setText(_translate("MainWindow", "Save Results"))
        self.scrape_all_pages.setText(_translate("MainWindow", "Scrape all pages"))
        self.page_desc_label.setText(_translate("MainWindow", "Scrape all pages"))
    
    
    def refresh_job_board(self):
        self.refresh_board_btn.setEnabled(False)
        
        job_df = None
        if self.scrape_all_pages.isChecked():
            job_df = scraper.scrape_jobs()
            
        else:
            job_df = scraper.scrape_jobs(int(self.num_pages_to_scrape.value()))
        
        job_df['STATUS'] = [JobStatus.UNOPENED.value for i in range(len(job_df.index))]
        
        row_count = len(job_df.index)
        col_count = len(job_df.columns)
        self.job_table_widget.setRowCount(row_count)
        self.job_table_widget.setColumnCount(col_count)
        
        col_names = job_df.columns
        for col_index in range(col_count):
            self.job_table_widget.setHorizontalHeaderItem(col_index, QtWidgets.QTableWidgetItem(col_names[col_index]))
        
        for row_index in range(row_count):
            for col_index in range(col_count):
                self.job_table_widget.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(job_df.ix[row_index, col_index])))
        self.refresh_status_colors()
        self.refresh_board_btn.setEnabled(True)

    
    def toggle_page_field(self):
        self.num_pages_to_scrape.setEnabled(not self.scrape_all_pages.isChecked())
        if self.scrape_all_pages.isChecked():
            self.page_desc_label.setText("Scrape all pages")
        else:
            self.update_page_desc()
    
    def update_page_desc(self):
        print("Moved")
        self.page_desc_label.setText("Scrape " + str(self.num_pages_to_scrape.value()) + " page/s")
    
 
    def save_job_results(self):
        print("Saving Results")
        job_results_list = {'TITLE' : [], 'COMPANY' : [], 'LINK' : [], 'JD' : [], 'RELEVANCE' : [], 'STATUS' : []}
        for row in range(self.job_table_widget.rowCount()):
            job_results_list['TITLE'].append(self.job_table_widget.item(row, 0).text())
            job_results_list['COMPANY'].append(self.job_table_widget.item(row, 1).text())
            job_results_list['LINK'].append(self.job_table_widget.item(row, 2).text())
            job_results_list['JD'].append(self.job_table_widget.item(row, 3).text())
            job_results_list['RELEVANCE'].append(int(self.job_table_widget.item(row, 4).text()))
            job_results_list['STATUS'].append(self.job_table_widget.item(row, 5).text())
                
        job_results_df = pd.DataFrame(job_results_list, index = range(len(job_results_list['TITLE'])))
        job_results_df.to_pickle("./data/job_results.pkl")
        print("Results Saved!")
         
    
if __name__ == "__main__":
    
#    app = QtWidgets.QApplication(sys.argv)
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())