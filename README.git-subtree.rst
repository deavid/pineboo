FLScriptParser y Git-Subtree
===================================

FLScriptParser y Pineboo son dos proyectos que comparten muchas cosas. De hecho
gran parte de la funcionalidad es gracias a esta librería. Como ambos proyectos
necesitan lo mismo, necesitamos que cuando se actualice desde un lado, aparezcan
los cambios en el otro. Por no hacer cosas dos veces.

Git Subtree es un comando que permite actualizar y enviar actualizaciones
filtrando por cierta carpeta. Es, en objetivo, muy similar a git submodules.
Pero la gran ventaja es que el resto de usuarios no va a necesitar aprender nada
de todo esto, pues lo tendrán todo integrado sin más. (Con submodules todo el
mundo tiene que saber usarlos, aunque no vayan a tocar nada de la librería)

Esta documentación está aquí principalmente para recordarme la sintaxis de pull
y push. Para el resto de usuarios, pueden hacer pull con estas instrucciones,
pero no pueden hacer push a no ser que utilicen también un fork de FLScriptParser.


Utilización
----------------

Muy sencillo, primero se agrega el remoto y se hace fetch. Aunque no tenga nada
que ver, ni coincidan carpetas. Yo utilizo "flp" como nombre de remoto.


Agregar el remoto:

$ git remote add flp git@github.com:deavid/flscriptparser.git
$ git fetch

Como ya está todo inicializado, no necesitamos nada más inicialmente.
Aparte de esto, se puede:

Actualizar nuestra versión de flscriptparser:

$ git subtree pull --prefix pineboolib/flparser/ flp master


Enviar una nueva actualización de flscriptparser:

$ git subtree push --prefix pineboolib/flparser/ flp master


La inicialización de la carpeta se hizo del siguiente modo:

$ git subtree add --prefix pineboolib/flparser/ flp master


Los comandos "pull" y "push" soportan --squash , para reducir todos los commits
en uno solo. Como tampoco hay tantas modificaciones en esta librería y también
las modificaciones se pueden considerar como "propias", he preferido quitar
el squash y ver todo el histórico.

La "pega" es que no deberían haber commits que modifiquen flparser y otra cosa
del proyecto a la vez, en el mismo commit.
