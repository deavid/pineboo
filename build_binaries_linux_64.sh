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
mkdir ./builds/$TARGET/extra_libs
mkdir ./builds/$TARGET/extra_libs/psycopg2
cp ./external_libs_deploy/lib.linux-x86_64-3.7/psycopg2/* ./builds/$TARGET/extra_libs/psycopg2


