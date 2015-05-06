#!/bin/bash
for i in `seq 495 -1 1`;
do
    echo $i
    /cygdrive/c/Users/imana_000/Downloads/pypy-2.5.1-win32/pypy-2.5.1-win32/pypy nptsp2.py $i > /dev/null 
done  
