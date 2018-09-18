#!/bin/bash
TARGET="ios-64"
SYSROOT=""
LOCALDIR="$(pwd)"




if [ -e "sysroots/$TARGET" ]; then
SYSROOT="--no-sysroot"
else

cd src
git clone https://code.qt.io/qt/qt5.git qt5-src-ios

cd qt5-src-ios
./init-repository --module-subset=qtbase
cd ..
cd ..
#cd src
#if [ ! -e "sqlite3-ios" ] ; then
#git clone https://github.com/stockrt/sqlite3-android
#cd sqlite3-android
#make
#cd ..
#fi

#if [ ! -e "bzip2-android" ] ; then
#git clone https://github.com/dmcrystax/cosp-android-bzip2 bzip2-android
#cd bzip2-android
#build.sh $ANDROID_NDK_ROOT --prefix=./lib
#cd ..   
#fi

#cd ..
fi







python3 ./build-pineboo-binaries.py --target $TARGET $SYSROOT --verbose
#python3 ./build-demo.py --target $TARGET $SYSROOT --verbose
