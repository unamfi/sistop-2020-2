from tkinter import *
from tkinter import ttk, scrolledtext
from tkinter.ttk import *
import time
from main import main

class Root:
    def __init__(self, window):
        # Inicializando la ventana de la apliación
        self.wind = window
        self.wind.title('Medical Parallel')
        self.wind.minsize(600,500)
        self.wind.iconbitmap("img/jeringa.ico")
        self.wind.config(bg='#CEF6F5')

        # Crando un Frame como contenedor
        frame = LabelFrame(self.wind, text = 'Registre el análisis del paciente')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Nombre del análisis
        Label(frame, text = 'Análisis: ').grid(row = 1, column = 0)
        #self.name = Entry(frame)
        self.name = Combobox(frame)
        self.name['values']= ["Hemoglobina","Glucemia"]
        self.name.grid(row = 1, column = 1)
        #self.name.focus()
        #self.name.grid(row = 1, column = 1)

        # Tiempo del análisis
        Label(frame, text = 'Tiempo estimado: ').grid(row = 2, column = 0)
        #self.analy = Entry(frame)
        #self.analy.grid(row = 2, column = 1)
        self.analy = Combobox(frame)
        self.analy['values']= ["1 día","2 días","3 días"]
        self.analy.grid(row = 2, column = 1)

        # Perfil al que está asociado
        Label(frame, text = 'Perfil: ').grid(row = 3, column = 0)
        #self.profile = Entry(frame)
        #self.profile.grid(row = 3, column = 1)
        self.profile = Combobox(frame)
        self.profile['values']= ["Sanguíneo","Lípidos","Triglicéridos"]
        self.profile.grid(row = 3, column = 1)

        selected =  IntVar()
        #Validación de diabetes
        Label(frame, text = 'Diabetes').grid(row = 4, column = 0)
        Radiobutton(frame,text='Sí', value=1, variable=selected).grid(row = 4, column = 1)
        #self.validate = Entry(frame)
        #self.validate.grid(row = 4, column = 1)

        # Button Add Product 
        ttk.Button(frame, text = 'Agregar proceso').grid(row = 7, columnspan = 2, sticky = W + E)

        # Output Messages 
        #self.message = Label(text = '', fg = 'red')
        #self.message.grid(row = 4, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 10, columns=("#0","#1","#2",))
        self.tree.grid(row = 4, column = 0, columnspan = 3)
        self.tree.heading('#0', text = 'Análisis', anchor = CENTER)
        self.tree.heading('#1', text = 'Tiempo', anchor = CENTER)
        self.tree.heading('#2', text = 'Perfil', anchor = CENTER)
        self.tree.heading('#3', text = 'Diabetes', anchor = CENTER)

        #Botón de iniciar simulación
        ttk.Button(window, text = 'Iniciar simulación', command = main).grid(row = 5, columnspan = 4, sticky = W + E)
        ttk.Button(window, text = 'Mostrar resultados simulación', command =self.mostrar).grid(row = 6, columnspan = 4, sticky = W + E)

        #Resultados
        self.tree = ttk.Treeview(height = 10, columns=1)
        self.tree.grid(row = 4, column = 0, columnspan = 4)
        self.tree.heading('#0', text = 'Resultados', anchor = CENTER)

        self.txt = scrolledtext.ScrolledText(window,width=40,height=10)
        self.txt.grid(row = 7, columnspan = 4, sticky = W + E)

    def mostrar(window):
        resultados = main()
        for i in range(len(resultados)):
            window.txt.insert(INSERT,resultados[i] + "\n")

    #def agregar_process():
    #    self.tree.insert("","end", values = self.tree.get_children())
    #    return
    '''def __init__(self):
        super(Root, self).__init__()
        self.title("Medical parallel")
        self.minsize(800,600)
        self.iconbitmap("img/jeringa.ico")
        self.config(bg='#CEF6F5')

        self.buttonFrame = ttk.LabelFrame(self, text="Progress Bar")
        self.buttonFrame.grid(column=0, row=0)

        self.progressBar()

    def progressBar(self):
        self.butt0n = ttk.Button(self.buttonFrame, text="Start Progress Bar", command=self.start_progress)
        self.butt0n.grid(column=0, row=0)

        self.butt1n = ttk.Button(self.buttonFrame, text="Stop Progress Bar", command=self.stop_progress)
        self.butt1n.grid(column=0, row=1)

        self.progress_bar = ttk.Progressbar(self, orient = 'horizontal', length= 286, mode='determinate')
        self.progress_bar.grid(column=0, row=2)
    
    def run_progressBar(self):
        self.progress_bar['maximum'] = 100
        for i in range(101):
            time.sleep(0.05)
            self.progress_bar["value"] = i
            self.progress_bar.update()

        self.progress_bar["value"] = 0

    def start_progress(self):
        self.progress_bar.start()

    def stop_progress(self):
        self.progress_bar.stop()'''

if __name__ == '__main__':
    window = Tk()
    application = Root(window)
    window.mainloop()