import itertools
import json
import os

import numpy as np
from pymatgen import Structure

# Shouldnt require my shit to be a composition that seems like too much effort, as long as stio it makes sense it will
# try to
# My general hatred toward pmg means that please enter compositions as their elemental formula or I may bite a bullet.

# - - - User input stuff - - - #
# TODO Key note Maybe enter the main system first otherwise it may cry - i'll fix this. Additionally no selectivedyn pls (this seems like a pmg issue)
# TODO might be wise to make this work for multiple substitutions otherwise bitch be mad and i be crazy.
# TODO - make it ask for a directory to dump into as of current people will have to dig into it to dump it anywhere. oof

# TODO - Additionally i should functionalise these

# NOTE !!!!  - This program seems to be ridicolously ineffective for large systems. A 20 total site 50:50 split makes
# roughly 20000 files so yeah. Need to some how consider symmetry but not sure how

comppy = input('Enter a desired composition as a list of lists [["Co",4],["Mn",4]] - or a dict maybe ## - not done yet')
pfile = '/Users/budmacaulay/Desktop/RESUBMIT/s104_9lay/sup121Co4Nibulksub/POSCAR'

prepresentdefect = input('Is there already a defective site you want to fix (type its formula or its coord)')
comp = json.loads(comppy)

# - - - End the userinp  - - - #

# - - - initial stru fix - - - #

if prepresentdefect == 'No':
    prepresentdefect = 'IGNORE'
if prepresentdefect == '':
    prepresentdefect = 'IGNORE'

# - - - finish initial stuff  - - - #

# - - - Loading structure - - - #

obby = Structure.from_file(pfile)
print('initial structure stio is - ' + obby.composition.formula)
print('searching for inputted prepresent defect')

# - - - DONE LOADING - - - #

# If user inputs a list - handling - Removes the list site from original structure and stores it (adds a counter to keep
# track!)
counter = 0
if prepresentdefect.startswith('['):
    print('list object found')
    fixlist = json.loads(prepresentdefect)
    prepresentdefect = input(
        'enter the element at said sites. - please im lazy i refuse to fix this')  # Goofy too lazy to read pos.
    for frac_cord in obby.frac_coords:
        if np.array_equal(frac_cord, fixlist):
            print('found element @ ' + prepresentdefect + ', fixing its location')
            counter += 1

            # removing the site to re add it at the end of the transformation cause yeah, super genius.
            obby.remove_sites(fixlist)
    if counter == 0:
        print('no occupancy @ said site are you sure you entered the right fraccord')
        print('skipping this for now! soz loser')
# if the user inputs an element - handling - removes the elements from the site and adds one to the counter
else:  # if the user inputs a species
    it = 0
    fixlist = []
    while it < obby.species.__len__():
        if obby.species[it].name == prepresentdefect:
            print('species found @ ' + str(obby.frac_coords[it]))
            fixlist.append(obby.frac_coords[it])
            counter += 1
        it += 1
# Removing the species from the list
obby.remove_species([prepresentdefect])

# Math part - substitutions to get the correct formula,

print('desired Metal Ox formula is ' + comp[0][0] + str(comp[0][1]) + comp[1][0] + str(comp[1][1]))
rati = comp[0][1] / (comp[0][1] + comp[1][1])
print('a ' + comp[0][0] + ' to total ratio of ' + str(rati) + ' is desired')

m_1state = obby.composition[comp[0][0]]
m_2state = obby.composition[comp[1][0]] + counter

# As of current just rounding when it cant reach desired ratio so yeah make sure your ratio is possible loser.
m_1subs = round(m_1state - rati * m_1state)
print('total subs is ' + str(m_1subs))

# Looks like pmg maaay not allow direct multiple transformations, which makes sense since pmg sucks. So here goes my
# attempt
siteint = []
it = 0
while it < obby.species.__len__():
    if obby.species[it].name == comp[0][0]:
        print('species found @ ' + str(obby.frac_coords[it]))
        siteint.append([it, comp[1][0]])
    it += 1

# Need to now split this list into a numerous lists of all possible combos.
sitesall = list(itertools.combinations(siteint, m_1subs))

# Then making all of these fuckers. - need to find a good way to iterate over this dogshit stuff! Should hopefully
# iterate over
county = 0  # just a tool to label each file appriopriately :)
for subnum in sitesall:
    newsys = obby.copy()
    for totsys in subnum:  # Iterate over total number of substitutions.
        newsys.replace(totsys[0], totsys[1])

    for readd in fixlist:  # Iterating over the elements to readd.
        newsys.append(prepresentdefect, readd)

    # Save new structure as a poscar
    newsys.sort()
    os.makedirs('/Users/budmacaulay/Desktop/newtestssss/' + str(county), exist_ok=True)
    newsys.to(filename='/Users/budmacaulay/Desktop/newtestssss/' + str(county) + '/POSCAR')
    county += 1
