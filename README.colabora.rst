Cómo colaborar en Pineboo
=====================================

Primero de todo, hemos de entender cómo funciona internamente Pineboo. Además,
habremos de familiarizarnos con Python3, especialmente hay algunas técnicas más
avanzadas que se usan para "hacer creer" al código QS que lo que hay detrás es
un motor QSA Qt3.


Cómo funciona Pineboo por dentro
---------------------------------

Pineboo está programado como una librería, por lo que todo el código está dentro
de la carpeta pineboolib. Los ficheros exteriores únicamente sirven como
lanzadores. El programa principal es main.py. En él se desarrolla prácticamente
todo lo que hace Pineboo, hasta el punto que deberíamos intentar separarlo en
partes más pequeñas según qué funcionalidad cubren. Ahora mismo main.py
controla casi todo lo que hace pineboo.

A grosso modo, el proceso de carga es el que sigue:

- Conexión a la base de datos
- Descarga de ficheros flfiles a carpeta de caché (tempdata/cache)
- Interpretado de los ficheros XML y UI de acciones
- Creación del formulario y rellenado con sus modulos y acciones.
- Al hacer clic en una acción (o si pasamos el switch -a) se dispara la carga
  de la misma, con su formulario.
- Si el fichero .py no existe, vamos al QS, lo convertirmos en XML y después a PY
- Se importa dinámicamente el fichero py
- Se crea el widget de la pestaña leyendo Qt3 y generando controles Qt4
- Se ejecuta el init de la acción

De forma más reciente, se soporta también la llamada a la acción EditRecord que
hace algo parecido a lo anterior: (este proceso está bastante inacabado)

- Se convierte el QS a PY
- Se crea el formulario pestaña leyendo Qt3 y generando controles Qt4
- Importamos dinámicamente el PY y ejecutamos el init.

Aspectos interesantes en los procesos de pineboo
---------------------------------------------------

La descarga de ficheros de base de datos a la caché, tiene una "heurística" para
detectar la codificación correcta. No es infalible, pero parece que funciona bien.

Los ficheros de la caché se guardan en carpetas con el nombre del fichero, y el
fichero realmente tiene de nombre el hash. Esto está así a propósito. De este
modo mezclo las cachés de distintos programas. Si dos programas comparten un
fichero, este no se convierte dos veces. Si un fichero se modifica, cambia de
nombre. Esto me simplifica bastante la vida.

La lectura de los XML y los UI se hace a través de python-lxml, que tendréis que
aprender si queréis modificar o mejorar el código, aunque no creo que haga falta
mucha colaboración en este punto concreto. Se guardan en una serie de clases,
que la verdad, podrían estar mejor organizadas, ya que todas están en main.py y
por otra parte hay cosas que están desperdigadas en otras clases cuando podríamos
unificarlas por simplicidad. Hay clases diferentes para acciones según si venía
del xml o del ui.

Estoy usando XMLStruct para mapear lo que se ve en los ficheros XML a propiedades
de la clase. De este modo es mucho más fácil leer los ficheros. El problema es
que en el código es un poco más complicado de seguir.

Respecto al formulario principal de la aplicación, José Antonio Fernández ya lo
mejoró bastante, y viendo cómo está ahora mismo yo, en mi opinión, focalizaría
los esfuerzos en otro área.

La conversión de QS a Python tiene bastante miga, en principio no espero
colaboración en este área por su complejidad, pero también es la que más
acabada tenemos. Sí agradecería colaboración detectando errores traduciendo de
QS a Python; por ejemplo si un código de QS parece que vaya a hacer otra cosa
en Python, o no se convierte del todo, u otro error. Obviamente para que
convierta, tiene que parsear bien, y es mucho más sensible que Eneboo a ciertas
formas de trabajo.

La importación dinámica de python, bueno, en principio se supone que sólo se
pueden importar ficheros de código si se conoce previamente su nombre, pero
usando (hackeando) el código del importador, es posible decirle que importe el
que quieras. No es muy complicado, funciona, y creo que está terminado. La
ventaja de importar dentro es que Python compila a bytecode el código fuente,
por lo que acelera su ejecución y además se cachea en disco para que la próxima
vez la importación sea casi instantánea.

