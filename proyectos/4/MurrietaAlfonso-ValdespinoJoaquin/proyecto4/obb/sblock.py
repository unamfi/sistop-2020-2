#!/usr/bin/env python3

import mmap
class sblock:

    ##superbloque datos de fiunamfs
    def __init__(self):
        print("iniciando superblock")
        fsimg = open("../proyecto4/fiunamfs.img","r+b")
        fmap =  mmap.mmap(fsimg.fileno(), 0, access=mmap.ACCESS_READ)
        self.fsname = fmap[0:8].decode("ascii")
        self.ver =  fmap[10:13].decode("ascii")
        self.vol =  fmap[20:35].decode("ascii")
        self.sizeclus=  int(fmap[40:45].decode("ascii")) 
        self.ndir_clus=  int(fmap[47:49].decode("ascii")) 
        self.tot_clus=  int(fmap[52:60].decode("ascii"))
        print(self.fsname)
        print(self.ver)
        print(self.vol)
        print(self.sizeclus)
        print(self.ndir_clus)
        print(str(self.tot_clus)+"\n")
            
        fmap.close()
        fsimg.close()