#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: ./topdf filename (without .tex extension)"
    exit 1
fi

FILENAME=$1
SOURCE_DIR="./source"
DOCS_DIR="./docs"
BUILD_DIR="./build"

if [ ! -f "$SOURCE_DIR/$FILENAME.tex" ]; then
    echo "Source file $SOURCE_DIR/$FILENAME.tex not found"
    exit 1
fi

mkdir -p "$DOCS_DIR"
mkdir -p "$BUILD_DIR"

cd "$SOURCE_DIR"

lualatex --output-directory="../$BUILD_DIR" "$FILENAME.tex"

cd ..

if [ ! -f "$BUILD_DIR/$FILENAME.pdf" ]; then
    echo "lualatex failed to create PDF"
    exit 1
fi

mv "$BUILD_DIR/$FILENAME.pdf" "$DOCS_DIR/"

echo "PDF generated: $DOCS_DIR/$FILENAME.pdf"

