#!/bin/bash
TARGET="linux-32"
SYSROOT=""

if [ -e "sysroots/$TARGET" ]; then
SYSROOT="--no-sysroot"
fi
python3 ./build-pineboo-binaries.py --target $TARGET $SYSROOT

