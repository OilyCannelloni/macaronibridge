#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
TARGET_DIR="$HOME/.macaronibridge"

if [ ! -d "$TARGET_DIR" ]; then
    mkdir "$TARGET_DIR"
fi

cp -r "$SCRIPT_DIR/lib/"*.sty "$TARGET_DIR"

export TEXINPUTS="$TARGET_DIR//:$TEXINPUTS"
