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



