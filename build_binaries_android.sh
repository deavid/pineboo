#!/bin/bash
TARGET="android-32"
SYSROOT=""
LOCALDIR="$(pwd)"
export ANDROID_SDK_ROOT=$LOCALDIR/src/android-studio
export ANDROID_NDK_ROOT=$LOCALDIR/src/android-ndk-r15b
export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools
export PATH=$PATH:$ANDROID_SDK_ROOT/tools
export PATH=$PATH:$ANDROID_NDK:$ANDROID_NDK_ROOT/build
export ANDROID_NDK_PLATFORM=android-26
export ANDROID_NDK_TOOLCHAIN_VERSION=4.9
export TOOLCHAIN_PREFIX=$ANDROID_NDK_ROOT/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/arm-linux-androideabi/bin

if [ -e "sysroot-$TARGET" ]; then
SYSROOT="--no-sysroot"
fi

cd src
if [ ! -e "sqlite3-android" ] ; then
git clone https://github.com/stockrt/sqlite3-android
cd sqlite3-android
make
cd ..
fi


# Download source
if [ ! -e "cosp-android-bzip2" ] ; then
git clone https://github.com/dmcrystax/cosp-android-bzip2 bzip2-android
cd bzip2-android
build.sh $ANDROID_NDK_ROOT --prefix=./lib
cd ..   
fi


cd ..
python3 ./build-pineboo-binaries.py --target $TARGET $SYSROOT

