# # # A list of useful functions in my aim to write a more consistant and understandable codebase.
# TODO - 1. - setting in the kpointit for sparce or dense, could get on that.

# TODO - 2. - setting in the qscript to be variable, and split where it puts systems, (large on ir5), small on michael

# TODO - 3. - setting in the possypot to spit an error if standard potentials dont exist - a task for smarter people

# TODO - 4. - pos2inc could use a lot of work on the overall rules and guidelines for gga, needs a dictionary (ptable)
#  level of information around magmoms e.t.c

# TODO - 5. - general failsafing in case an idiot is using a program. Would be ideal to fix this crap so if you enter
#  something ridicolous it doesnt break - a job for the more patient.

# TODO - 6. - better error handling of tabulateitall - as of current vaspruns that are dead are just sorta printed as
#  error then ignored

import os
import shutil
import datetime
import numpy as np


# bit of math used extensively in dyn2 and genacomp2 so it was easiest ot put it here.
def the_key(tol, val):
    return val // tol


# Generate a slabset - useful for convergence testing #
def slabsets(inputfile, outputdir, plane2cut, vacmin=4, vacmax=16, numberoflayers=6):
    # Plane to cut should be in pymatgen format miller planes - [A, B ,C] otherthan that it basically calls on pymatgen
    # to do the work
    import os.path

    import pymatgen
    from pymatgen.core.structure import Structure
    from pymatgen.core.surface import SlabGenerator
    from pymatgen.io.cif import CifWriter

    slices_string = ''.join(str(e) for e in plane2cut)

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

    struc = Structure.from_file(inputfile)
    for vacsize in vac:
        slabgen = SlabGenerator(struc, plane2cut, numberoflayers, vacsize, center_slab=True, in_unit_planes=True)
        all_slabs = slabgen.get_slabs()
        CIF = pymatgen.io.cif.CifWriter(all_slabs[0], symprec=1e-4)
        os.makedirs(outputdir + '/' + slices_string + 'vac' + str(vacsize), exist_ok=True)
        CIF.write_file(outputdir + '/' + slices_string + 'vac' + str(vacsize) + '.cif')
        strucs = Structure.from_file(outputdir + '/' + slices_string + 'vac' + str(vacsize) + '.cif')
        strucs.to(filename=(outputdir + '/' + slices_string + 'vac' + str(vacsize) + '/POSCAR'))


# TODO figure out how I want this to be defined, it'll be cool to rewrite subsxxx since it sucks quite a bit.
# Subs has been roughly rewritten it's cool, you should be able to call bulksub and surfsub seperately now. which is
# interesting
def supers(inputfile, outputdir, supercelldim):
    from pymatgen import Structure
    import os

    if len(supercelldim) == 3:
        obby = Structure.from_file(inputfile)
        os.makedirs(outputdir + '/sup' + str(supercelldim[0]) + str(supercelldim[1]) + str(
            supercelldim[2]), exist_ok=True)
        obby.make_supercell(supercelldim)
        obby.to(filename=(outputdir + '/sup' + str(supercelldim[0]) + str(supercelldim[1]) + str(
            supercelldim[2]) + '/POSCAR'))
    else:
        print('dimension not found fix this')
    return obby

def surfsub(inputstructure, subsfor, subswith, outputdir):
    from pymatgen.core.structure import Structure

    obby = inputstructure
    subspos = []
    for element in range(0, len(obby)):
        if obby.species[element].name == subsfor:
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
    obby[atswitch_1] = subswith
    obby[
        atswitch_2] = subswith  # Neccessary to ensure the symmetry - makes cross results annoying tho but oh well
    obby.sort()  # this is neccessary as uhm you might've took a middle thingy
    os.makedirs(outputdir + 'sup' + str(subsfor) + '4' + str(subswith) + 'surfsub', exist_ok=True)
    obby.to(filename=(outputdir + 'sup' + str(subsfor) + '4' + str(subswith) + 'surfsub/POSCAR'))


