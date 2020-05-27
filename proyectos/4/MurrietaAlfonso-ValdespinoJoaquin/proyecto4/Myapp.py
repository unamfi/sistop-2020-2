#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 22:29:52 2020

@author: joaquin-valdespino
"""

import sys
import os, os.path
import mmap, math, time 
from obb.entry_fs import ENTRY_FS
from obb.sblock  import sblock
from PyQt5 import uic, QtWidgets, QtGui

qtCreatorFile = "FSFI.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    fsimgm = open("fiunamfs.img","a+b")
    fsmap = mmap.mmap(fsimgm.fileno(), 0, access=mmap.ACCESS_WRITE)  
    block= sblock()
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btn_add.clicked.connect(self.cpfs)
        self.btn_df.clicked.connect(self.df)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_cp.clicked.connect(self.cpc)
        self.init.clicked.connect(self.loadDir)
        ##self.btn_pid.clicked.connect(self.addPID)
        
     ###########################################
     #codigo#
    ##obtenemos los elementos del directorio y los listamos en interfaz  
    def loadDir(self):
        self.listV.clear()
        self.listV.addItem('{:15} {:25} {:20} {:25} {:20}'.format("Cluster","Nombre", "Tamaño", "Creación", "Modificación"))
        list_e=[] ##lista de los elementos del directorio
        for entry in range(0,64):
        ## cada entrada es de 64 b
        ## el tamaño del directorio es de 1024
        ## 1024 * 4  = 4096
        ## por lo tanto la cantidad de entradas disponibles son 4096/64 =64
            print(entry)
            ac_entry = self.block.sizeclus + entry * 64
            ob_entry = ENTRY_FS(self.fsmap[ac_entry:(ac_entry + 64)])

            if ob_entry.name.find("Xx.") == -1:
                ob_entry.array_ps= entry
                list_e.append(ob_entry)
                self.listV.addItem('{:15} {:25} {:20} {:25} {:20}'.format(ob_entry.clus_init,ob_entry.name, ob_entry.size, self.dateString(ob_entry.date_create), self.dateString(ob_entry.date_mod)))
        return list_e
    
    #da forma a la fecha para imprimirla
    def dateString(self,date): 
        return date[0:4]+"/"+date[4:6]+"/"+date[6:8]+" "+date[8:10]+":"+date[10:12]+":"+date[12:14]
    
    ##empezamos la funcion de copiar a fs
    ##VERIFICA QUE EL archivo exista, por una parte dentro de fiunamfs o fuera de fs
    def cpfs(self):
        file = self.txt_inst.toPlainText()
        print(file)
        if os.path.isfile(file):
            if self.getEntry(file) != None:
                self.lb_msg.setText("this file already exist");
            else:
                print("loading....")
                self.genEntry(file);
        else:
            self.lb_msg.setText("this file not exist, please retry");
    
    ##obtiene la entrada y su posicion en caso de existir en fs
    def getEntry(self, name):
        for entry in range(0,64):
            ac_entry = self.block.sizeclus + entry * 64
            ob_entry = ENTRY_FS(self.fsmap[ac_entry:(ac_entry + 64)])

            if name == ob_entry.name:
                print("OMG")
                ob_entry.array_ps = entry
                return ob_entry
        return None
    
    ## en caso de agregar, se genera una entrada donde se cargaran sus datos correspondientes
    def genEntry(self, file):
        entrys = self.loadDir()
        entrys.sort(key = lambda x : x.clus_init)
        size = os.stat(file).st_size
        ##ceil redondea el numero obtenido, es mejor que truncar el valor
        clus_file = math.ceil(size/self.block.sizeclus)

        #si fs no tiene elementos se añadira a partir del cluster 5 ya que antes es el superbloque
        if len(entrys) == 0:
            #los clusters de tamaño del archivo a añadir no debe sobrepasar el tamaño total de los clusters
            if  clus_file <= (self.block.tot_clus - 4):
                f = open(file,"rb")
                send = self.block.size_clus * 5
                self.fsmap[send:(send + size)] = f.read()
                self.loadfile(file,5)
                f.close()
            else:
                self.lb_msg.setText(file + "to big")
        else:
            copy = False
            ##buscara una seccion contigua desocupada
            for entry in range(0,len(entrys)-1):
                last_clus = entrys[entry].clus_init + math.ceil( entrys[entry].size / self.block.sizeclus)
                between_space = entrys[entry+1].clus_init - last_clus

                if clus_file <= between_space:
                    f = open(file,"rb")
                    part = int(self.block.sizeclus * (clus_file + 1))
                    self.fsmap[part : part + size ] = f.read()
                    self.loadfile(file,clus_file + 1)
                    f.close()
                    copy = True
                    break
            # en caso de fallo al insertar, tratara de insertar al final del espacio ( +-ultimo cluster)
            if copy == False:
                last = entrys[len(entrys) - 1].clus_init + math.ceil(entrys[len(entrys) - 1].size / self.block.sizeclus )
                freespace = self.block.tot_clus - last
                if clus_file <= freespace:
                    f = open(file,"rb")
                    part = self.block.tot_clus * (last + 1)
                    self.fsmap[part : part + size] = f.read()
                    self.loadfile(file, last + 1)
                    f.close()
                    copy= True
                else:
                    self.lb_msg.setText(file + "to big")
        
    
    def loadfile(self,file,clus):
        for entry_i in range(64):
            part = self.block.sizeclus + entry_i*64
            ent = ENTRY_FS(self.fsmap[part:part + 64])
            if "Xx.xXx.xXx.xXx." == ent.name:
                # se rellena con espacios
                self.fsmap[part:part + 15] = file.rjust(15).encode('ascii')
                size = str(os.stat(file).st_size) #tamaño del archivo en bytes
                print(part)
                print(len(ent.name))
                npart = part + 16
                print(npart)
                ##zfill rellena con 0 la cadena
                ##npart hace el recorrido sobre los espacios de cada byte llenando con los datos correspondientes a la documentacion 
                self.fsmap[npart :npart + 8] = size.zfill(8).encode("ascii")
                clus_file = str(clus)
                npart += 9
                self.fsmap[npart:npart + 5] = clus_file.zfill(5).encode('ascii')

                date_c= time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getctime(file)))
                npart += 6
                self.fsmap[npart:npart + len(ent.date_create)] = date_c.encode('ascii')

                date_md=time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getmtime(file)))
                npart += 15
                self.fsmap[npart:npart + 14] = date_md.encode('ascii')        
                
                self.lb_msg.setText("copy to FS success")
                self.loadDir()
                break
            
    ##la funcion elimina un elemento del directoio     
    def delete(self):
        item = self.listV.currentItem()
        strings = item.text().split(" ")
        print("ha seleccionado: "+strings[15])
        file = strings[15]
        entry = self.getEntry(file)
        if entry != None:
            aux_entry = self.block.sizeclus + 64 * entry.array_ps
            ##eliminamos dejando al nombre como un una entrada sin utilizar, dejando los demas datos como basura sin utilizar 
            self.fsmap[aux_entry:aux_entry+15] = bytes(("Xx.xXx.xXx.xXx.").encode('ascii'))
            self.lb_msg.setText("delete success")
        else:
            self.lb_msg.setText("not deleted")
        self.loadDir()
    
    ## funcion que copia un elemento de fs a nuestra pc dada una ruta absoluta(preferentemente)
    def cpc(self):
        item = self.listV.currentItem()
        strings = item.text().split(" ")
        print("ha seleccionado para copiar: "+strings[15])
        file = strings[15] #name archivo a copiar
        pathfinder = self.txt_inst.toPlainText() ##ruta donde se va a copiar
        entry = self.getEntry(file)
        if entry != None :
            if os.path.exists(pathfinder): ## verifica que la ruta sea valida
                ##copiamos el archivo pasando su contenido 
                filecpd = open(pathfinder+"/"+file,"a+b")
                clus = self.block.sizeclus * entry.clus_init
                filecpd.write(self.fsmap[clus:clus+ entry.size])
                filecpd.close()
            else:
                self.lb_msg.setText("directory "+pathfinder+" not exist ")
        else:
            self.lb_msg.setText("file "+ entry.name +" not exist")
    
    ## funcion para desfragmentar fs 
    def df(self):
        ##empezamos del cluster 5 ya que antes es el superbloque
        entrys = self.loadDir()
        clus_init_srch=5
        clus = {}
        
        for entry in entrys:
             aux_e = [entry.size, entry.array_ps]
             clus[entry.clus_init] = aux_e
        #se verifica si se pueden mover los elementos (64 b) por cada entrada
        for clusts in range(len(clus)):
            minc = min(clus)
            if(minc > clus_init_srch):
                 init = self.block.sizeclus * minc
                 end = math.ceil(clus.get(minc)[0]/self.block.sizeclus) ##cluster usados del file
                 file = self.fsmap[init : init + (end*self.block.sizeclus)] ##toma a file
                 self.fsmap[clus_init_srch * self.block.sizeclus : (clus_init_srch * self.block.sizeclus) + (end * self.block.sizeclus)] = file #reposiciona 
            aux_e = clus.get(minc)
            del clus [minc]
            #se actualiza la posicion de los datos de file
            rdata = 1024 + (aux_e[1] * 64)
            self.fsmap[rdata + 25 : rdata + 30] = str(clus_init_srch).zfill(5).encode('ascii')
            num_clus_file = math.ceil(aux_e[0] / self.block.sizeclus)
            clus_init_srch += num_clus_file #nuevo valor del clus_init para realizarlo de manera contigua
        
        self.lb_msg.setText("desfragmentado")
        self.loadDir()
         
     ###########################################   
        
if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
