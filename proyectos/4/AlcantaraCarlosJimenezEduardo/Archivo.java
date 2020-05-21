/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sistemasOperativos.back;

/**
 *
 * @author carlo
 */
public class Archivo {
    private String name;
    private int size;
    private int initClus;
    private int creationDate;
    private int modificationDate;
    private int bytesNotUsed;

    public Archivo(String name, int size, int initClus, int creationDate, int modificationDate, int bytesNotUsed) {
        this.name = name;
        this.size = size;
        this.initClus = initClus;
        this.creationDate = creationDate;
        this.modificationDate = modificationDate;
        this.bytesNotUsed = bytesNotUsed;
    }
    
    public void setInitClus(int initClus){
        this.initClus=initClus;
    }
    
    public String getName() {
        return name;
    }

    public int getSize() {
        return size;
    }

    public int getInitClus() {
        return initClus;
    }

    public int getCreationDate() {
        return creationDate;
    }

    public int getModificationDate() {
        return modificationDate;
    }

    public int getBytesNotUsed() {
        return bytesNotUsed;
    }
    
    public static Archivo getArchivo(byte byteMap[]){
        if(byteMap.length!=Directorio.tamEntrada){
            return null;
        }
        else{
            String name="";
            for(int i=0;i<15;i++){
                name=name+(char)byteMap[i];
            }
            
            String size="";
            for (int i=16;i<24;i++){
                size=size+(char)byteMap[i];
            }
            
            
        }
    }
}


