Pineboo - Migración a Python3 y nueva hoja de ruta
====================================================

He decidido migrar todo a Python3. El motivo es que Python2 está cerca de ser
abandonado. No hay nuevas releases, y a día de hoy empieza a haber más gente
programando cosas nuevas con python3 que con python2 (aunque siguen muy
igualados)

Para el día en que Pineboo pueda serle útil a alguien, probablemente Python2
ni siquiera sea una opción. Es posible que antes del 2018 python2 sea obsoleto
y complicado de instalar en sistemas actuales.

Nuevas dependencias con Python3
-----------------------------------

Prácticamente lo mismo que antes, pero los paquetes se llaman python3-xyz.

- Python3.3 o posterior
- psycopg2
- pyqt4
- lxml
- ply

Adicionalmente, hacemos uso de un paquete llamado "future", que es el que me
ha ayudado a hacer la transformación con una herramienta llamada futurize.

Future se usa ahora en el código para que Python2.7 pueda ejecutar nuestro
código de python3 y que ambos hagan lo mismo. (Emulando python3)

Esto hace que algunos ficheros requieran de esta librería con Python3, pero creo
que es una dependencia que se puede eliminar en el futuro (cuando casi nadie use
python2). De todos modos para Python3 creo que no hace casi nada.

Esta dependencia, al menos en ubuntu 14.04 necesita de "pip" para instalarse.
No está disponible para apt-get.

   $ sudo apt-get install pip3
   $ sudo pip3 install future

Por otra parte he usado pylint para parsear el código... mientras era python2.
Con Python3 no consigo instalar pylint en este sistema. Supongo que se arreglará
en versiones futuras.


Porqué se mantiene Qt4 y no se introduce ya Qt5
-------------------------------------------------

Qt3 es muy distinto de Qt4. Además, Eneboo tiene modificaciones grandes a Qt y
a QSA, haciendo imposible seguir una guía estándar de actualización.

Al menos, con Qt4, tenemos un set de controles "compatibles" con Qt3. Se conocen
como Qt3Support.

Pero, con Qt5 estos módulos desconozco si continúan existiendo, pero creo que no.
Qt5 está pensado para que la gente migre fácilmente aplicaciones de Qt4. Pero
esto aún ni siquiera es una aplicación Qt4.

Ubuntu no distribuye para 14.04 un módulo pyqt5 para python2.
Y por otra parte Qt5 aún está empezando y tiene mucho margen para crecer.
Siempre se podrá migrar más tarde.


Cosas que hay que hacer ahora
---------------------------------

- Integrar la parte de flscriptparser que usamos dentro de pineboo. (* hecho)
- Modificar el parseador para que escriba código Python3 (* hecho)
- Agregar una opción "-c" para indicar la conexión por consola. (* hecho)
- Crear un fichero de utilidades y mover algunas funciones (* hecho)
- Modificar el diálogo de conexión para que funcione
- Erradicar el uso de ficheros xml para proyecto, dejar la opción, pero como
  obsoleta
- Refactorizar algunas funciones que se han vuelto un poco grandes
- Cargar al inicio los ficheros principales de cada módulo
- flparser no reconoce valores de array ni objetos insertados in-line (x = []; y = {})
- flparser no reconoce funciones anónimas (lambdas)
- flparser no reconoce el operador ternario ( x ? y : z ; y if x else z )
- los cursores deberían realizar las consultas con cursores de servidor por defecto



