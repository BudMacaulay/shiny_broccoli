import datetime
import json
import os
import shutil

import numpy as np
from pymatgen import Structure
from pymatgen.io.vasp.inputs import Poscar
from i_functions import dyna


# DONE
#  Grab user-inputted settings or a base incar/kpoints file and iterate it across all directories - key note
#  to count the atom listings and atomcounts for gga and for magmoments if it's specified - this could a cool way to
#  make INCAR making automated. (Thoughts?!) - maybe pmg has something - looks like nothing to general

# Plan - read an initial incar file - walk through all dirs/subsdirs - read said poscars, change incar to match
# importantly magmoments and U values (GGA) will need to be updated

# Should probably clean this up at some point as i'll like to be able to call teh relevant functions throughout this.


# TODO -
#  make a small change on the surfsub function such that it will readily pick the surfaces such that its both non-polar
#  but more importantly symmetry is not broken (MIGHT CAUSE ISSUES IF THEIR SURFACE IS NOT SYMMETRICAL BEFORE HAND THO)

# TODO -
#  make a change so that bulksub is picking solely based on C value and not the A or B values as often this can lead to
#  non-symmetric slabs - actually thinking about it if the cell is non-sym then doing this may cause even more issues,
#  seems a little tough to come up with an adequate solution - the solution >> ignore it GENIUS!

# Plan - maybe i could have a ask/check if the surface is initially symmetric and only then keep do the sym inversion
# however i believe this may be a bit ch00nky and even worse not neccessarily computationally cheap.


# KEYNOTE - I SHOULD LOOK AT DAMN ASE AT SOME POINT - it looks like it has most of this stuff fairly handled already...

# Before running this make sure that if you're scaling a surface that the vac is across C -
# if running on a bulk cell only choose the bulk option if substiting please otherwise i'll cry and it'll cry :(

# Keynote - I should move these to be in a decent spot outside of this file as this is mostly a superscript

def surfsub():
    subspos = []
    for element in range(0, len(obby)):
        if obby.species[element].name == userinpin:
            # print(userinpin + ' @ site' + str(n))
            subspos.append(element)
    # find the surface level
    eucdis = obby.frac_coords[subspos]
    subspos = np.array([subspos])  # Adding atom positions to this thingy
    subspos = subspos.T  # rotate this array cause yeah
    eucdis = np.append(eucdis, subspos, 1)  # Combining
    eucdis = eucdis[eucdis[:, 2].argsort()]  # Sort the rows 2 implies C

    atswitch_1 = int(eucdis[0][3])  # sets a vari to that atom cause yeah
    atswitch_2 = int(eucdis[len(eucdis) - 1][3])
    # Need to just subs this with the other atom which pmg should be able to do
    obby[atswitch_1] = userinpout
    obby[
        atswitch_2] = userinpout  # Neccessary to ensure the symmetry - makes cross results annoying tho but oh well
    obby.sort()  # this is neccessary as uhm you might've took a middle thingy
    os.makedirs(workdir + 'sup' + sup_str[i] + str(userinpin) + '4' + str(userinpout) + 'surfsub', exist_ok=True)
    obby.to(filename=(workdir + 'sup' + sup_str[i] + str(userinpin) + '4' + str(userinpout) + 'surfsub/POSCAR'))


def bulksub():
    obby = Structure.from_file(userinp1)
    obby.make_supercell(lofl[i])
    subspos = []
    for n__ in range(0, len(obby)):
        if obby.species[n__].name == userinpin:
            # print(userinpin + ' @ site' + str(n))
            subspos.append(n__)
    eucdis = []
    for n__ in subspos:  # array-tiest the results of which is closest to center.
        eucdis = np.append(eucdis, [np.linalg.norm(np.array(0.5) - obby.frac_coords[n__][2]), n__])

    eucdis = np.reshape(eucdis, (len(subspos), 2))  # restruc into a x2 array
    eucdis = eucdis[eucdis[:, 0].argsort()]  # order said array
    atswitch = int(eucdis[0][1])  # sets a vari to that atom cause yeah

    # Need to just subs this with the other atom which pmg should be able to do
    obby[atswitch] = userinpout
    obby.sort()  # this is neccessary as uhm you might've took a middle thingy
    os.makedirs(workdir + 'sup' + sup_str[i] + str(userinpin) + '4' + str(userinpout) + 'bulksub', exist_ok=True)
    obby.to(filename=(workdir + 'sup' + sup_str[i] + str(userinpin) + '4' + str(userinpout) + 'bulksub/POSCAR'))

# Decided to attempt to code this myself cause im a dipshit and uhh yeah i hate my existance tbh
# user input stuff! - loading the directory and e.t.c
userinp1 = input('The thing you want to work on cif/xyz/pos ')  # should accept pos/xyz/ etc
workdir = '/'.join(userinp1.split('/')[:-1]) + '/'  # I like ending dirs with / not sure if thats correct but w/e

