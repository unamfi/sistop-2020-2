from tkinter import *
from tkinter import ttk
import time

class Root(Tk):
    def __init__(self):
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
        self.progress_bar.grid(column=0, row=3)
    
    def run_progressBar(self):
        self .progress_bar['maximum'] = 100
        for i in range(101):
            time.sleep(0.05)
            self.progress_bar["value"] = i
            self.progress_bar.update()

        self.progress_bar["value"] = 0

    def start_progress(self):
        self.progress_bar.start()

    def stop_progress(self):
        self.progress_bar.stop()

root = Root()
root.mainloop()
'''
root = Tk()

root.title("Medical parallel")
root.config(bg='#CEF6F5')
root.iconbitmap("img/jeringa.ico")
root.geometry('800x600')

style = ttk.Style()
style.theme_use('clam')
style.configure("black.Horizontal.TProgressbar", background='#ccc')

bar = Progressbar(root, length=200, style='black.Horizontal.TProgressbar')
bar['value'] = 70
bar.grid(column=0, row=0)'''