# amber2gromacs
Files for converting between Amber and GROMACS

Scripts to convert amber generated topology and coordites to GROMACS format.

Files included in this directory:

reorder.py   - python script to reorder Na+ and Cl- (if needed) </br> 
correct_amber.sh - script to rename atoms that are named incorrectly for Amber14FF </br>
dimer_solv.inpcrd - example amber generated coordinate file </br>
dimer_solv.prmtop - example amber generated topology file </br>
write_trr.tcl  - tcl script to convert amber trajectory into GROMACS trr format </br> 

Procedure:

acpype -p dimer_solv.prmtop -x dimer_solv.inpcrd -b dimer </br>

bash correct_amber.sh -f dimer_GMX.top -o dimer_GMX_corr.top </br>

python reorder.py -i dimer_GMX.gro -o dimer_GMX_reorder.gro </br>


