#!/bin/bash
for i in `seq 1 495`;
do
    echo $i
    ./nptsp.py $i > /dev/null
done  
