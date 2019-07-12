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
    UNOPENED = 'black'
    OPENED = 'blue'

class PandasModel(QtCore.QAbstractTableModel): 
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
#        elif role == QtCore.Qt.BackgroundRole:
#            if index.column() == 5:
#                if index.row() == JobStatus.OPENED.value:
#                    return QtGui.QBrush(QtCore.Qt.green)
#                elif index.row() == JobStatus.UNOPENED.value:
#                    return QtGui.QBrush(QtCore.Qt.red)
            
        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))
    
    def get_data(self, row, column, value_type = 'QVariant'):
        if value_type == 'QVariant' :
            return QtCore.QVariant(str(self._df.ix[row, column]))
        elif value_type == 'str':
            return str(self._df.ix[row, column])
        
    
    
    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True
    
           
        
    
    def set_data(self, row, column, value):
        row = self._df.index[row]
        col = self._df.columns[column]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        
        start_of_row = self.index(row, 0)
        end_of_row = self.index(row, self.columnCount())
        self.dataChanged.emit(start_of_row, end_of_row)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
    


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
        
        ### Code
        self.refresh_board_btn.clicked.connect(self.refresh_job_board)
        self.scrape_all_pages.setChecked(True)
        self.num_pages_to_scrape.setEnabled(False)
        self.scrape_all_pages.toggled.connect(self.toggle_page_field)
        
        self.num_pages_to_scrape.sliderMoved.connect(self.update_page_desc)
        
        self.job_table_view.setSelectionMode(1)
        self.job_table_view.setSelectionBehavior(1)
#        self.job_table_view.horizontalHeader().setStretchLastSection(True)
        
        self.job_table_view.doubleClicked.connect(self.open_job_link)    
        
    def open_job_link(self, model_index):
        print("\nTable Double Clicked\n")
        
        print(model_index.row())
        print(model_index.column())
        print(model_index.data())
        if model_index.column() == 2:
#            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://www.indeed.com" + model_index.data()))
            self.job_table_view.model().set_data(model_index.row(), 5, JobStatus.OPENED.value)
            

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Job Board"))
        self.refresh_board_btn.setText(_translate("MainWindow", "Refresh Board"))
        self.savecancel_board_btn.setText(_translate("MainWindow", "Save and Cancel"))
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
        job_table_model = PandasModel(job_df)
        
        self.job_table_view.setModel(job_table_model)
        self.refresh_board_btn.setEnabled(True)
        self.job_table_view.resizeColumnsToContents
    
    
    def toggle_page_field(self):
        self.num_pages_to_scrape.setEnabled(not self.scrape_all_pages.isChecked())
        if self.scrape_all_pages.isChecked():
            self.page_desc_label.setText("Scrape all pages")
        else:
            self.update_page_desc()
    
    def update_page_desc(self):
        print("Moved")
        self.page_desc_label.setText("Scrape " + str(self.num_pages_to_scrape.value()) + " page/s")
    
    
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