Sobre la conversión de Qt3 a Qt4, lo que se hace a groso modo es leer el XML del
fichero UI (formato Qt3) y empezamos a seguir sus instrucciones para crear un
formulario con la misma "receta". El problema es que los "ingredientes" no son
los mismos en Qt4, por lo que hay que ir traduciendo nombres de propiedad o
controles al vuelo. Lo más importante aquí es que un control lo busca primero
en "flcontrols.py" y después lo busca en Qt4. Eso quiere decir que si defines
en flcontrols un control que sí existe en Qt4, fuerzas al UI a cargar este
control en lugar del que viene por defecto, eso nos permite cambiarle las
propiedades o ampliarlas.

Sobre la ejecución del código de la acción, actualmente solo lanzamos el init.
Hay que tener en cuenta que al principio del py traducido hay unos cuantos imports
que facilitan emular Qt3+QSA.

Dónde hay que colaborar en Pineboo
---------------------------------------

La parte donde más trabajo tenemos que poner todos es en la API de los ficheros
QS y en los controles FL*.

Por mucho que ya traducimos a Python, ahora ese código empieza a buscar funciones
en FLUtil que no existen, los controles FLTableDB le falta casi toda la funcionalidad,
las FLSqlQuery no están ni implementadas, etc, etc.

Muchas de esas cosas están en Qt4 mejor resueltas que en Qt3, por lo que a veces
con sencillos "wrappers" que emulen el comportamiento antiguo haría que todo
empezase a funcionar. Pero hay mucho curro de ir función por función y enlazándola
donde le toca. Además hay que probar mucho código, para ir viendo cómo funciona
todo en la realidad.

Todo esto de la API se divide en unos pocos ficheros:

- **flcontrols.**
  Aquí pondremos todo lo que sean controles visuales de Qt, especialmente
  si queremos que qt3ui, al traducir el formulario, encuentre dónde está el control.
- **qsaglobals.**
  Este fichero es para las funciones y clases que sí están disponibles
  globalmente en qsa, pero no lo están en Python. Por ejemplo "parseFloat" está aquí.
- **qsatype.**
  Es muy similar a qsaglobals, pero aquí dejo principalmente los constructores
  de algunas clases. Hay también constructores de controles, para que cuando desde
  QS se cree un control nuevo, podamos tener mayor control sobre lo que hará el programa.

Para colaborar, lo normal es intentar ejecutar un programa completo, ir probando
y viendo en la consola todos los mensajes que se reportan; localizar qué parte
del código qs no se está lanzando y decidir qué nuevas API implementar.

Una vez implementemos lo nuevo, debemos comprobar que se ejecuta correctamente,
al menos lo que nosotros hemos programado.

Muchas de las clases y funciones tienen triquiñuelas para evitar que de error
cuando el QS haga algo para lo que no está programado. El primero que hice es
el decorador "NotImplementedWarn", y más adelante hice el "DefFun". El primero
hay que ponerlo función a función. El segundo solo una vez por clase. La funcionalidad
de ambos es que cuando se llame a algo inexistente, lo informe por la consola,
pero que emule el método devolviendo un valor por defecto, permitiendo que el
código se ejecute más allá del error.




Cómo funciona la conversión a Python
--------------------------------------

La conversión de ficheros de QS a Python se hace en dos pasos, primero de QS a
XML y luego de XML a Python. Lo tenéis todo en la carpeta flparser.

El primer paso convierte el fichero QS en un XML. Consiste internamente en:

- **parsear.**
  Usamos para esto python-ply, lee el código, separa las distintas
  palabras claves, números, textos (esto se conoce como lexer y está en flex.py).
  Después procesamos el resultado siguiendo unos patrones. (flscriptparse.py)
  En estos patrones no se han configurado tal y como especifica el
  estándar Ecmascript, sino de un modo más comprensivo y similar a como nosotros
  programamos. El resultado es que el parser entiende mejor el sentido del programa,
  pero por contra, no parsea todos los programas que se pueden hacer en QSA.
  Hay algunos patrones de programación que no va a reconocer, pero por lo general
  suelen ser dañinos y deberíamos cambiarlos.
