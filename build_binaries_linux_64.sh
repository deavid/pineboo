#!/bin/bash
TARGET="linux-64"
SYSROOT=""


if [ -e "sysroots/$TARGET" ]; then
SYSROOT="--no-sysroot"
fi
python3 ./build-pineboo-binaries.py --target $TARGET $SYSROOT

rm ./builds/$TARGET/*.*
rm ./builds/$TARGET/Makefile
rm -Rf ./builds/$TARGET/resources


