#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "Error: directory does not exist"
    exit 1
fi

for dir in "$1"/*/; do
    if [ -d "$dir" ]; then
        name=$(basename "$dir")
        count=$(ls -1 "$dir" | wc -l)
        echo "$count" > "$name"
    fi
done


