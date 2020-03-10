# Below is a list of input parameters. Standard stuff really. Should really probs make this a callable function
# but that's effort standard if the slices var is set to general it will slice up a set of common
# planes for you, otherwise it'll take your input vac range will be such that it'll always make a 0 vac cell
# (which will functionally be the same as the standard cif just re-oriented) it'll also try its best to make
# 4 evenly spaces vaccuum sizes between vacmin and vacmax, unless  they're the same value in which it will only make 1
# the thickness is just how many atomic layers depth you want, this set to 5 if left blank maybe just put a value
# between 3 - 6 since this might not work too well

# 'The in units cells seems a bit buggy, i was under the initial impression that it would make cells with thickness in
# layers and then switch to Angs for vaccuum and my initial testing did seem to do that however it would appear that
# for certain surfaces (i.e 001) it makes cells with
# vaccuum sizes in unit planes - checked the docs and it states this is normal behaviour so perhaps vacmin/vacmax should
# be closer to 0<->5
# Looks like the symm functionality may be broken so will probs have to fix it or use lower tolerances as i believe in
# my tests 104 is sym

import glob
import os
import os.path

import pymatgen
from pymatgen.core.structure import Structure
from pymatgen.core.surface import SlabGenerator
from pymatgen.io.cif import CifWriter
from pymatgen.io.vasp import Poscar


def slabs(rutfold, slices, vacmin, vacmax, thickness):
    # The inputs i used for testing - was on a LCO system seemed to work
    rutfold = "/Users/budmacaulay/Desktop/RESUBMIT/"  # - should work as long there is only one cif file in there.

    vacmin = 15
    vacmax = 15
    thickness = 9
    slices = [[1, 0, 0], [1, 1, 0], [1, 1, 1], [2, 1, 0], [1, 0, 4]]
    # slices = 'general'
    # slices_string = ['100', '110', '001', '012', '110', '104']

    # Check if the calling directory actually has a cif present cause if not upi cant slice anything
    fileList = glob.glob(rutfold + "*.cif")
    if not len(fileList) == 1:  # more than 1 also spits an error
        print('There is either 0 or more than 1 cif file in the current directory plz fix its confusing')
    else:
        print('found cell - with name')
        print(fileList)
        struc = Structure.from_file(str(fileList[0]))

        print(struc.formula + 'is the formula of the bulk, for consistancy in stioch - need to code this in still.')
    if slices == 'general' or None:
        slices = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 2], [1, 1, 0], [1, 0, 4]]

    i = 0
    slices_string = [None] * (len(slices))
    while i < len(slices):
        slices_string[i] = str(slices[i]).replace('[', '')
        slices_string[i] = slices_string[i].replace(']', '')
        slices_string[i] = slices_string[i].replace(' ', '')
        slices_string[i] = slices_string[i].replace(',', '')
        i += 1

    if vacmax == vacmin:
        vac = []
        vac = [vacmin]
    else:
        vac = [None] * 5
        vacrange = ((vacmax - vacmin) / 3)
        vac[0] = 0
        vac[1] = round(vacmin)
        vac[2] = round(vac[1] + vacrange)
        vac[3] = round(vac[2] + vacrange)
        vac[4] = round(vacmax)

    if thickness is None:
        thickness = 5

    i = 0
    j = 0

    # Pre make the directories that i'll jam shit into
    while i < len(slices):
        os.mkdir(str(rutfold) + slices_string[i])
        i += 1

    i = 0
    while i < len(slices):
        for j in vac:
            if os.path.exists(str(rutfold) + slices_string[i] + '/vac' + str(j)):
                print('folders already exist - ')
            else:
                os.mkdir(str(rutfold) + slices_string[i] + '/vac' + str(j))
                slabgen = SlabGenerator(struc, slices[i], thickness, j, center_slab=True, in_unit_planes=True)
                all_slabs = slabgen.get_slabs()
                CIF = pymatgen.io.cif.CifWriter(all_slabs[0], symprec=1e-4)
                CIF.write_file(str(rutfold) + slices_string[i] + '/vac' + str(j) + '.cif')
                if all_slabs[0].is_symmetric(symprec=0.1):
                    print('Slab' + slices_string[i] + 'is not symmetric, likely to be a polar surface')
                else:
                    print('Slab' + slices_string[i] + 'is symmetric')
        i += 1

    i = 0
    while i < len(slices):
        for j in vac:
            if os.path.exists(str(rutfold) + slices_string[i] +'vac' + str(j) + '/POSCAR'):
                print('something something')
            else:
                strucs = Structure.from_file(str(rutfold) + slices_string[i] + '/vac' + str(j) + '.cif')
                strucs.to(filename=(str(rutfold) + slices_string[i] + '/vac' + str(j) + '/POSCAR'))
        i += 1

        # Ignore this crap - will try and make a way to spit out poscars in an ordered mode.
        # Pos = Poscar(slabgen.get_slabs())
        # Pos.write_file(rutfold + slices_string[i] + '/vac' + j + '/POSCAR')
        # l o = Str.from_file(str(rutfold) + slices_string[i] + '/vac' + str(vac[j]) + '.cif')
        # lo.to(filename=str(rutfold) + slices_string[i] + '/vac' + str(vac[j]) + '/POSCAR') #This method is heavy and currently spits out pos in atom ordered mode
