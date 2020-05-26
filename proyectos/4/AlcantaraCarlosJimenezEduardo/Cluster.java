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
public class Cluster {
    public static Integer size;
    private Boolean used;
    private LinkedList<Byte> byteMap;
    
    
    public Cluster(){
        byteMap=new LinkedList<Byte>();
        for (int i =0;i<size;i++){
            byteMap.add(null);
        }
        this.used=false;
    }
    
    public Cluster(byte byteMap[]){
        size=byteMap.length;
        this.byteMap=new LinkedList<Byte>();
        for (int i =0;i<size;i++){
            this.byteMap.add(byteMap[i]);
        }
        this.used=true;
    }
    
    public Boolean isUsed(){
        return this.used;
    }
    
    private void setUsed(Boolean used){
        this.used=used;
    }
    
    public void marcarUsado(){
        this.setUsed(true);
    }
    
    public void marcarNoUsado(){
        this.setUsed(false);
    }
    
    public byte[] getByteMap(){
        return SistemaDeArchivos.toArray(byteMap);
    }
    
    public byte[] getByteMap(int indexA,int indexB){
        byte res[]= new byte[indexB-indexA];
        byte divide[]=getByteMap();
        int j=0;
        for(int i=indexA;i<indexB;i++){
            res[j]=divide[i];
            j=j+1;
        }
        return res;
    }
    
}
