#!/bin/bash

ncell=99

counter=10
while [  $counter -le $ncell ]; do
    mkdir $counter
    cd $counter
    cat ../KPOINTS                            	  >  KPOINTS
    cat ../POTCAR                            	  >  POTCAR
    cat ../POSCAR-0$counter                    	  >  POSCAR-0$counter
    cp POSCAR* POSCAR
    cat ../INCAR                            	  >  INCAR
    echo "LREAL =  Auto"                     	  >> INCAR
    
    cd ../
    (( counter=$counter+1 ))
done