def bulksub(inputstructure, subsfor, subswith, outputdir):
    from pymatgen import Structure

    obby = inputstructure
    subspos = []
    for n__ in range(0, len(obby)):
        if obby.species[n__].name == subsfor:
            # print(userinpin + ' @ site' + str(n))
            subspos.append(n__)
    eucdis = []
    for n__ in subspos:  # array-tiest the results of which is closest to center.
        eucdis = np.append(eucdis, [np.linalg.norm(np.array(0.5) - obby.frac_coords[n__][2]), n__])

    eucdis = np.reshape(eucdis, (len(subspos), 2))  # restruc into a x2 array
    eucdis = eucdis[eucdis[:, 0].argsort()]  # order said array
    atswitch = int(eucdis[0][1])  # sets a vari to that atom cause yeah

    # Need to just subs this with the other atom which pmg should be able to do
    obby[atswitch] = subswith
    obby.sort()  # this is neccessary as uhm you might've took a middle thingy
    os.makedirs(outputdir + 'sup' + str(subsfor) + '4' + str(subswith) + 'bulksub', exist_ok=True)
    obby.to(filename=(outputdir + 'sup' + str(subsfor) + '4' + str(subswith) + 'bulksub/POSCAR'))


# Check if you want a dynamic system #
def dyna(inputfile, surfaceorbulk, layersrelaxed=3, tol=0.01):
    # TODO - This feature may be buggy - as of current the tolerance on the layers is uhhh to be said lightly. someone
    #  smarter than me can figure it out
    from pymatgen.io.vasp.inputs import Poscar
    from pymatgen import Structure

    obby = Structure.from_file(inputfile)

    if surfaceorbulk == 'surface':
        print(' okay will dyn' + layersrelaxed + ' surface layers on either side')
        subspos = []
        for n__ in range(0, len(obby)):  # pretty much cpaste from the subs stuff above
            subspos.append(n__)
        eucdis = []
        for n__ in subspos:  # array-tiest the results of which is closest to center.
            eucdis = np.append(eucdis, [np.linalg.norm(np.array(0.5) - obby.frac_coords[n__][2]), n__])

        eucdis = np.reshape(eucdis, (len(subspos), 2))  # restruc into a x2 array
        eucdis = eucdis[eucdis[:, 0].argsort()]  # make the array measure based on c distance from center
        # TODO - need to fiddle with this cause as of current the 'stepping process is fucked and may think all 1 layer
        v = 0
        k = 0
        lofleucdis = [[]]
        while v < len(eucdis[:, 1]) - 1:
            if np.isclose(eucdis[v], eucdis[v + 1], atol=tol)[0]:
                print(str(eucdis[v][0]) + ' is near ' + str(eucdis[v + 1][0]))
                lofleucdis[k].append(eucdis[v][1])
            else:
                # print(str(eucdis[v][0]) + ' is not near ' + str(eucdis[v + 1][0]))
                lofleucdis.append([])
                k += 1
            v += 1
        boolatoms = []
        booldyn = np.ones([len(obby), 3])  # Premaking the boolean input
        for elem in range(0, int(layersrelaxed) - 1):  # Takes the surface layers as defined
            boolatoms = boolatoms + lofleucdis[elem]
        for elem in boolatoms:
            booldyn[int(elem)] = [0, 0, 0]
        boollist = booldyn.tolist()  # Convert to list
        possy = Poscar(obby, selective_dynamics=boollist)  # write as poscar structure
        possy.structure.to(filename=inputfile)
    else:
        print('okay bulk system found will relax all atoms')
        booldyn = np.ones([len(obby), 3])  # makes an array of 1's
        boollist = booldyn.tolist()  # for some reason p.m.g doesnt accept np.arrays - weird!
        possy = Poscar(obby, selective_dynamics=boollist)
        possy.structure.to(filename=inputfile)
    print("your input poscar has been updated - dynamic - sorry if this isn't what you wanted </3")


