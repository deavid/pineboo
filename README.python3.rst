Pineboo - Hoja de ruta
====================================================


Dependencias con Python3
-----------------------------------

Prácticamente lo mismo que antes, pero los paquetes se llaman python3-xyz.

- Python3.3 o posterior
- psycopg2
- sqlite3
- MySQLdb (*MySQL opcional)
- pyqt5 
- lxml
- ply

$ sudo apt-get install python3-lxml python3-psycopg2 python3-ply python3-pip
$ sudo pip3 install PyQt5

Adicionalmente, hacemos uso de un paquete llamado "future", que es el que me
ha ayudado a hacer la transformación con una herramienta llamada futurize.

Future se usa ahora en el código para que Python2.7 pueda ejecutar nuestro
código de python3 y que ambos hagan lo mismo. (Emulando python3).

Esto hace que algunos ficheros requieran de esta librería con Python3, pero creo
que es una dependencia que se puede eliminar en el futuro (cuando casi nadie use
python2). De todos modos para Python3 creo que no hace casi nada.

   $ sudo pip3 install future

Por otra parte he usado pylint para parsear el código... mientras era python2.
Con Python3 no consigo instalar pylint en este sistema. Supongo que se arreglará
en versiones futuras.


Cosas que hay que hacer ahora
---------------------------------

- Refactorizar algunas funciones que se han vuelto un poco grandes
- flparser no reconoce funciones anónimas (lambdas)
- los cursores deberían realizar las consultas con cursores de servidor por defecto
- Mejorar soporte MySQL y SQLite
- AQSobjects
- Mejorar FLTableDB
- Kugar



