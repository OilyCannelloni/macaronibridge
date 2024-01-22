#!/bin/bash

TARGET_DIR="$HOME/.macaronibridge"

if [ ! -d "$TARGET_DIR" ]; then
    mkdir "$TARGET_DIR"
fi

cp -r ./lib/*.sty "$TARGET_DIR"

export TEXINPUTS="$TARGET_DIR//:$TEXINPUTS"
