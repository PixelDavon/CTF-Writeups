#!/bin/bash
NAME="$1"
mkdir -p "Writeups/$NAME"
cp TEMPLATE.md "Writeups/$NAME/README.md"
echo "Created Writeups/$NAME/README.md"