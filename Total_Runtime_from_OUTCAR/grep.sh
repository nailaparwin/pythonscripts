#!/bin/bash

ncell=16

counter=1
while [  $counter -le $ncell ]; do

   # mkdir $counter
    cd $counter
    #cp ../../$counter/OUTCAR .
    grep -ir "Total CPU time used (sec):" OUTCAR
    cd ../
    (( counter=$counter+1 ))
done