# Consistancy check - if you're running through stepwise
obby = Structure.from_file(userinp1)

# dynamics stuff here!
userinpdyn = input('do you wish to make these materials to be dynamic y/n ')
if userinpdyn == 'y':
    dyna()

yninp = input('Do you desire to make a supercell of this structure y/n')

obby = Structure.from_file(userinp1)  # Reloading the new uptodate poscar

# Supercells and substits
if yninp == 'y':
    print('making supercells desired ')
    userinp2 = input('input your desired supercells as a list of lists plz [[]] - im lazy ')
    lofl = json.loads(userinp2)  # if this spits an error your shit is wrong (missing comma?)

    userinpsub = input('do you want subs y/n ')

    if userinpsub == 'y':  # more user input stuff - maybe i should've gave them less option,
        print('subs wanted')
        userinpin = input('what atom do you want to replace ')
        userinpout = input('replace with what ')
        userwhere = input('replace on surface, in bulk or both - hint if unsure pick both')

    # stupid way of converting a list of lists into a set of strings but im stupid so :)
    i = 0
    sup_str = [None] * (len(lofl))  # makes directory lvl 1
    while i < len(lofl):
        sup_str[i] = str(lofl[i]).replace('[', '')
        sup_str[i] = sup_str[i].replace(']', '')
        sup_str[i] = sup_str[i].replace(' ', '')
        sup_str[i] = sup_str[i].replace(',', '')
        #os.makedirs(workdir + 'sup' + sup_str[i], exist_ok=True)  # Makes the directories to cram shit into
        #if userinpsub == 'y':
        #    os.makedirs(workdir + 'sup' + sup_str[i] + str(userinpin) + '4' + str(userinpout) + '/',
        #                exist_ok=True)  # Makes the subs directories
        i += 1

    # Across all inputted thingies
    i = 0
    while i < len(lofl):
        obby = Structure.from_file(userinp1)
        obby.make_supercell(lofl[i])
        print('making ' + sup_str[i] + ' supercells')
        if userinpsub == 'y':  # Check if substitutions are wanted
            if userwhere == 'both':
                surfsub()
                bulksub()
            elif userwhere == 'surface':
                surfsub()
            elif userwhere == 'bulk':
                bulksub()
        else:
            obby.to(filename=(workdir + 'sup' + sup_str[i] + '/POSCAR'))
        i += 1

# else:
#    print('making newthings cells not desired - why are you using this program? - POTCAR FUNCTIONALITY I GUESS')

# potcar functionality - reads all poscar and writes potcar - in same directory coolio!
# [NOTE NO FAILSAFE FOR Nonstandard pots] - easily implementable but way too much effort
# Second NOTE - will always iterate over your crap, be careful putting your starting directory in the crap
# i should functionalise this too

for subdir, dirs, files in os.walk(workdir):
    for file in files:
        if file.endswith('POSCAR'):
            print(os.path.join(subdir, file))
            f = open(os.path.join(subdir, file))
            liz = []
            for line in f:
                if len(liz) < 8:
                    liz.append(line)
                else:
                    # print('first 8 read')
                    break
            with open(subdir + '/POTCAR', 'w') as outfile:
                for j in liz[5].split():
                    with open(  # This should be your potcar directory don't change past n
                            '/Users/budmacaulay/POT_GGA_PAW_PBE/' + j + '/POTCAR') as infile:
                        for line in infile:
                            outfile.write(line)


# as of current i can just make it copy a very basic incar with some basic parameters ( GGA OFF / MAGMOM OFF)
# Looks like the magmom is a cool lil' thing but needs ispin = 2, icharge = 1 - This works :)

# Might need a dict of gga values as otherwise it'll just be picking randomly - Uvals (Co - 3.32, Ni - 6.40, Mn - 4.00)
# Could be an interesting baseline of values - will look up some other vals


# TODO  - need to make this a function in of itself. Also maybe add a dictionary that allows people to not have to type
#  these fuckers everytime.

