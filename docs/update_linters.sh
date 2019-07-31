#!/bin/bash
LINTER=$1
APP=$2
if [ "$LINTER" = "pylint" ]; then
    (cd .. && pylint3 pineboolib/$APP --load-plugins=pylint_json2html --output-format=jsonextended) \
        | pylint-json2html -f jsonextended -o source/linters/pylint/static/pylint_$APP.html;
    exit 0;
fi
PACKAGES=$( (cd ../pineboolib && find * -maxdepth 0 -type d \! -iname "_*") )
echo "Running PyLint3 . . ."
echo $PACKAGES
echo $PACKAGES | xargs -t -n1 -P4 $0 pylint
