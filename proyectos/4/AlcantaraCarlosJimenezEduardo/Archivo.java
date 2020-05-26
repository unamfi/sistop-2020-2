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
    private String size;
    private String initClus;
    private String creationDate;
    private String modificationDate;
    private String bytesNotUsed;

    public Archivo(String name, String size, String initClus, String creationDate, String modificationDate, String bytesNotUsed) {
        this.name = name;
        this.size = size;
        this.initClus = initClus;
        this.creationDate = creationDate;
        this.modificationDate = modificationDate;
        this.bytesNotUsed = bytesNotUsed;
    }
    
    public Archivo(){
        this.name="Xx.xXx.xXx.xXx.";
        this.size="00000000";
        this.initClus="00000";
        this.creationDate="00000000000000";
        this.modificationDate="00000000000000";
        byte empty=(byte)0;
        this.bytesNotUsed=""+(char)empty+(char)empty+(char)empty;
    }

    public void setInitClus(int initClus){
        String clusterInicial=Integer.toString(initClus);
        while(clusterInicial.length()<5){
            clusterInicial="0"+clusterInicial;
        }
        this.initClus=clusterInicial;
    }
    
    public String getName() {
        String nombre="";
        char s[]=name.toCharArray();
        boolean bandera=false;
        for(char c:s){
            if(c!=' '){
                nombre=nombre+c;
                bandera=true;
            }else if(bandera==true){
                nombre=nombre+' ';
            }
        }
        return nombre;
    }

    public String getSize() {
        return size;
    }

    public String getInitClus() {
        return initClus;
    }

    public String getCreationDate() {
        return creationDate;
    }

    public String getModificationDate() {
        return modificationDate;
    }

    public String getBytesNotUsed() {
        return bytesNotUsed;
    }
    
    public byte[] getByteMap(){
        byte byteMap[]=new byte[Directorio.tamEntrada];
        char aux[]=this.name.toCharArray();
        for(int i=0;i<15;i++){
            byteMap[i]=(byte)aux[i];
        }
        
        aux=this.size.toCharArray();
        for (int i=16;i<24;i++){
            byteMap[i]=(byte)aux[i-16];
        }
        
        aux=this.initClus.toCharArray();
        for (int i=25;i<30;i++){
            byteMap[i]=(byte)aux[i-25];
        }
        
        aux=this.creationDate.toCharArray();
        for (int i=31;i<45;i++){
            byteMap[i]=(byte)aux[i-31];
        }
        
        aux=this.modificationDate.toCharArray();
        for (int i=46;i<60;i++){
            byteMap[i]=(byte)aux[i-46];
        }
        
        aux=this.bytesNotUsed.toCharArray();
        for (int i=61;i<64;i++){
            byteMap[i]=(byte)aux[i-61];
        }
        
        return byteMap;
    }
    
    
    public static Archivo getArchivo(byte byteMap[]){
        Archivo created;
        if(byteMap.length!=Directorio.tamEntrada){
            return null;
        }
        else{
            String name="";
            for(int i=0;i<15;i++){
                name=name+(char)byteMap[i];
            }
            
            String aux="";
            for (int i=16;i<24;i++){
                aux=aux+(char)byteMap[i];
            }
            String size=aux;
            
            aux="";
            for (int i=25;i<30;i++){
                aux=aux+(char)byteMap[i];
            }
            String initClus=aux;
            
            aux="";
            for (int i=31;i<45;i++){
                aux=aux+(char)byteMap[i];
            }
            String creationDate=aux;
            
            aux="";
            for (int i=46;i<60;i++){
                aux=aux+(char)byteMap[i];
            }
            String modificationDate=aux;
            
            aux="";
            for (int i=61;i<64;i++){
                aux=aux+(char)byteMap[i];
            }
            String bytesNotUsed=aux;
            
            created= new Archivo(name, size, initClus, creationDate, modificationDate, bytesNotUsed);
        }
        return created;
    }
}


