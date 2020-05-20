echo "El tamaño del disco es:"
eval fdisk -s ./fiunamfs.img
echo "MB"
eval fdisk ./fiunamfs.img
eval n
eval p
eval 1

