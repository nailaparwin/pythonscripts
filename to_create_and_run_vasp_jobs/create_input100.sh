#!/bin/bash

ncell=150

counter=100
while [  $counter -le $ncell ]; do
    mkdir $counter
    cd $counter
    cat ../KPOINTS                            	  >  KPOINTS
    cat ../POTCAR                            	  >  POTCAR
    cat ../POSCAR-$counter                    	  >  POSCAR-$counter
    cp POSCAR* POSCAR
    cat ../INCAR                            	  >  INCAR
    echo "LREAL =  Auto"                     	  >> INCAR
    
    cd ../
    (( counter=$counter+1 ))
done
