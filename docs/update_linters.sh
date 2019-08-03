#!/bin/bash
LINTER=$1
APP=$2
if [ "$LINTER" = "pylint" ]; then
    if test -f source/linters/pylint/static/pylint_$APP.html; then
        # If we have a cache of previous run, check if we need to update:
        if find ../pineboolib/$APP -type f -name "*.py" \
            -newer source/linters/pylint/static/pylint_$APP.html | \
            head -n1 | grep pineboolib; then
            echo "Changed files found for pineboolib.$APP."
        else
            echo "Cache for pineboolib.$APP is still valid."
            exit 0;
        fi
    fi

    (cd .. && pylint pineboolib/$APP --load-plugins=pylint_json2html --output-format=jsonextended) \
        | pylint-json2html -f jsonextended -o source/linters/pylint/static/pylint_$APP.html;
    sed -e 's|body {|#pylint { font-size: 12px;|' -e 's|<body>|<div id="pylint">|' \
        -e 's|</body>|</div>|' -i source/linters/pylint/static/pylint_$APP.html
    exit 0;
fi
PACKAGES=$( (cd ../pineboolib && find * -maxdepth 0 -type d \! -iname "_*") )
# ----
echo "Running PyLint . . ."
echo $PACKAGES | xargs -n1 -P8 $0 pylint
# ----
echo "Running MyPy . . ."
(cd .. && mypy -p pineboolib --html-report=docs/source/_static/linters/mypy)
cp source/_static/linters/mypy-html-tpl.css source/_static/linters/mypy/mypy-html.css
# ----
echo "Running Coverage . . ."
(cd .. && pytest -q --cov=pineboolib --cov-report= pineboolib/)
(cd .. && coverage html -d source/_static/linters/pytest-coverage/)
cp source/_static/linters/pytest-coverage-style-tpl.css source/_static/linters/pytest-coverage/style.css
# ----
echo "Running Bandit . . ."
(cd .. && bandit -r pineboolib/ -f html > docs/source/_static/linters/bandit/bandit_report.html) || /bin/true
# ----

exit 0
