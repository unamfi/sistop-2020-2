#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 22:29:52 2020

@author: joaquin-valdespino
"""

import sys
import os
##from lines.LineComplete import LineComplete
from PyQt5 import uic, QtWidgets

qtCreatorFile = "FSFI.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        ##self.btn_pid.clicked.connect(self.addPID)
     ###########################################
     #codigo#
     

            
        
     ###########################################   

if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
