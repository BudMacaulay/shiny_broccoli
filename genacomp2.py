import itertools as itt
import json
import os
from pymatgen import Structure
import numpy as np
from functools import partial
from i_functions import the_key
import math
from pymatgen import symmetry
from pymatgen import SymmOp
from pymatgen.core.periodic_table import Element, Specie, get_el_sp, DummySpecie
from pymatgen.core.lattice import Lattice


# This mostly looks done! - would be cool to finish the functionalisation of this and also define the things commonly used in this package (layer finder)
# As they will be quite cool!

# TODO - functionalise layer finder. Also confer with some people about whether they way i've done it is absolutely insane.
# TODO - as of current this method produced aLOT less sites for the 5 layer system as it'll also give me every possible
#  m1m2 composition for my shit.

# Provided pymatgen is consistant in making symmtetrical slabs it really shouldn't be an issue

# rewriting genacomp below
def genacomp(initialstructure, savedir, A1='Co', A2='Mn', fixspecies='Ni', initiallayers=9):
    # step 1 - load structure and half it (allows easier symmterisation of surfaces)
    # initialstructure = 'C:/Users/Bud/Desktop/test/104vac11/sup141Co4Mnsurfsub/POSCAR'
    obby = Structure.from_file(initialstructure)
    # A1 = 'Co'
    # A2 = 'Mn'
    # fixspecies = 'Ni'
    # initiallayers = 5
    cdim = []
    for element in obby:
        cdim.append(element.coords[2])
    cdim.sort()
    # TODO - Add this improved method to the dyna package. it seems to be more flexible.
    listy = []
    ranvar = 0.01
    while len(listy) != initiallayers:
        listy = [list(g) for k, g in itt.groupby(cdim, partial(the_key, ranvar))]
        ranvar = ranvar * 1.01
        print(ranvar)
    keepcount = math.ceil(initiallayers / 2)

    # need to half the listy here
    listy = listy[0:keepcount]

    flat_list = [item for sublist in listy for item in sublist]
    setter = list(set(flat_list))
    cutstru = []
    for c in setter:
        for k in obby:
            print(k)
            if c == k.coords[2]:
                print('yes')
                cutstru.append(k)

    newstruc = Structure.from_sites(cutstru)
    # now that structure has been halved-ish, it'll be ideal to count the number of sites!
    print('total number of sites = ' + str(newstruc.num_sites))

    ### Time to generate all possible combinations! - detect prepresentdefect
    counter = 0
    it = 0
    fixlist = []
    while it < newstruc.species.__len__():
        if newstruc.species[it].name == fixspecies:
            print('species found - ' + fixspecies + ' @ ' + str(newstruc.frac_coords[it]))
            fixlist.append(newstruc[it])
            counter += 1
        it += 1
    newstruc.remove_species([fixspecies])

    # find A1 and A2 total count!
    metal = 0
    it = 0
    itlist = []
    while it < newstruc.species.__len__():
        if newstruc.species[it].name == A1:
            print('species found - ' + A1 + ' @ ' + str(newstruc.frac_coords[it]))
            itlist.append(newstruc[it])
            metal += 1
        elif newstruc.species[it].name == A2:
            print('species found - ' + A1 + ' @ ' + str(newstruc.frac_coords[it]))
            itlist.append(newstruc[it])
            metal += 1
        it += 1

    print('total changable sites is ' + str(metal))
    if metal > 7:
        print("that's a lot of sites do you want to proceed")
        proceed = input('y/n')
        if proceed != 'y':
            print('good idea, your computer will have been sad')
            exit()

    # Need to now split this list into a numerous lists of all possible combos.
    # step 1, generate the pure A1 metal if it isn't already
    changestru = newstruc.copy()
    for i in itlist:
        i.species = A1
        changestru.remove(i)

    allset = list(itt.product([A1, A2], repeat=metal))
    county = 0
    for combo in allset:
        iterstru = changestru.copy()
        i = 0
        while i < len(itlist):
            itlist[i].species = combo[i]
            i += 1
        makelist = itlist + fixlist + list(changestru)
        # this is 1 half of the structure.
        savenew = Structure.from_sites(makelist)

        # making the otherside
        cdim = []
        for element in makelist:
            cdim.append(element.coords[2])
        cdim.sort()

        listy = []
        ranvar = 0.01
        while len(listy) != math.ceil(initiallayers/2):
            listy = [list(g) for k, g in itt.groupby(cdim, partial(the_key, ranvar))]
            ranvar = ranvar * 1.01
            print(ranvar)
        # need to half the listy here
        listy.pop()
        flat_list = [item for sublist in listy for item in sublist]
        setter = list(set(flat_list))
        cutstru = []
        for c in setter:
            for k in makelist:
                print(k)
                if c == k.coords[2]:
                    print('yes')
                    cutstru.append(k)
        strr = Structure.from_sites(cutstru, to_unit_cell=True)
        strr.apply_operation(SymmOp.reflection((0,0,1), origin=(strr.lattice.a/2,strr.lattice.b/2,strr.lattice.c/2)))

        newest = list(strr) + list(savenew)
        both = Structure.from_sites(newest)
        for element in both:
            if element.coords[2] < 0:
                element.coords[2] = abs(element.coords[2])
                element.frac_coords[2] = abs(element.frac_coords[2])
            if element.frac_coords[2] < 0:
                element.frac_coords[2] = abs(element.frac_coords[2])
        both.sort()
        os.makedirs(savedir + '/' + A2 + str(int(both.composition.get(A2))) + '_' + str(county),exist_ok=True)
        both.to(filename=(savedir + "/" + A2 + str(int(both.composition.get(A2))) + '_' + str(county) + '/POSCAR'))
        county += 1

# genacomp('C:/Users/Bud/Desktop/test/104vac11/sup121Co4Mnbulksub/POSCAR', 'C:/Users/Bud/Desktop/newest', A1='Co', A2='Ni', fixspecies='Mn', initiallayers=5)
# genacomp('C:/Users/Bud/Desktop/test/104vac11/sup141Co4Mnsurfsub/POSCAR', 'C:/Users/Bud/Desktop/newest2', A1='Co', A2='Ni', fixspecies='Mn', initiallayers=5)

