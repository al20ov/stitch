#!/bin/sh

blueprint-compiler batch-compile src/ src/ src/*.blp
python3 src/main.py
