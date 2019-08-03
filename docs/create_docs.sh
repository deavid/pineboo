#!/bin/bash

if [ "$1" = "" ]; then
    test -e source/code/pineboolib && mv source/code/pineboolib source/code/old.pineboolib
    mkdir source/code/pineboolib
    # Create folders
    (cd .. && git ls-files -- pineboolib/"*.py") | sed 's|/[^/]*$||' | sort -u | awk '{ print "source/code/" $0}' | xargs mkdir

    (cd .. && git ls-files -- pineboolib/"*.py") | sed 's|\.py||' | sed 's|/__init__$|/index|' | sort -u | awk '{ print "   code/" $0 }' > index_template.rst

    (cd .. && git ls-files -- pineboolib/"*.py") | sed 's|\.py||' | sed 's|/__init__$|/index|' | sort -u | xargs -n1 $0 tpl

    test -e source/code/old.pineboolib && rm source/code/old.pineboolib -R

fi

if [ "$1" = "tpl" ]; then
    # Process single file template
    PARAM2=$2
    DSTOLDFILE="source/code/old.$PARAM2.rst"
    DSTFILE="source/code/$PARAM2.rst"
    # if file exists, skip. Don't overwrite.
    # test -f "$DSTFILE" && exit 0

    MODULE_PRE="${PARAM2////.}"
    MODNAME_PRE="${MODULE_PRE//[a-z]*./}"
    MODULE="${MODULE_PRE//.index/}"
    MODNAME="${MODULE//[a-z]*./}"
    MODPATH="${MODULE//.//}"
    TEMPLATE="module_template.rst"

    if [ "$MODNAME_PRE" == "index" ]; then
        TEMPLATE="package_template.rst"
    fi
    echo "MOD: $MODULE  DST: $DSTFILE"
    sed -e "s|%MODULE%|$MODULE|g" -e "s|%MODNAME%|$MODNAME|g" "$TEMPLATE" > "$DSTFILE"
    if [ "$MODNAME_PRE" == "index" ]; then
        echo "" >> "$DSTFILE"
        grep -E "code/$MODPATH/[^/]+(/index)?$" index_template.rst | grep "index" | grep -v "code/$MODPATH/index" | sed "s|code/$MODPATH/||" >> "$DSTFILE"
        grep -E "code/$MODPATH/[^/]+(/index)?$" index_template.rst | grep -v "index" | grep -v "code/$MODPATH/index" | sed "s|code/$MODPATH/||" >> "$DSTFILE"
    fi
    if cmp --silent "$DSTOLDFILE" "$DSTFILE"; then
        # If files have the same contents, delete new and move original
        # this serves to avoid changing the modification times, so other tools may cache.
        rm "$DSTFILE"
        mv "$DSTOLDFILE" "$DSTFILE"
    fi

fi
