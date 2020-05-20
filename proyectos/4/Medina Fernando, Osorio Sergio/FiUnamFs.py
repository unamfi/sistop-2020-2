import os
carp='/fiunamfs'
print("********************************************************\n**********************ADVERTENCIA***********************\n********************************************************\nLos comandos que serán utilizados requieren de que se \nejecuten como sudo o su, por ello se necesitará la \nejecución como sudo python3 FiUnamFs.py o brindar de \nmanera manual el permiso, cada que se le solicite")
os.system('sudo mkfs -t ext4 ./fiunamfs.img')
print('Creación de carpeta')
os.system('sudo mkdir /mnt'+carp)
os.system('sudo mount -r -t auto -o loop ./fiunamfs.img /mnt'+carp)
#print('Disco montado en /mnt/fiunamfs')
os.system('df -hT')
os.system('sudo umount /mnt'+carp)
print('Eliminación de la carpeta')
os.system('sudo rmdir /mnt'+carp)

