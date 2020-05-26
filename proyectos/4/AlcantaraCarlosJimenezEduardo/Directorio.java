/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sistemasOperativos.back;

import java.util.LinkedList;

/**
 *
 * @author carlo
 */
public class Directorio {
    public static int tamEntrada;
    private LinkedList<Archivo> archivos;
    
    public Directorio (Cluster directorio[]){
        archivos=new LinkedList<Archivo>();
        for(int j=0;j<directorio.length;j++){
            
            for(int i=0;i<Cluster.size/Directorio.tamEntrada;i++){
                
                archivos.add(Archivo.getArchivo(directorio[j].getByteMap(i*64,(i*64)+64)));
            }
        }
    }
    
    public boolean deleteFile(String name){
        boolean deleted=false;
        int tamDir=this.archivos.size();
        for(int i=0;i<tamDir;i++){
            Archivo f=archivos.get(i);
            if (f.getName().equals(name)==true){
                archivos.remove(i);
                archivos.add(i, new Archivo());
                deleted=true;
                break;
            }
        }
        return deleted;
    }
    
    public boolean insertFile(byte byteMap[]){
        boolean inserted=false;
        Archivo nuevaEntrada= Archivo.getArchivo(byteMap);
        for(int i=0;i<archivos.size();i++){
            Archivo actual=archivos.get(i);
            if(actual.getName().equals("Xx.xXx.xXx.xXx.")==true){
                archivos.remove(i);
                archivos.add(i,nuevaEntrada);
                inserted=true;
                break;
            }
        }
        return inserted;
    }
    
    @Override
    public String toString(){
        String s="";
        for (Archivo file:archivos){
            s=s+"\t"+file.getName()+"\n";
        }
        return s;
    }
    
    
    
}
