#!/bin/bash
TARGET="win-64"
SYSROOT=""
LOCALDIR="$(pwd)"
MXE_FOLDER="win64-mxe"
MXE_TARGET="i686-w64-mingw32.static" #i686-w64-mingw32.static x86_64-w64-mingw32.static
#mkdir ./sysroot-$TARGET
#cp ./src/qt-everywhere-opensource-src-5.*.*.tar.xz ./sysroot-$TARGET
#cd ./sysroot-$TARGET
#tar -xf qt-everywhere-opensource-src-5.*.*.tar.xz
cd src
if [ ! -e "$MXE_FOLDER" ]; then
echo "Instalando mxe ..."
git clone https://github.com/mxe/mxe.git ./$MXE_FOLDER
fi
echo "Comprobando mxe ..."
cd $MXE_FOLDER && make MXE_TARGETS=$MXE_TARGET qt5
cd ..
cd ..
TARGET_DIR=$LOCALDIR/src/$MXE_FOLDER
export PATH=$PATH:$TARGET_DIR/usr/bin
export PATH=$PATH:$TARGET_DIR/usr/$MXE_TARGET/include

if [ -e "sysroots/$TARGET" ]; then
SYSROOT="--no-sysroot"
fi
python3 ./build-pineboo-binaries.py --target $TARGET $SYSROOT --verbose