# A new method of dynamising your slabs i devised a while ago. It seems quite consistent and bugfree
# TODO - add somemore testing for this thing. it'll be cool too!
def dyna2(inputfile, initiallayers, style=0):
    # TODO - think of a decent way of nonlayer symmetric surfaces (i.e those of 6 layers?)

    # Rewriting the dyna package, with intent to make it more user friendly and whatnot. Simply.
    # A style of 0 will mean all layers are relaxed (every atom is given a T value)
    # A style of 1 will (if possible give 1 layer of bulk [2 if even initiallayers]- ideal for toy systems or small systems)
    # A style of 2 will (if possible give 3 layers of bulk [4 if even initiallayers] - this is probably more than adequate)

    from pymatgen import Structure
    from pymatgen.io.vasp import Poscar
    import math
    import itertools as itt
    from functools import partial
    import numpy as np
    obby = Structure.from_file(inputfile)
    # Can skip all math if style = 0 as it'll just set all atoms to dynBool=True
    if style == 0:
        booldyn = np.ones([len(obby), 3])  # makes an array of 1's
        boollist = booldyn.tolist()  # for some reason p.m.g doesnt accept np.arrays - weird!
        possy = Poscar(obby, selective_dynamics=boollist)
        possy.structure.to(filename=inputfile)

    else:
        if initiallayers % 2 == 0:
            print('initiallayers is even')
            if style == 1:
                print('style=1 - small bulk')
                bulklay = 2
            else:
                print('style=2 - large bulk')
                bulklay = 4
        else:
            print('initiallayers is odd')
            if style == 1:
                print('style=1 - small bulk')
                bulklay = 1
            else:
                print('style=2 - large bulk')
                bulklay = 3

        c_ = []
        for element in obby:
            c_.append(element.coords[2])
        c_.sort()

        listy = []
        ranvar = 0.01
        while len(listy) != initiallayers:
            listy = [list(g) for k, g in itt.groupby(c_, partial(the_key, ranvar))]
            ranvar = ranvar * 1.01
            # print(ranvar)

        print('Assuming that system is symmetric and bulk is central!')
        relax = int((initiallayers - bulklay) / 2)
        print('relaxing ' + str(relax) + ' layer on both sides of the slab')

        # list2 = [listy[relax],listy[-relax]]
        list2 = listy[0:relax]
        flatlist2 = [item for sublist in list2 for item in sublist]
        atomrelax = len(flatlist2)

        # Make a bool of 0's and then convert first and last atom relax to 1
        booldyn = np.zeros([len(obby), 3])
        booldyn[0:atomrelax] = [1, 1, 1]
        booldyn[-atomrelax:] = [1, 1, 1]
        boollist = booldyn.tolist()  # for some reason p.m.g doesnt accept np.arrays - weird!

        # TODO Cause im dumb
        def cdim(elem):
            return elem.c

        # Sorting the structure based on c dimension
        obby.sort(key=cdim)

        # After this write it to the file as of current it's overwriting the input file but w/e i'm lazy
        possy = Poscar(obby, selective_dynamics=boollist)
        possy.structure.sort()  # Have to sort it back or potcar is gunna freak out.
        possy.structure.to(filename=inputfile)


# Iterate a 'correct' potcar over all files #
def possypot(workdir, potcardir):
    # # #
    # # #
    print('possy to potcar is running')

    for subdir, dirs, files in os.walk(str(workdir)):
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
                        with open(str(potcardir) + j + '/POTCAR') as infile:
                            for line in infile:
                                outfile.write(line)


