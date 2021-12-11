#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:03:46 2020

@author: joaquin-valdespino
"""
import sys
import os
from lines.LineComplete import LineComplete
from PyQt5 import uic, QtWidgets

qtCreatorFile = "maps.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btn_pid.clicked.connect(self.addPID)
     ###########################################
     #codigo#
     
     #event click button P_ID de la ventana#
    def addPID(self):
        print("adquirio p_id")
        self.map_tx.setText("");
        try:
            pidx = int(self.pid_tx.toPlainText())
            print(pidx)
            self.map_tx.setText(" mapeo del P_ID: "+str(pidx)+"\n");
            if(pidx >0):
                self.mapping(pidx)
            else:
                raise ValueError("p_id no valido")    
        except ValueError:
            self.map_tx.setText("mapeo no realizado")
            
    ##################################################### 
    def mapping(self,pid):
    ##### obtencion de maps en un txt ###
        maps = 'cat /proc/' + str(pid) + '/maps > maps'+str(pid)+'.txt'
        os.system(maps)
        ### files ###
        filemaps = open("maps"+str(pid)+".txt","r")
        filemap = open("MUVAMAP_"+str(pid).upper()+".txt","w") 
        
        ### lectura de lineas ###
        linesimp=[]
        Filelines = filemaps.readlines()
        
        for line in Filelines :
            segmentedline = line.split(" ")
            page = segmentedline[0]
            perm = segmentedline[1]
            use = segmentedline[len(segmentedline)-1]
            typeUse = ""
            
            if (use.find("[") != -1 and use.find("]") != -1):
                typeUse = use
                typeUse = typeUse.replace("[","")
                typeUse = typeUse.replace("]\n","")
                
            elif (use.find("home") != -1 and perm.find("r") != -1 and perm.find("x") != -1):
               typeUse = "Texto"
            elif (use.find("home") != -1 and perm.find("r") != -1 and perm.find("w") != -1):
               typeUse = "Datos"
            elif (use.find("lib") != -1 and perm.find("r") != -1 and perm.find("x") != -1):
               typeUse = "Bib-Texto"
            elif (use.find("lib") != -1 and perm.find("r") != -1 and perm.find("w") != -1):
               typeUse = "Bib-Datos"
            elif (use == "" or use =="\n"):
                use ="vacio"
            

             
            linesimp.append(LineComplete(page,perm,typeUse,use))   
          
        self.toPrint(linesimp,filemap)
        filemaps.close()
        filemap.close()
    
    #####imprimir en pantalla #####
    
    def toPrint(self,linesimp,file):
        print("entro toprint")
        print(len(linesimp))
        string = "| {:_^11} | {:_^16} | {:_^16} | {:_^16} | {:_^12} | {:_^4} | {} \n".format(" use"," De pag"," A pag"," Tamaño"," Num paginas"," Perm","Uso o mapeo")
        file.write(string)
        self.map_tx.append(string+"\n")
        for line in linesimp:
            string = line.toString()
            file.write(string)
            
            if(line.gettypeUse() == "stack"):
                Text = "<span style=\" font-size:9pt; font-weight:600; color:#ff0000;\" >"
                Text += string
                Text +="</span>"
                self.map_tx.append(Text+"\n")
            elif(line.gettypeUse() == "vvar"):
                Text = "<span style=\" font-size:9pt; font-weight:600; color:#fca71a;\" >"
                Text += string
                Text +="</span>"
                self.map_tx.append(Text+"\n")
            elif(line.gettypeUse() == "vdso"):
                Text = "<span style=\" font-size:9pt; font-weight:600; color:#a387a5;\" >"
                Text += string
                Text +="</span>"
                self.map_tx.append(Text+"\n")
            elif(line.gettypeUse() == "vsyscall"):
                Text = "<span style=\" font-size:9pt; font-weight:600; color:#87c725;\" >"
                Text += string
                Text +="</span>"
                self.map_tx.append(Text+"\n")
            elif(line.gettypeUse() == "Texto"):
                Text = "<span style=\" font-size:9pt; font-weight:600; color:#11a000;\" >"
                Text += string
                Text +="</span>"
                self.map_tx.append(Text+"\n")
            elif(line.gettypeUse() == "Datos"):
                Text = "<span style=\" font-size:9pt; font-weight:600; color:#ff8b08;\" >"
                Text += string
                Text +="</span>"
                self.map_tx.append(Text+"\n")
            elif(line.gettypeUse() == "Bib-Texto"):
                Text = "<span style=\" font-size:9pt; font-weight:600; color:#00bcd6;\" >"
                Text += string
                Text +="</span>"
                self.map_tx.append(Text+"\n")
            elif(line.gettypeUse() == "Bib-Datos"):
                Text = "<span style=\" font-size:9pt; font-weight:600; color:#6100d6;\" >"
                Text += string
                Text +="</span>"
                self.map_tx.append(Text+"\n")
            elif(line.gettypeUse() == "heap"):
                Text = "<span style=\" font-size:9pt; font-weight:600; color:#950000;\" >"
                Text += string
                Text +="</span>"
                self.map_tx.append(Text+"\n")                
            else:
                blackText = "<span style=\" font-size:9pt; font-weight:600; color:#000000;\" >"
                blackText +=string
                blackText +="</span>"
                self.map_tx.append(blackText+"\n")
            
        
     ###########################################   

if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
