#!/usr/bin/env python3

class ENTRY_FS:
    name = "Xx.xXx.xXx.xXX."
    
    def __init__(self, entry):
        
        try:
            self.name = entry[0:15].decode("ascii").lstrip()
            print(self.name)
            self.size = int(entry[16:24].decode("ascii"))
            self.clus_init = int(entry[25:30].decode("ascii"))
            self.date_create = entry[31:45].decode("ascii")
            self.date_mod = entry[46:60].decode("ascii")
        ##self.empty_slot = entry[61:64].decode("ascii")
            self.array_ps = -1;
        except  UnicodeDecodeError:
            print("muy grande para decodificar")
            
       