# Iteratea a standard incar over all files #
def pos2inc(workdir, initialincarfile):
    # Need to change the current handling of these fuckers into a damn json file. As of current i'm just finding
    # parameters that are incar required and adding them by hand
    useratoms = 'Li Ni Mn Co O'.split()
    useratoms_mag = '0.0 1.0 1.0 1.0 0.0'.split()
    useratoms_ul = '-1 2 2 2 -1'.split()
    useratoms_uu = '0.00 5.90 3.90 3.32 0.00'.split()
    useratoms_uj = '0.00 0.00 0.00 0.00 0.00'.split()

    useratomstup = tuple(zip(useratoms, useratoms_mag, useratoms_ul, useratoms_uu, useratoms_uj))

    print('currently defined atoms are ' + str(useratoms) + "if you expect a different species please add it, "
                                                            "i'm working on a dict")

    for subdir, dirs, files in os.walk(workdir):
        for file in files:
            if file.endswith('POSCAR'):

                f = open(os.path.join(subdir, file))
                liz = []
                for line in f:
                    if len(liz) < 8:
                        liz.append(line)
                    else:
                        break

                with open(str(initialincarfile)) as infile:
                    inc_1 = 0
                    incar_lofl = [[]]
                    for line in infile:
                        if line == '\n':
                            incar_lofl[inc_1].append('\n')
                            incar_lofl.append([])
                            inc_1 += 1
                        else:
                            incar_lofl[inc_1].append(line)
                    incar_lofl = [x for x in incar_lofl if x != []]
                    incar_lofl = [item for sublist in incar_lofl for item in sublist if
                                  not item.startswith('!')]
                    incar_lofl = [x.strip() for x in incar_lofl]

                    varry = 0
                    while varry < len(incar_lofl):
                        if incar_lofl[varry].startswith('gen'):
                            incar_lofl[varry] = 'general: - !auto generated by BSM on ' + str(datetime.datetime.now())

                        if incar_lofl[varry].startswith('MAGMOM'):
                            # print('line ' + str(varry) + 'being updated')
                            comptup = tuple(zip(liz[5].split(), liz[6].split()))
                            incar_lofl[varry] = 'MAGMOM = '
                            for k in comptup:
                                for elem in useratomstup:
                                    if elem[0] == k[0]:
                                        incar_lofl[varry] = incar_lofl[varry] + k[1] + '*' + elem[1] + ' '
                        if incar_lofl[varry].startswith('LDAUL'):
                            # print('line ' + str(varry) + 'being updated')
                            incar_lofl[varry] = 'LDAUL = '
                            for k in comptup:
                                for elem in useratomstup:
                                    if elem[0] == k[0]:
                                        incar_lofl[varry] = incar_lofl[varry] + elem[2] + ' '
                        if incar_lofl[varry].startswith('LDAUU'):
                            # print('line ' + str(varry) + 'being updated')
                            incar_lofl[varry] = 'LDAUU = '
                            for k in comptup:
                                for elem in useratomstup:
                                    if elem[0] == k[0]:
                                        incar_lofl[varry] = incar_lofl[varry] + elem[3] + ' '
                        if incar_lofl[varry].startswith('LDAUJ'):
                            incar_lofl[varry] = 'LDAUJ = '
                            for k in comptup:
                                for elem in useratomstup:
                                    if elem[0] == k[0]:
                                        incar_lofl[varry] = incar_lofl[varry] + elem[4] + ' '
                        varry += 1
                incar_write = '\n'.join(incar_lofl)
                with open(subdir + '/INCAR', 'w') as outterfile:
                    outterfile.write(incar_write)


# Iterate a kpoint over all files #
def kpointer(workdir, kpointfile):
    for subdir, dirs, files in os.walk(workdir):
        for file in files:
            if file.endswith('POSCAR'):
                shutil.copy2(kpointfile, subdir)


# ports a qscript over all directories #
def qscript2folder(workdir, qscriptdirectory, desiredcluster='iridis5', atomspercore=1, optionalargs=None):
    import json
    from pymatgen.io.vasp import Poscar
    import math

    if optionalargs == None:
        print('no optional args - none thought of as of yet')

    f = open(qscriptdirectory + '/' + str(desiredcluster) + '.json')
    clusterstuff = json.load(f)

    print(clusterstuff['hostname'] + ' wanted')
    for subdir, dirs, files in os.walk(workdir):
        for file in files:
            if file.endswith('POSCAR'):
                print(subdir.replace(workdir, ''))  # Printing the current dir
                pos = Poscar.from_file(subdir + '/POSCAR')
                # Count no. atoms
                print(str(sum(pos.natoms)) + ' atoms in poscar')
                nodescalled = math.ceil(sum(pos.natoms) / (atomspercore * clusterstuff["corespernode"]))
                if nodescalled > clusterstuff["maxnodes"]:
                    nodescalled = clusterstuff["maxnodes"]
                infile = open(qscriptdirectory + '/' + 'qscript_' + clusterstuff["submissiontype"], 'r')
                qscript_new = [i.replace("{qs2fcorecount}", str(int(clusterstuff["corespernode"]) * nodescalled)) for i
                               in infile]
                qscript_new = [i.replace("{qs2fname}", str(subdir).split('/')[-1]) for i in qscript_new]
                qscript_str = ''.join(qscript_new)
                # Writing should be here
                with open(subdir + '/qscript', 'w') as outterfile:
                    outterfile.write(qscript_str)

    # Want to make a json with the important information for all clusters
    # Aswell as a standard qscript for said clusters.


