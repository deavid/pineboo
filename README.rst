Pineboo - Manual de supervivencia
===================================
Se ha redactado este manual para las dudas más comunes sobre este proyecto de 
investigación, y ayudar a que cualquiera pueda poner en marcha y realizar las 
pruebas que desee con el mismo.

¿Qué demonios es Pineboo?
----------------------------
Pineboo es un proyecto de investigación, donde no se pretende obtener un producto
final, sino sentar una base y crear las tecnologías necesarias para el día de mañana
crear realmente el/los producto(s) que se deseen.

Lo que se desea es contestar a la frase: "Qué necesitamos para poder ejecutar un proyecto
de módulos de Eneboo sin Eneboo?"

Para ello, se crea un micro-proyecto (o mejor dicho, pico-proyecto) que solo cubre
lo mínimo necesario para cumplir esa frase, y estrictamente esa frase.

Es posible que exista más de una versión de Pineboo, cada una con distintas aproximaciones
y tecnologías. Actualmente, en el momento de escribir esta documentación, solo existe una.

El nombre de Pineboo viene de Pico-eneboo, y hace referencia que es un proyecto de 
investigación


Aproximaciones existentes
---------------------------
Solo existe una única aproximación a la ejecución de proyectos de Eneboo:

 - Python3.x + PyQt5
 - Permite ejecutarlo en PostgreSQL y en MySQL.
 - Motor realizado integramente en Python
 - Conversión al vuelo de QSA a PY con parseador FLScriptParser2 
 - Conversión al vuelo de formularios Qt3 a Qt5 creando un UiLoader manualmente
 

Dependencias
----------------
 - Python 3.x
 - PyQt5
 - PsycoPG2
 - Python PLY (flscriptparser)
 - Python LXML
 - FLScriptParser
 

Alcance actual de Pineboo
---------------------------
Pineboo es capaz de conectarse a cualquier base de datos de Eneboo y realizar
las siguientes tareas:

 - Funcionamientos habituales de las acciones
 - Trabajos normales de cursor (afterCommit, beforeCommit, ...)
 - Transacciones plenamente operativas sobre postgres
 - Impresión con jasperPluging configurado


Al iniciar una acción, el formulario es convertido al vuelo a Qt5 (con errores) y  
el script QS es convertido a Python y ejecutado (con muchos más errores). Se 
lanza el init() automáticamente.

Las referencias entre módulos (flfacturac.iface.XYZ) funcionan con carga de módulo
retrasada.

La API de QSA y Eneboo está en desarrollo. En la API aún existente son
funciones y clases "fake", que desde el script, parece que funcionen pero no 
realizan ningún trabajo. Esto permite ejecutar los scripts, pero no opera correctamente.

¿Si cargo Pineboo en mi base de datos de producción, puedo perder datos?
-------------------------------------------------------------------------
Sí, pueden perderse datos. Los experimentos con gaseosa. 

Dado que es un motor experimental, puede que no realice el trabajo que se le 
mande, sino otro inesperado. Un script podría de forma inadvertida borrar registros
por fallos en la API implementada. Y aquí nadie se hace responsable de esto.

Lo mejor es usarlo en bases de datos de desarrollo para evitar problemas.


Cómo poner en marcha Pineboo
------------------------------
    PASO 1 - DESCARGAMOS PINEBOO Y FLSCRIPTPARSER :
    PASO 2 - INSTALAMOS PYTHON 3.x :
    PASO 3 - CREAR EL PATH PARA PYTHON 3.X :
    PASO 4 - INSTALAR "Python-lxml" PARA WINDOWS :
    PASO 5 - INSTALAR PYTHON3-PLY :
    PASO 6 - INSTALAR PYTHON3-PYQT5 :
    PASO 7 - INSTALAR PYTHON3-FUTURE :
    PASO 8 - INSTALAR PYTHON3-PSYCOPG2 :
    PASO 9 - INSTALAR PYTHON3-XMLJSON :
    PASO 9B-Instalar PYTHON3-BARCODE :
    PASO 9C-Instalar PYTHON3-PILLOW :
    PASO 9D-Instalar PYTHON3-Z3C.RML :
    PASO 10 - INSTALAR SERVIDOR PostgreSQL o MySQL
    PASO 11 - DAR DE ALTA NUEVO USUARIO Y BASE DE DATOS EN SERVIDOR PostgreSQL o MySQL
    PASO 12 - ARRANCAR PINEBOO :
    PASO 13 - A�ADIR DATOS CONEXI�N AL FORMULARIO DE ENTRADA :

