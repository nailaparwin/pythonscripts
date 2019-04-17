#!/bin/bash

ncell=97

counter=1
while [  $counter -le $ncell ]; do
    
    cd $counter
    cp ../job-run-gpu.sh .
    qsub job-run-gpu.sh
    
    cd ../
    (( counter=$counter+1 ))
done