# Tool for andrea sendvasp #
def json2folder(workdir, optionalargs=None):
    import json

    if optionalargs is None:
        print('no optional args - none thought of as of yet')

    for subdir, dirs, files in os.walk(workdir):
        for file in files:
            if file.endswith('qscript'):
                with open(subdir + '/qscript', 'r') as f:
                    jsondata = f.readlines()[1].split('-')
                if jsondata[0] == '#BUD':
                    jsonny = {'sub_cmd': jsondata[2].strip('\n'), 'hpc_fld': '~/' + subdir.split('/')[-2],
                              'hostname': jsondata[1], 'env_setup': "~/env.sh"}
                    with open(subdir + '/local.json', 'w') as outterfile:
                        json.dump(jsonny, outterfile, indent=4)
                else:
                    print('cant determine this is a BUD qscript dying poorly')


# Postprocessing stuff #
def tabluateitall(workdir):
    import os
    from operator import itemgetter

    import pandas as pd
    from pymatgen import Structure
    from pymatgen.io.vasp.outputs import Vasprun
    data = []
    for subdir, dirs, files in os.walk(workdir):
        for file in files:
            if file.endswith('OUTCAR'):
                try:
                    print(subdir.replace(workdir, ''))
                    file_pos = Structure.from_file(subdir + '/POSCAR')
                    file_vr = Vasprun(subdir + '/vasprun.xml')

                    # Add things to a list
                    data.append([subdir.replace(workdir, ''), file_pos.composition, file_pos.composition.num_atoms,
                                 file_vr.final_energy, file_vr.final_energy / file_pos.composition.num_atoms,
                                 file_vr.converged])
                except BadPotcarWarning:
                    data.append([subdir.replace(workdir, ''), file_pos.composition, file_pos.composition.num_atoms,
                                 '!!!', '!!!', 'badpotcar?',
                                 'FLAG RAISED'])
                except:
                    data.append([subdir.replace(workdir, ''), file_pos.composition, file_pos.composition.num_atoms,
                                 file_vr.final_energy, file_vr.final_energy / file_pos.composition.num_atoms, '!!!',
                                 'FLAG RAISED'])
                    print(
                        'STUPID ERROR - pymatgen doesnt like your outcar or vasprun ??? - Are all jobs complete?')
                    pass

    data = sorted(data, key=itemgetter(0))
    TITLE = ['FOLDER NAME', 'COMPOSITION', 'NO. ATOMS', 'TOTAL ENERGY', 'ENERGY / ATOM', 'CHECK_CONV RESULT', 'FLAGS?']
    data = [[TITLE], data]
    data = [item for sublist in data for item in sublist]
    datadf = pd.DataFrame(data)
    writer = pd.ExcelWriter(workdir + '/TABSFROMRUNS.xlsx')
    datadf.to_excel(writer)
    writer.save()


# Should somewhat consistantly make onetep ready .dat files. As of current it will take a supplied blank .dat file to use
# TODO - could interface thise to ask for type of job and make the starting .dat itself but effort...
# TODO - need to sync with the pt that i've written and from there import hubbard U/magmom variables - largely done...
# As of current only ldos is the variable function call. It'd be cool to see the starting dat and decide from there
# whether to include certain parameters but that's effort
# TODO - may make it read the current incar file and check the ggau values used for hte vaspruns but that seems a little overkill.

