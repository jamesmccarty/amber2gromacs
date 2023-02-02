mol new system.pdb 

set t1 1 
set t2 101 

animate read system.md.nc beg $t1 end $t2 waitfor all 0 

animate write trr trajectory_${t1}_${t2}.trr 0 

quit 