Al llamar al programa Pineboo �ste crea una base de datos sqlite llamada "conectores" en el subdirectorio "/projects". Es accesible desde una tabla-formulario.

Desde ese formulario se configura el acceso a la empresa elegida. Existe un bot�n en la tercera pesta�a desde el cu�l cargar una "Empresa de Prueba".

Con esto, pineboo debería iniciarse así::

    ./pineboo -l proyecto1
    
Veréis una lista de módulos y al pulsar salen las acciones.

Para que las acciones funcionen vais a necesitar la conversión de QS a PY, pero
esa tarea está en otro programa llamado flscriptparser::

    git clone git://github.com/deavid/flscriptparser.git

El proyecto está en github: https://github.com/deavid/flscriptparser

Pineboo lanza el comando flscriptparser2, que debe existir en el PATH. Si habéis
seguido las instrucciones de instalación, ya lo tenéis. Si no, pues podéis 
enlazarlo::

    sudo ln -s /path/to/flscriptparser/flscriptparser2 /usr/local/bin/flscriptparser2
    
Con esto debería de funcionar ya.

Algunos ejemplos interesantes son las acciones de articulos, tarifas, pedidoscli.

Pineboo en Windows
----------------------
S� se ha programado Pineboo pensando en que sea ejecutado en Windows. Se ejecuta con "python pineboo.py"

Para poner flscriptparser2 en el PATH a lo mejor
es más conveniente cambiar el PATH de windows.

Por otra parte todos los paquetes necesarios tienen que ser instalados uno a uno
en windows. Mira el listado de dependencias.

Pineboo y Eclipse
---------------------
Para integrar Pineboo con eclipse. Despues de instalar Eclipse añade los repositorios de PyDev  y Egit

PyDev
Help > install New Software > Add Repository
  http://pydev.org/updates

Egit
Help > install New Software > Add Repository
  http://download.eclipse.org/egit/updates

Ahora que tienes los compementos instalados, Create un fork de https://github.com/deavid/pineboo 
Despues importa ese repositorio Git.

Import > Git > Project from Git > Clone URI 

https://github.com/AquiTuUsuario/pineboo 


Cosas que se pueden probar en Pineboo
----------------------------------------
La opción --help ofrece un listado de opciones, algunas pueden ser interesantes.

Por ejemplo, para facilitar las pruebas existe el switch -a que ejecuta directamente
una acción determinada. (Abre el formulario master de esa acción)

Otra opción interesante es --no-python-cache que fuerza a regenerar los ficheros
de python transformados aunque ya existan. Útil si estamos jugando con flscriptparser.

Se puede probar a abrir el master de artículos y pulsar el botón de copiar artículo.
No copia el artículo pero sí pregunta la nueva referencia y hace el bucle de copia.

Si el master de artículos (u otro master) tiene checkboxes u otro método de filtrado
rápido, también funcionarán y la tabla se verá correctamente filtrada.

Si el master realiza comprobaciones sobre la fila seleccionada, también funcionan. 
Por ejemplo al albaranar un pedido puede advertirnos de que ya está servido.

Hay que tener en cuenta que la API de FLSqlCursor está implementada parcialmente.
La mayoría de señales no se envían aún y muchas de las funciones aún no tienen
implementación.

FLTableDB tiene una implementación a medio completar. Sólo se enlaza con el cursor por defecto
y más. Esto es suficiente para ejecutar muchos de los ejemplos.

El resto de objetos de Eneboo no existen o tienen una implementación "hueca", es 
decir, los métodos llegan a existir, pero no hacen nada.

Los formularios con convertidos al vuelo, y aún requiere este proceso de muchos
retoques. Las características más usadas funcionan, pero muchas de las cosas
que se pueden hacer en un formulario de Eneboo aún no son intepretadas correctamente.

Para ejecutar los scripts se usan tres capas de compatibilidad: flcontrols, qsaglobals
y qsatypes. 

Los ficheros son convertidos a python y guardados junto al fichero QS de cache.
Por ejemplo, las conversiones de masterarticulos.qs se pueden ver en la ruta
`tempdata/cache/nombre_bd/flfactalma/file.qs/masterarticulos/`.

 
