#!/bin/bash
# Tests that all python modules under pineboolib can be imported isolated and separately.

if [ "$1" == "" ]; then
    rm tempdata/import_safety_*.log 2>/dev/null || /bin/true
    find pineboolib -type f -iname "*.py" | sed -e 's|/__init__\.py$||' -e 's|\.py||' | tr '/' '.' \
        | xargs -n1 -P8 "$0" 2>/dev/null
    EXIT_CODE="$?"
    sleep 1
    echo
    exit $EXIT_CODE;  # Return with same error code as find
fi

PINEBOO_MODULE=$1
OUTPUT_FILE="tempdata/import_safety_${PINEBOO_MODULE//[.]/_}.log"
RESULT=$(python3 -c "import $PINEBOO_MODULE" 2>&1)
EXIT_CODE="$?"
if [ "$EXIT_CODE" != "0" ]; then
    echo "Failed to import $PINEBOO_MODULE (exit code: $EXIT_CODE)" > "$OUTPUT_FILE"
    echo -ne "$RESULT" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    cat "$OUTPUT_FILE"
    exit 255
elif [[ "$RESULT" != "" ]]; then
    echo "When importing $PINEBOO_MODULE the following lines were printed:" > "$OUTPUT_FILE"
    echo -ne "$RESULT" >> "$OUTPUT_FILE"
    cat "$OUTPUT_FILE"
    exit 255
fi
