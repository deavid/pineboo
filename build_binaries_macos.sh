#!/bin/bash
TARGET="macos-64"
SYSROOT=""
LOCALDIR="$(pwd)"

export CROSS='i686-apple-darwin8-'
export PATH=$PATH:/opt/mac/bin

if [ -e "sysroots/$TARGET" ]; then
SYSROOT="--no-sysroot"
else

cd src/qt-everywhere-opensource-src-5.10.1
./configure -macos


fi







python3 ./build-pineboo-binaries.py --target $TARGET $SYSROOT --verbose
#python3 ./build-demo.py --target $TARGET $SYSROOT --verbose