def vasp2onetep(workdir, startingdat, outputdir='0', ldos=False):
    from ase.io import read, write
    import json
    import re
    import os
    import shutil
    from pt import pt

    if outputdir == '0':
        outputdir = workdir

    os.makedirs(outputdir + '/ONETEPRUN', exist_ok=True)  # Make the directory
    for subdir, dirs, files in os.walk(workdir):
        for file in files:
            if file.endswith('POSCAR'):
                print(os.path.join(subdir))
                os.makedirs(outputdir + '/ONETEPRUN/' + subdir.replace(workdir, ''), exist_ok=True)
                # ASE - good at this shit - successfully makes an xyz - pretty nicely perhaps shudda looked at this before.
                write(outputdir + '/ONETEPRUN/' + subdir.replace(workdir, '') + '/test.xyz',
                      read(subdir + '/POSCAR'))

                incfile = open(subdir + '/INCAR', 'r') # Grabs the encut from the file. could func this with the dict.
                for line in incfile:
                    line.strip().split('/n')
                    if line.startswith('ENCUT'):
                        print('INCAR read with\n' + line)
                        encut = [int(s) for s in line.split() if s.isdigit()]

                latticeblock = ['%BLOCK LATTICE_CART\n', 'ang\n']
                for i in range(0, 3):
                    stringer = str(read(subdir + '/POSCAR').cell.T[i])  # lattice dims
                    for k in (('[', ''), (']', '')):
                        stringer = stringer.replace(*k)
                    latticeblock.append('  ' + stringer + '\n')
                latticeblock.append('%ENDBLOCK LATTICE_CART\n')

                posblock = []
                testfile = open(outputdir + '/ONETEPRUN/' + subdir.replace(workdir, '') + '/test.xyz', 'r')
                for line in testfile:
                    posblock.append(line)
                posblock.pop(0)  # remove the first two lines they're useless
                posblock.pop(0)
                speciesblock = []
                counter = 0
                while counter < len(posblock):
                    speciesblock.append(posblock[counter].split()[0])
                    counter += 1
                # turning the species list into a listset
                potlist = list(set(speciesblock))
                eleblock = ['%BLOCK SPECIES\n']  # Block species
                pottyblock = ['%BLOCK SPECIES_POT\n']
                hubbardblock = ['%BLOCK HUBBARD\n']
                ldosblock = ['%BLOCK SPECIES_LDOS_GROUPS']
                # for loop should make the speciesblock, Hubbardblock and the
                for element in potlist:
                    print(element)
                    print(
                        "using buddy pt for " + pt.get(element).get("name") + " - check your ele exists, if not add it")
                    ldosblock.append(element) # ldos line. Always made not always put in.
                    # TODO - replace line below with a join() method - im too lazy
                    eleblock.append((element + ' ') * 2 + str(pt.get(element).get("number")) + ' ' + str(
                        pt.get(element).get("ot").get("ngwf_num")) + ' ' + str(
                        pt.get(element).get("ot").get("ngwf_rad")) + '\n')
                    # TODO - find an adequate method to define cluster location of pseudos - also should discuss psuedos to use with someone
                    pottyblock.append(str(element) + ' ' + str(element) + '!Bfiddle\n')
                    if pt.get(element).get("hubbardu"):
                        # TODO - implement a method of asking for the type of u values wanted (as of current only cedar is added)
                        hubbardblock.append('{0} {1} {2} {3} {4} {5}\n'.format(str(element), str(
                            pt.get(element).get("U").get("cedar").get("Lval")), str(
                            pt.get(element).get("U").get("cedar").get("Uval")), str(
                            pt.get(element).get("U").get("cedar").get("Z")), str(
                            pt.get(element).get("U").get("cedar").get("alpha")), str(
                            pt.get(element).get("U").get("cedar").get("sigma"))))
                    else:
                        print("Hubbard U is off for this element")
                        hubbardblock.append(str(element) + ' 0 0 0 -10 0 0\n')


                pottyblock.append('%ENDBLOCK SPECIES_POT\n')
                eleblock.append('%ENDBLOCK SPECIES\n')
                hubbardblock.append('%ENDBLOCK HUBBARD\n')
                posblock = ['%BLOCK POSITIONS_ABS\n', *posblock, '%ENDBLOCK POSITIONS_ABS\n']
                ldosblock = ['%ENDBLOCK SPECIES_LDOS_GROUPS']

                dat = []
                datfile = open(startingdat, 'r')  # open starting dat.
                for line in datfile:
                    dat.append(line)
                counter = 0
                while counter < len(dat):
                    if dat[counter].startswith('cutoff_energy'):
                        dat[counter] = 'cutoff_energy : ' + str(encut[0])
                    counter += 1

                if ldos:
                    dat = [dat, '\n', ldosblock]

                newdat = [dat, '\n', eleblock, '\n', pottyblock, '\n', hubbardblock, '\n', latticeblock, '\n', posblock]
                newdat = [val for sublist in newdat for val in sublist]

                with open(outputdir + '/ONETEPRUN/' + subdir.replace(workdir, '') + '/automade.dat',
                          'w+') as outfile:
                    for element in newdat:
                        outfile.write(element)
