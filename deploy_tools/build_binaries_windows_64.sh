#!/bin/bash
TARGET="win-64"
SYSROOT=""
LOCALDIR="$(pwd)"
SYSROOT_FOLDER="WIN-64"
QT_VERSION="5.11"
QT_RELEASE="3"
QT_SOURCE_FILE="qt-everywhere-src-$QT_VERSION.$QT_RELEASE"
TARGET="x86_64-w64-mingw32"
QT_COMPILED_FOLDER="/opt/Qt$QT_VERSION/$QT_VERSION.$QT_RELEASE/$TARGET"
CMD_MAKE="make"
#MXE_FOLDER="win64-mxe"
#MXE_TARGET="x86_64-w64-mingw32.static" #i686-w64-mingw32.static x86_64-w64-mingw32.static
#mkdir ./sysroot-$TARGET
#cp ./src/qt-everywhere-opensource-src-5.*.*.tar.xz ./sysroot-$TARGET
#cd ./sysroot-$TARGET
#tar -xf qt-everywhere-opensource-src-5.*.*.tar.xz

if [ -e "sysroots/$TARGET" ]; then
SYSROOT="--no-sysroot"
python3 ./build-pineboo-binaries.py --target $TARGET $SYSROOT --verbose
else

cd src

if [ ! -e "$QT_SOURCE_FILE" ]; then #Si no existe la carpeta
echo "INFO : Compilando Qt $QT_VERISON:"
echo "Target $QT_COMPILED_FOLDER"


if [ ! -f "$QT_SOURCE_FILE.tar.xz" ]; then #1) #Descargo el zip
echo "INFO : Descargando $QT_SOURCE_FILE.tar.xz"
wget https://download.qt.io/archive/qt/$QT_VERSION/$QT_VERSION.$QT_RELEASE/single/$QT_SOURCE_FILE.tar.xz > /dev/null
fi

echo "INFO : Extrayendo $QT_SOURCE_FILE.tar.xz"
tar -xf $QT_SOURCE_FILE.tar.xz > /dev/null
fi


cd $QT_SOURCE_FILE

PROCESSORS=$(expr  $(cat /proc/cpuinfo | grep processor | tail -n 1 | sed "s/.*:\(.*\)/\1/") + 1)
CMD_MAKE="$CMD_MAKE -k -j $PROCESSORS "

if [ -f "Makefile" ]; then #1) #Si se ha compilado previamente limpio
echo "INFO : Limpiando make previo"
make clean > /dev/null
fi
#añadir #include "/usr/$TARGET/include/windows.h" a /src/qt-everywhere-src-5.11.3/qtbase/src/corelib/global/qt_windows.h
echo "INFO : Configure ..."
./configure -xplatform win32-g++ -prefix $QT_COMPILED_FOLDER -device-option CROSS_COMPILE=$TARGET- -nomake examples -nomake tools -continue -opensource -confirm-license -static -opengl desktop -no-dbus -qt-pcre #-I /usr/$TARGET/include

echo "INFO : Make ..."

$CMD_MAKE
cd ..
echo "Ejecute make install y vuelva a ejecutar el script"

cd ..

fi

#if [ ! -e "$MXE_FOLDER" ]; then
#echo "Instalando mxe ..."
#git clone https://github.com/mxe/mxe.git ./$MXE_FOLDER
#fi
#echo "Comprobando mxe ..."
#cd $MXE_FOLDER && make MXE_TARGETS=$MXE_TARGET qt5
#cd ..
#cd ..
#TARGET_DIR=$LOCALDIR/src/$MXE_FOLDER
#export PATH=$PATH:$TARGET_DIR/usr/bin
#export PATH=$PATH:$TARGET_DIR/usr/$MXE_TARGET/include




