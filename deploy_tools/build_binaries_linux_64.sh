#!/bin/bash
TARGET="linux-64"
SYSROOT=""
FILE_SQLLITE="sqlite-autoconf-3260000"
SRC_DIR_SQLLITE="sqlite3-linux-64"
if [ -e "sysroots/$TARGET" ]; then
SYSROOT="--no-sysroot"
else
cd src
if [ ! -e $SRC_DIR_SQLLITE ] ; then
if [ ! -f $FILE_SQLLITE.tar.gz ]; then
wget https://www.sqlite.org/2018/$FILE_SQLLITE.tar.gz
fi

mkdir $SRC_DIR_SQLLITE
tar -xvzf $FILE_SQLLITE.tar.gz -C ./$SRC_DIR_SQLLITE > /dev/null
cd $SRC_DIR_SQLLITE
cd $FILE_SQLLITE
./configure --enable-static --enable-dynamic-extensions
make
cd ..
cd ..
fi

cd ..
fi
python3 ./build-pineboo-binaries.py --target $TARGET $SYSROOT 

rm ./builds/$TARGET/*.*
rm ./builds/$TARGET/Makefile
rm -Rf ./builds/$TARGET/resources


