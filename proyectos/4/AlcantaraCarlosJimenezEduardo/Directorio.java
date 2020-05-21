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
    private LinkedList<Archivo> archivos;
    
    public String toString(){
        String s="";
        for (Archivo file:archivos){
            s=s+"\t"+file.getName()+"\n";
        }
        return s;
    }
}
