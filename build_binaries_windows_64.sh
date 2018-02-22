#!/bin/bash
TARGET="win-64"
SYSROOT=""


#mkdir ./sysroot-$TARGET
#cp ./src/qt-everywhere-opensource-src-5.*.*.tar.xz ./sysroot-$TARGET
#cd ./sysroot-$TARGET
#tar -xf qt-everywhere-opensource-src-5.*.*.tar.xz
cd src
if [ ! -e "mxe" ]; then
echo "Instalando mxe ..."
git clone https://github.com/mxe/mxe.git ./mxe
fi
echo "Comprobando mxe ..."
cd mxe && make MXE_TARGETS=x86_64-w64-mingw32.static qt5
cd ..
cd ..

if [ -e "sysroot-$TARGET" ]; then
SYSROOT="--no-sysroot"
fi
python3 ./build-pineboo-binaries.py --target $TARGET $SYSROOT

