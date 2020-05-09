async function generateMap() {
	var data = document.getElementById("data").value
    let backvalues = await eel.getPID(data)()
    backvalues[0]=""+backvalues[0]+"%"
    backvalues[1]=""+backvalues[1]+"%"
    backvalues[2]=""+backvalues[2]+"%"
    backvalues[3]=""+backvalues[3]+"%"
    backvalues[4]=""+backvalues[4]+"%"    
    document.getElementById("div1").style.height = backvalues[0];
    document.getElementById("div2").style.height = backvalues[1];
    document.getElementById("div3").style.height = backvalues[2];
    document.getElementById("div4").style.height = backvalues[3];
    document.getElementById("div5").style.height = backvalues[4];
    backvalues[0]="Texto: "+backvalues[0]
    backvalues[1]="\nDatos: "+backvalues[1]
    backvalues[2]="\nHeap: "+backvalues[2]
    backvalues[3]="\nBibliotecas: "+backvalues[3]
    backvalues[4]="\nStack: "+backvalues[4]
    alert("AVISO: El mapa cargara despues de aceptar estos mensajes. \nLos porcentajes de las secciones de memoria en el mapa son:\n")
    alert(backvalues)
}