- **generación árbol AST.**
  AST significa "Abstract Syntax Tree" y básicamente es
  una representación de nodos donde está la información recolectada por el parser.
  Aunque el parser se intenta que sea más listo con los patrones que lee, las
  estructuras generadas en este paso siguen siendo demasiado complejas y liadas
  como para que otro programa "entienda" qué está haciendo. (flscriptparse.py)
- **simplificar el árbol.**
  Dado que el AST es aún demasiado complicado, lo que
  hacemos es aplicar unas conversiones. Cuando se detectan ciertos patrones
  repetitivos, se resumen en un solo nodo. (postparse.py)
- **guardar a XML.**
  El resultado, lo guardamos en un fichero XML. El objetivo es
  principalmente, permitir la depuración "a mano". Si algo va mal, el XML es el
  punto intermedio que nos permite saber en qué parte del programa tenemos que
  modificar. Una cosa que falta a futuro, es eliminar este paso intermedio
  (ahorrariamos CPU de grabar y leer XML, que no es poco) y dejarlo como opción
  para depurar. (postparse.py)

El segundo paso lee el XML y lo convierte en un fichero Python. Este es mucho
más sencillo que el anterior. Lo que hacemos es convertir cada nodo del xml
en un patrón de programación de Python. Cuando algo no se reconoce, hay que
agregar un nuevo patrón de programación. Algunos son más complicados o confictivos
que otros. Todo esto está controlado en el fichero pytnyzer.py.

En este último paso, me encargo de modificar lo que se escribe a Python. Por
ejemplo se introducen una serie de encabezados al inicio del fichero. También
detecto ciertas llamadas/patrones y reemplazo por otro contenido.

Un ejemplo de esto es la clase "qsa", que cuando el parser detecta llamadas a
propiedades conflictivas (por ejemplo antes era posible hacer child("x").text = "1"
y ahora hay que hacer un setText("1")) consigue detectar más o menos el tipo de
llamada que pretende y lanzar en su lugar la correcta. De ese modo el código
qsa sigue funcionando. Este problema lo hemos tenido ya en Eneboo al mejorar
su parseador (cuando lo hizo infoSial en AbanQ), y también ocurre de forma
mucho más grave cuando intentas lanzar en Qt4 el QtScript, ya que ocurre
exactamente lo mismo, lo que antes eran propiedades ahora son funciones.

Por eso, cuando veáis el código Python, algunas partes las veréis cambiadas.
Al principio tendremos que depurar cuidadosamente para estar seguros de
que estamos ejecutando lo mismo que antes.

Cómo funciona la conversión de Qt3 a Qt4
------------------------------------------

Todo empieza con la función loadUi de qt3ui.py. En ella leemos a mano el fichero,
y identificamos las conexiones a realizar, las imágenes y "el widget".

El widget, que sería alo como el widget raíz, es donde empieza lo complicado.
Dentro del widget se define todo el formulario en forma de layouts y más widgets.

La función "loadWidget" se encarga de este dilema recursivo. Tienen toda la
lógica necesaria y se llama a sí misma. La clave reside en el "for c in xml",
el cual procesa todas las ordenes del ui para este widget. Según el tipo de
etiqueta realizamos una u otra acción. Cuando encontramos otro widget, lo creamos
usando la función "createWidget" que nos busca y nos crea la clase adecuada.
A partir de aquí se llama a sí mismo para completar la carga del widget de forma
recursiva.

Lo más curioso de esta función es que traduce unas propiedades por otras
(translate_properties) y para asignarlas, busca una función setXyz para una
propiedad xyz.

De momento lo que más faena da son los FLTableDB dentro de pestañas (QTabWidget).
Dado que este control se inicializa en su construcción, por el modo en que se
construye en este caso, queda mal inicializado.
