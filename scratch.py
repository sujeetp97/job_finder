# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 11:47:09 2019

@author: sujit
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
 
qtCreatorFile = "C:/Users/sujit/OneDrive/Documents/Work/Job Finder/ui.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow
        self.ui.setupUi(self, )
        
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())