#!/bin/bash

SOURCE_DIR="./source"
DOCS_DIR="./docs"
BUILD_DIR="./build"

mkdir -p "$DOCS_DIR"
mkdir -p "$BUILD_DIR"

convert_file() {
    local FILENAME=$1

    if [ ! -f "$SOURCE_DIR/$FILENAME.tex" ]; then
        echo "Source file $SOURCE_DIR/$FILENAME.tex not found"
        return 1
    fi

    cd "$SOURCE_DIR"
    lualatex --output-directory="../$BUILD_DIR" "$FILENAME.tex"
    cd ..

    if [ ! -f "$BUILD_DIR/$FILENAME.pdf" ]; then
        echo "lualatex failed to create PDF for $FILENAME"
        return 1
    fi

    mv "$BUILD_DIR/$FILENAME.pdf" "$DOCS_DIR/"
    echo "PDF generated: $DOCS_DIR/$FILENAME.pdf"
}

if [ "$#" -eq 1 ]; then
    FILENAME=$1
    convert_file "$FILENAME"
else
    for texfile in "$SOURCE_DIR"/*.tex; do
        FILENAME=$(basename "$texfile" .tex)
        convert_file "$FILENAME"
    done
fi
