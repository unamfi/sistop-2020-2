#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 23:39:42 2020

@author: joaquin-valdespino
"""
class LineComplete:
    ## class para la informacion de una linea del map ##    
    __Ipage='na'
    __Epage='na'
    __perm='na'
    __size='na'
    __npages='na'
    __use='na'
    __typeUse='na'
    
    def __init__(self,page,perm,typeUse,use):
        print("init:"+page)
        self.pageInfo(page)
        self.__perm = perm
        self.__typeUse = typeUse
        self.__use = use
        
        
    def pageInfo(self,page):
      
        segmentedpage = page.split("-")

        
        self.__Ipage = segmentedpage[1]
        self.__Epage = segmentedpage[0]

        kbs = int((int(self.__Ipage,16) - int(self.__Epage,16))/1024)
        ##size##
        if ((kbs/1048576)>=1):
            self.__size=str((kbs/1048576))+" GB"
        elif((kbs/1024)>=1):
            self.__size=str(kbs/1024)+" MB"
        else:
            self.__size=str(kbs)+" KB"
        
        ##numero de pags##
        self.__npages = str(int(kbs/4))+" pages"
  
    def toString(self):
        return '| {:_^11} | {:_^16} | {:_^16} | {:_^16} | {:_^12} | {:_^4} | {} '.format(self.__typeUse,self.__Ipage,self.__Epage,self.__size,self.__npages,self.__perm,self.__use)
        
    def gettypeUse(self):   
        return self.__typeUse
        
        
        
        
        
        
        