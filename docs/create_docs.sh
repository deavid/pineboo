#!/bin/bash

if [ "$1" = "" ]; then
    # Create folders
    (cd .. && git ls-files -- pineboolib/"*.py") | sed 's|/[^/]*$||' | sort -u | awk '{ print "source/code/" $0}' | xargs mkdir

    (cd .. && git ls-files -- pineboolib/"*.py") | sed 's|\.py||' | sed 's|/__init__$||' | sort -u | xargs -n1 $0 tpl
    (cd .. && git ls-files -- pineboolib/"*.py") | sed 's|\.py||' | sed 's|/__init__$||' | sort -u | awk '{ print "   code/" $0 }' > index_template.rst

fi

if [ "$1" = "tpl" ]; then
    # Process single file template
    PARAM2=$2
    DSTFILE="source/code/$PARAM2.rst"
    MODULE="${PARAM2////.}"
    MODNAME="${MODULE//[a-z]*./}"
    # if file exists, skip. Don't overwrite.
    # test -f "$DSTFILE" && exit 0
    echo "MOD: $MODULE  DST: $DSTFILE"
    sed -e "s|%MODULE%|$MODULE|g" -e "s|%MODNAME%|$MODNAME|g" "module_template.rst" > "$DSTFILE"


fi
