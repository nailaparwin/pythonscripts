#!/bin/bash

ncell=9

counter=1
while [  $counter -le $ncell ]; do
    mkdir $counter
    cd $counter
    cat ../KPOINTS                            	  >  KPOINTS
    cat ../POTCAR                            	  >  POTCAR
    cat ../POSCAR-00$counter                   	  >  POSCAR-00$counter
    cp POSCAR* POSCAR
    cat ../INCAR                            	  >  INCAR
    echo "LREAL =  Auto"                     	  >> INCAR
    
    cd ../
    (( counter=$counter+1 ))
done
