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
investigación, pensado más como una pequeña utilidad que como un programa real.


Aproximaciones existentes
---------------------------
Solo existe una única aproximación a la ejecución de proyectos de Eneboo:

 - Python3.x + PyQt5 + PsycoPG2 (El un futuro será según opción sql seleccionada (PostgreSQL, MySQL, SQLite, ...)
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

 - Listar los módulos
 - Listar las acciones posibles para un módulo
 - Iniciar el OpenDefaultForm() para una acción dada

Al iniciar una acción, el formulario es convertido al vuelo a Qt4 (con errores) y  
el script QS es convertido a Python y ejecutado (con muchos más errores). Se 
lanza el init() automáticamente.

Las referencias entre módulos (flfacturac.iface.XYZ) funcionan con carga de módulo
retrasada.

La API de QSA y Eneboo está apenas empezada. En su mayoría la API existente son
funciones y clases "fake", que desde el script, parece que funcionen pero no 
realizan ningún trabajo. Esto permite ejecutar los scripts, pero no opera correctamente.

¿Si cargo Pineboo en mi base de datos de producción, puedo perder datos?
-------------------------------------------------------------------------
Sí, pueden perderse datos. Los experimentos con gaseosa. 

Dado que es un motor experimental, puede que no realice el trabajo que se le 
mande, sino otro inesperado. Un script podría de forma inadvertida borrar registros
por fallos en la API implementada. Y aquí nadie se hace responsable de esto.

Lo mejor es usarlo en bases de datos de desarrollo para evitar problemas.

Actualmente, en el momento de escribir esta documentación, Pineboo no puede
permutar la base de datos, porque carece de las API's para ello.

No obstante esto podría cambiar en el futuro y estar la documentación 
desactualizada.


Cómo poner en marcha Pineboo
------------------------------
Bien, supongo que la mayoría de la gente antes de leer esto habrá intentado
ejecutar "./pineboo" y se ha encontrado con un diálogo de conexión que no funciona.

Efectivamente, no funciona. O mejor aún, no está programado siquiera. Si a agluien 
le apetece colaborar, este formulario es un buen inicio.

Para poder iniciarlo se necesita especificar manualmente la conexión. Y la única
forma es a través de un XML de proyecto.

Tenéis una carpeta llamada "projects/" y dentro un ejemplo "eneboo-base.xml".
Debéis copiar el ejemplo a otro nombre, por ejemplo "proyecto1.xml" y cambiarle 
los datos de conexión.

Cuando cambiéis los datos de conexión de vuestro "proyecto1.xml" a lo mejor os
preguntáis para que sirve lo del nombre o lo del path de la aplicación, de si
hay que cambiarlo o no. Es puramente decorativo, así que lo podéis dejar tal cual.
Es posible que la aplicación sí lea el contenido, aunque no lo use, así que no 
borréis las etiquetas ni su contenido. Por lo que pueda pasar.

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
No se ha programado Pineboo pensando en que sea ejecutado en Windows. Pero no hay 
nada que impida que funcione. Nadie lo ha probado. Probablemente con las instrucciones
genéricas funcione también. Para poner flscriptparser2 en el PATH a lo mejor
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

FLTableDB tiene una implementación mínima. Sólo se enlaza con el cursor por defecto
y poco más. Esto es suficiente para ejecutar muchos de los ejemplos.

El resto de objetos de Eneboo no existen o tienen una implementación "hueca", es 
decir, los métodos llegan a existir, pero no hacen nada.

Los formularios con convertidos al vuelo, y aún requiere este proceso de muchos
retoques. Las características más usadas funcionan, pero la gran mayoría de cosas
que se pueden hacer en un formulario de Eneboo aún no son intepretadas correctamente.
No obstante, debería ser suficiente para ejecutar muchos de los formularios master
que existen.

Para ejecutar los scripts se usan tres capas de compatibilidad: flcontrols, qsaglobals
y qsatypes. En algunos casos no está aún claro cómo debería comportarse por ejemplo
un Array. 

Los ficheros son convertidos a python y guardados junto al fichero QS de cache.
Por ejemplo, las conversiones de masterarticulos.qs se pueden ver en la ruta
`tempdata/cache/flfactalma/file.qs/masterarticulos/`.

Cosas que realizar a medio plazo
----------------------------------------
 - Más API's de Eneboo clonadas
 - Diálogo de conectar que funcione
 - Establecer conexión manual desde consola usando formato URI
 - Apertura de formularios de registro (Browse)
 - Creación de switch "--read-only-mode", donde los commitBuffer y commit sean inocuos.
 
