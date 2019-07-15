from scrapers import indeed as scraper
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from enum import Enum, unique
import os

@unique
class JobStatus(Enum):
    NEW = 'New'
    OPENED = 'Opened'
    OPENED_SIMILAR = 'Similar was opened'
    APPLIED = 'Applied'
    APPLIED_SIMILAR = 'Similar was Applied'
    
@unique
class JobStatusColors(Enum):
    NEW = '#ffffcc'
    OPENED = '#ff9478'
    OPENED_SIMILAR = '#f64747'
    APPLIED = '#4daf7c'
    APPLIED_SIMILAR = '#36d7b7'

class Ui_MainWindow(object):
    
    results_save_path = './data/job_results.pkl'
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 646)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.refresh_board_btn = QtWidgets.QPushButton(self.centralwidget)
        self.refresh_board_btn.setGeometry(QtCore.QRect(230, 540, 131, 23))
        self.refresh_board_btn.setAutoFillBackground(False)
        self.refresh_board_btn.setObjectName("refresh_board_btn")
        
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
                
        self.scrape_all_pages.setChecked(True)
        self.num_pages_to_scrape.setEnabled(False)
        self.scrape_all_pages.toggled.connect(self.toggle_page_field)
        
        self.num_pages_to_scrape.sliderMoved.connect(self.update_page_desc)
        self.job_table_widget.itemDoubleClicked.connect(self.open_job_link)
        
        # Adding Context Menu
        self.job_table_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.job_table_widget.customContextMenuRequested.connect(self.show_context_menu)
        
    def show_context_menu(self, position):
        right_clicked_item = self.job_table_widget.itemAt(position)
        if right_clicked_item.column() != 5:
            return(False)
        
        status_context_menu = QtWidgets.QMenu()
        to_applied_action = status_context_menu.addAction(JobStatus.APPLIED.value)
        to_opened_action = status_context_menu.addAction(JobStatus.OPENED.value)
        to_unopened_action = status_context_menu.addAction(JobStatus.NEW.value)
        status_context_menu.setTitle("Modify status")
        action = status_context_menu.exec_(self.job_table_widget.mapToGlobal(position))
        
        if action in [to_applied_action, to_opened_action, to_unopened_action]:
            self.change_status(right_clicked_item.row(), JobStatus[JobStatus(action.text()).name])
            
            
    
    def change_status(self, row, status = JobStatus):
        self.job_table_widget.setItem(row, 5, QtWidgets.QTableWidgetItem(status.value))
        self.color_row(row, QtGui.QColor(JobStatusColors[status.name].value))
        self.save_job_results()
        
                
        
        
    
    def color_row(self, row_index, color = QtGui.QColor):
        for col_index in range(self.job_table_widget.columnCount()):
            self.job_table_widget.item(row_index, col_index).setBackground(color)
    
    
    def refresh_status_colors(self):
        for i in range(self.job_table_widget.rowCount()):
            self.color_row(i, QtGui.QColor(JobStatusColors[JobStatus(self.job_table_widget.item(i,5).text()).name].value))
    
    
    def open_job_link(self, item):
        print("\nTable Double Clicked\n")
        if item.column() == 2:
#            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://www.indeed.com" + item.text()))
            self.job_table_widget.setItem(item.row(), 5, QtWidgets.QTableWidgetItem(JobStatus.OPENED.value))
            self.color_row(item.row(), QtGui.QColor(JobStatusColors.OPENED.value))
            self.save_job_results()
   
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Job Board"))
        self.refresh_board_btn.setText(_translate("MainWindow", "Refresh Board"))
        self.scrape_all_pages.setText(_translate("MainWindow", "Scrape all pages"))
        self.page_desc_label.setText(_translate("MainWindow", "Scrape all pages"))
    
    
    def refresh_job_board(self):
        self.refresh_board_btn.setEnabled(False)
        
        job_df = None
        if self.scrape_all_pages.isChecked():
            job_df = scraper.scrape_jobs()
            
        else:
            job_df = scraper.scrape_jobs(int(self.num_pages_to_scrape.value()))
        
        job_df['STATUS'] = [JobStatus.NEW.value for i in range(len(job_df.index))]
        
        # Loading saved results file and comparing to change statuses
        if(os.path.exists(self.results_save_path)):
            
            results_archive_df = pd.read_pickle(self.results_save_path)
            opened_results_df = results_archive_df[results_archive_df['STATUS'].isin([JobStatus.OPENED.value, JobStatus.APPLIED.value])]
            
    #        for job_index in range(len(job_df.index)):
    #            for open_index in range(len(opened_results_df.index)):
    #                if job_df.iloc[job_index]['JD'] == opened_results_df.iloc[open_index]['JD']:
    #                    job_df.at[job_index, 'STATUS'] = JobStatus.OPENED.value
    #                    break
            
            job_df = pd.merge(job_df, opened_results_df[['TITLE', 'COMPANY', 'STATUS']], how = 'left', on = ['COMPANY', 'TITLE'], suffixes = ('', '_Y'))
            job_df.loc[job_df['STATUS_Y'] == JobStatus.OPENED.value, 'STATUS'] = JobStatus.OPENED_SIMILAR.value
            job_df.loc[job_df['STATUS_Y'] == JobStatus.APPLIED.value, 'STATUS'] = JobStatus.APPLIED_SIMILAR.value
            job_df.drop('STATUS_Y', 1, inplace = True)

       
        # Loading the QTableWidget
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
        self.save_job_results()
        
    
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
        job_results_df.loc[job_results_df['STATUS'] == JobStatus.OPENED_SIMILAR.value, 'STATUS'] = JobStatus.OPENED.value
        job_results_df.to_pickle(self.results_save_path)
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