# BELOW HERE IS THE INCAR ITERATOR - WHICH IS VERY COOL - SHOULD FUNCTIONALISE THIS TO BE MORE USER FRIENDLY
if input('do you desire incars for all folders? y/n') == 'y':
    # uncomment if you want to self pick this
    # useratoms = input('what atoms do you expect in all folders? - type with a space inbetween').split(' ')
    # useratoms_mag = input('enter their respective  magmoms').split(' ')
    # useratoms_ul = input('enter their respective L values (orbs)').split(' ')
    # useratoms_uu = input('enter their respective U values (see cedar)').split(' ')
    # useratoms_uj = input('enter their respective J values - if in doubt 0.00 0.00 ...').split(' ')

    useratoms = 'Li Ni Mn Co O'.split()
    useratoms_mag = '0.0 1.0 1.0 1.0 0.0'.split()
    useratoms_ul = '-1 2 2 2 -1'.split()
    useratoms_uu = '0.00 5.90 3.90 3.32 0.00'.split()
    useratoms_uj = '0.00 0.00 0.00 0.00 0.00'.split()

    useratomstup = tuple(zip(useratoms, useratoms_mag, useratoms_ul, useratoms_uu, useratoms_uj))

    for subdir, dirs, files in os.walk(workdir):
        for file in files:
            if file.endswith('POSCAR'):
                # print(os.path.join(subdir, file))
                f = open(os.path.join(subdir, file))
                liz = []
                for line in f:
                    if len(liz) < 8:  # keeps files small and all params required the incar should be here
                        liz.append(line)
                    else:
                        # print('first 8 read') -
                        break

                with open('/Users/budmacaulay/Desktop/RESUBMIT/INCAR') as infile:
                    inc_1 = 0
                    incar_lofl = [[]]
                    for line in infile:
                        if line == '\n':  # Splits your incar based on the 'paragraphs' please paragraphalise ye incars!
                            incar_lofl[inc_1].append('\n')
                            incar_lofl.append([])
                            inc_1 += 1
                        else:
                            incar_lofl[inc_1].append(line)
                    incar_lofl = [x for x in incar_lofl if x != []]  # remove empty list -
                    incar_lofl = [item for sublist in incar_lofl for item in sublist if
                                  not item.startswith('!')]  # removing comment lines - this can maybe be commented out
                    incar_lofl = [x.strip() for x in incar_lofl]  # strips whitespace

                    varry = 0
                    while varry < len(incar_lofl):
                        if incar_lofl[varry].startswith('gen'):
                            incar_lofl[varry] = 'general: - !auto generated by BSM on ' + str(datetime.datetime.now())

                        if incar_lofl[varry].startswith('MAGMOM'):
                            print('line ' + str(varry) + 'being updated')
                            comptup = tuple(zip(liz[5].split(), liz[6].split()))
                            incar_lofl[varry] = 'MAGMOM = '
                            for k in comptup:
                                for elem in useratomstup:
                                    if elem[0] == k[0]:
                                        incar_lofl[varry] = incar_lofl[varry] + k[1] + '*' + elem[1] + ' '
                        if incar_lofl[varry].startswith('LDAUL'):
                            print('line ' + str(varry) + 'being updated')
                            incar_lofl[varry] = 'LDAUL = '
                            for k in comptup:
                                for elem in useratomstup:
                                    if elem[0] == k[0]:
                                        incar_lofl[varry] = incar_lofl[varry] + elem[2] + ' '
                        if incar_lofl[varry].startswith('LDAUU'):
                            print('line ' + str(varry) + 'being updated')
                            incar_lofl[varry] = 'LDAUU = '
                            for k in comptup:
                                for elem in useratomstup:
                                    if elem[0] == k[0]:
                                        incar_lofl[varry] = incar_lofl[varry] + elem[3] + ' '
                        if incar_lofl[varry].startswith('LDAUJ'):
                            # print('line ' + str(varry) + 'being updated')
                            incar_lofl[varry] = 'LDAUJ = '
                            for k in comptup:
                                for elem in useratomstup:
                                    if elem[0] == k[0]:
                                        incar_lofl[varry] = incar_lofl[varry] + elem[4] + ' '
                        varry += 1
                incar_write = '\n'.join(incar_lofl)
                # Writing should be here
                with open(subdir + '/INCAR', 'w') as outterfile:
                    outterfile.write(incar_write)

# This now works - should switch to making the general lines make sense.
# Also should probably put a !that its automatically made

# TODO - as of current i need KPOINTS + qscript IN ALL THESE FILES SO IM JUST GUNNA COPY THEM OVER ITERATIVELY could be
# interesting to have them change based on the unit size but meh - way too much math - actually not really but its fine
# will likely be doing kpoint conv anyway so whats the use!
# Add functionality to check if kpoints already exist in the folder as to not overwrite someones hard work :(


# I should add some parameters and then functionalise this so it doesnt uto run everytime - KPOIN/QSUB DRAGGER
# it could be generalised fairly nicely
for subdir, dirs, files in os.walk(workdir):
    for file in files:
        if file.endswith('POSCAR'):
            # print(os.path.join(subdir, file))
            shutil.copy2('/Users/budmacaulay/Desktop/nmc/Surface/104/LMnNiedge/KPOINTS', subdir)
            shutil.copy2('/Users/budmacaulay/Desktop/RESUBMIT/qscript', subdir)


# ignore this - its a template os.walk and write -
# filenames = ['file1.txt', 'file2.txt', ...]
# with open('path/to/output/file', 'w') as outfile:
#    for fname in filenames:
#        with open(fname) as infile:
#            for line in infile:
#                outfile.write(line)

