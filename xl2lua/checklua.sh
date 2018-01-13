#!/bin/sh
SHELL_DIR=$(cd "$(dirname "$0")"; pwd)
echo "checking $SHELL_DIR/../luanew/*.lua"
for file in $SHELL_DIR/../luanew/*.lua
do
    if test -f $file
    then
        lua $file
    fi
    if test -d $file
    then
        echo $file 是目录
    fi
done