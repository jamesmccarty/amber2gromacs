#!/bin/bash

# script to correct topology files from acpype for atoms names from amber14. 

while getopts f:o: flag 
do 
	case "${flag}" in 
	    f) gromacs_top=${OPTARG};;
	    o) outfile=${OPTARG};;
	esac 
done 
echo "Reading topology: ${gromacs_top}"
#gromacs_basename=dimer_GMX

sed 's/ 2C / CT /g' ${gromacs_top} | sed 's/ 3C / CT /g' | sed 's/ IP / Na+/' | sed 's/ IM / Cl-/' > ${outfile}  

echo "Output topology: ${outfile}"
