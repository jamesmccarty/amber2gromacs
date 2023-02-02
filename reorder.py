#!/usr/bin/env python

import sys
import os
import shutil
import re
import getopt


# Current directory
cwd = os.getcwd()

# infile = "ref_GMX.gro"
# outfile = "ref_GMX_reordered.gro"
infile = ""
outfile = ""

try:
   opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["infile=","outfile="])
except getopt.GetoptError:
   print 'reorder.py -i <inputfile> -o <outputfile>'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print 'reorder.py -i <inputfile> -o <outputfile>'
      sys.exit()
   elif opt in ("-i", "--infile"):
      infile = arg
   elif opt in ("-o", "--outfile"):
      outfile = arg
print 'Input file is "', infile
print 'Output file is "', outfile

# Open input file

filerun=os.path.join(cwd, infile)
f = open(filerun,'r')


# Extract the number of atoms

header = f.readline()
natoms_raw = f.readline()
natoms = int(natoms_raw.strip())


# Extract all atom information

atoms = {}
residues = {}
resnum = []
resname = []
atname = []
satnum = []
atnum = []
coords = []

for iatom in range(0,natoms):
    line = f.readline()
    resnum.append(line[0:5])
    resname.append(line[5:10])
    atname.append(line[10:15])
    satnum.append(line[15:20])
    atnum.append(int(satnum[iatom].strip()))
    coords.append(line[20:80])

# Extract cell information 

box = f.readline()


# BEWARE : standard list copy is by pointer, not by value
# The newlist=list(oldlist) systax is needed to copy by value

newresnum=list(resnum)
newresname=list(resname)
newatname=list(atname)
newatnum=list(atnum)
newsatnum=list(satnum)
newcoords=list(coords)


# Indexes for Na+ and Cl- need to be corrected so that they are grouped together

def update_indexes():
    newresnum[new_index]=resnum[new_index]
    newresname[new_index]=resname[old_index]
    newatname[new_index]=atname[old_index]
    newatnum[new_index]=atnum[new_index]
    newsatnum[new_index]=satnum[new_index]
    newcoords[new_index]=coords[old_index]



na_indexes = []
cl_indexes = []

for iatom in range(0,natoms):
    if resname[iatom] == "  Na+":
        na_indexes.append(iatom)
    else :
        if resname[iatom] == "  Cl-":
            cl_indexes.append(iatom)

nacl_indexes=na_indexes+cl_indexes
nacl_indexes.sort()
nacl_indexdiff=nacl_indexes[-1]-nacl_indexes[0]

if len(nacl_indexes)!= nacl_indexdiff+1:
    print "Na+ and Cl- ions are scattered at different places, cannnot continue"
    print "Na+/Cl- First index : ", nacl_indexes[0]
    print "Na+/Cl- Last-first index difference :", nacl_indexdiff
    print "Na+/Cl- list length", len(nacl_indexes)
    quit()
    

if min(na_indexes)<min(cl_indexes):
    first="Na"
else :
    first="Cl"

if first == "Na":
    firstna=min(na_indexes)
    new_na_indexes=range(min(na_indexes),min(na_indexes)+len(na_indexes))
    for i in range(0,len(na_indexes)):
        old_index=na_indexes[i]
        new_index=new_na_indexes[i]
        update_indexes()
    new_cl_indexes=range(min(na_indexes)+len(na_indexes),min(na_indexes)+len(na_indexes)+len(cl_indexes))
    for i in range(0,len(cl_indexes)):
        old_index=cl_indexes[i]
        new_index=new_cl_indexes[i]
        update_indexes()
else :
    firstcl=min(cl_indexes)
    new_cl_indexes=range(min(cl_indexes),min(cl_indexes)+len(cl_indexes))
    for i in range(0,len(cl_indexes)):
        old_index=cl_indexes[i]
        new_index=new_cl_indexes[i]
        update_indexes()
    new_na_indexes=range(min(cl_indexes)+len(cl_indexes),min(cl_indexes)+len(cl_indexes)+len(na_indexes))
    for i in range(0,len(na_indexes)):
        old_index=na_indexes[i]
        new_index=new_na_indexes[i]
        update_indexes()


# Write vthe output file

fileout=os.path.join(cwd, outfile)
f = open(fileout,'w')
f.write(header,)
f.write(natoms_raw,)
for iatom in range(0,natoms):
    f.write('%s%s%s%s%s' % (newresnum[iatom],newresname[iatom],newatname[iatom],newsatnum[iatom],newcoords[iatom] ),)
f.write(box)
f.close()

