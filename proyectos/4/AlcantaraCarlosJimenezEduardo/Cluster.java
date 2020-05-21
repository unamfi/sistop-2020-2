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
    private LinkedList<Sector> sectors;
    private Integer size;
    private Boolean used;
    
    public Cluster(int size){
        this.size=size;
        sectors=new LinkedList<Sector>();
        for (int i=0;i<size;i++){
            sectors.add(null);
        }
    }
    
    
    public void setSector(int index,Sector sec){
        sectors.set(index, sec);
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
}
