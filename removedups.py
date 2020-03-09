import itertools
import json
import os
import collections
from collections import Counter
import numpy as np
from pymatgen import Structure
from statistics import mode
import shutil

### Not sure of computer science stuff and thus therefore am unsure of how i should compare a set of numbers iteratively
## In terms of memory it seems most ideal to infact do a i and j = i+1 method or something.

# Step 1: #
## Open a folder and determine the 'cheapest' method of calculating simularities

p = Structure.from_file(filename='/Users/budmacaulay/Desktop/newtestssss/0' + '/POSCAR')
# Pretty sure it's more light weight to use dicts and such but im a terrible coder and honestly im painfully lazy

c = collections.Counter(p.species)
leastcom = []
for site in p:
    if site.specie.name == c.most_common()[-1][0].name:
        leastcom.append(site)

checkele = c.most_common()[-2][0].name

# # # - - - Checking first 100 desired sites are in correct position - - - # # #
thecount = 0
for folder in range(1, 100):
    # 1 Open poscar
    comped = Structure.from_file(filename='/Users/budmacaulay/Desktop/newtestssss/' + str(folder) + '/POSCAR')
    # 2 Check if it compares
    i = 0
    while i < len(comped):
        if comped[i].specie.name == leastcom[0].specie.name:
            # Check the coord
            if comped[i] == leastcom[0]:
                print('same')
            else:
                print('not same co-ord')
                thecount += 1
        i += 1
if thecount > 0:
    print('something probably went wrong - desired site is not in same position for all thingy magicks')

# # # - - - DONE CHECKING SITES - - - # # #

# # # - - - FULL ITERATION OVER ALL SITES - - - # # #
# Do the same process as above but instead of just saying same is good, need to say instead same is BAD and remove them
# from the file
# TODO - since i need to run it over all the possible whackity tobackity i need to find a good way of saying
#  i ->> ->> where are the thingies j ->> are they same place? ->> NO???. okay not same!!!

# TODO - Fix it such that it doesnt remove similar sites, should instead see if i can map all A(sites) onto B(sites)
#  Seems way too much effort.
# Figure out how to iter - over while running

i = 0
j = 1
folderlist2 = list(range(0, 679))  ### Length of the whacky backy folders.
while i < folder - 1:
    disties = []
    istruc = Structure.from_file(filename='/Users/budmacaulay/Desktop/newtestssss/' + str(i) + '/POSCAR')
    for element in istruc:
        if element.specie.name == checkele:
            disties.append(np.linalg.norm(np.array([0.5, 0.5, 0.5]) - element.frac_coords))  # Not strictly true
    while j < folder:
        testies = []
        jstruc = Structure.from_file(filename='/Users/budmacaulay/Desktop/newtestssss/' + str(j) + '/POSCAR')
        for element in jstruc:
            if element.specie.name == checkele:
                testies.append(np.linalg.norm(np.array([0.5, 0.5, 0.5]) - element.frac_coords))
        if testies == disties:
            print(str(j) + ' and ' + str(i) + ' are related!')
            try:
                folderlist2.remove(j)
            except ValueError:
                pass  # do nothing!
        j += 1
    i += 1
    j = i + 1

# Rewrite below;
# OVer counting massively with current methods, perhaps it'll be more ideal to instead break upon find a single match!
# Removing the current i value from the list.

# Will give that a go below!
# TODO - DO THIS writen above
######### --- THis looks like a much faster method than that prior.
i = 0
j = 1
folderlistnew = list(range(0, 679))  ### Length of the whacky backy folders.
while i < folder - 1:
    disties = []
    istruc = Structure.from_file(filename='/Users/budmacaulay/Desktop/newtestssss/' + str(i) + '/POSCAR')
    for element in istruc:
        if element.specie.name == checkele:
            disties.append(np.linalg.norm(np.array([0.5, 0.5, 0.5]) - element.frac_coords))  # Not strictly true
    while j < folder:
        testies = []
        jstruc = Structure.from_file(filename='/Users/budmacaulay/Desktop/newtestssss/' + str(j) + '/POSCAR')
        for element in jstruc:
            if element.specie.name == checkele:
                testies.append(np.linalg.norm(np.array([0.5, 0.5, 0.5]) - element.frac_coords))
        if testies == disties:
            print(str(j) + ' and ' + str(i) + ' are related!')
            try:
                folderlistnew.remove(i)
            except ValueError:
                pass
            break

        j += 1
    i += 1
    j = i + 1

# # # - - - DONE COMPARING SHIT - - - # # #

# Once done it is probs ideal to move said shit into a damn new folder, that way you wont overwrite important shit
# from here you can use any of the tools to move a json, qscript, kpoints potcar and incar into the directories.
# Should be pretty cool!

os.makedirs('/Users/budmacaulay/Desktop/newtestssss/removed', exist_ok=True)
for folder in folderlistnew:
    os.makedirs('/Users/budmacaulay/Desktop/newtestssss/removed/' + str(folder), exist_ok=True)
    shutil.copy2('/Users/budmacaulay/Desktop/newtestssss/' + str(folder) + '/POSCAR', '/Users/budmacaulay/Desktop'
                                                                                      '/newtestssss/removed/' + str(
        folder))
