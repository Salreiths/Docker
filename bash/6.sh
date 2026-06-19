#!/bin/bash

if [ "$FOO" = "5" ] && [ "$BAR" = "1" ]; then
    exit 1
fi

for i in $(seq 1 10); do
    if [ -f "fix.txt" ]; then
        echo "File appeared"
        exit 0
    fi
    sleep 0.1
done

exit 1


