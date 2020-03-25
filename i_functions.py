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


# a method for determining layers
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
def supers(inputfile, outputdir, supercelldim):
    if len(supercelldim) == 3:
        obby = Structure.from_file(userinp1)
        obby.make_supercell(supercelldim)
        obby.to(filename=(outputdir + '/sup' + str(supercelldim[0]) + str(supercelldim[1]) + str(supercelldim[2]) + '/POSCAR'))
    else:
        print('dimension not found fix this')

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

    print('currently defined atoms are ' + str(useratoms) + 'if you expect a different species please add it')

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
                            #print('line ' + str(varry) + 'being updated')
                            comptup = tuple(zip(liz[5].split(), liz[6].split()))
                            incar_lofl[varry] = 'MAGMOM = '
                            for k in comptup:
                                for elem in useratomstup:
                                    if elem[0] == k[0]:
                                        incar_lofl[varry] = incar_lofl[varry] + k[1] + '*' + elem[1] + ' '
                        if incar_lofl[varry].startswith('LDAUL'):
                            #print('line ' + str(varry) + 'being updated')
                            incar_lofl[varry] = 'LDAUL = '
                            for k in comptup:
                                for elem in useratomstup:
                                    if elem[0] == k[0]:
                                        incar_lofl[varry] = incar_lofl[varry] + elem[2] + ' '
                        if incar_lofl[varry].startswith('LDAUU'):
                            #print('line ' + str(varry) + 'being updated')
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
    from pymatgen.io.vasp.outputs import Outcar
    from pymatgen.io.vasp.outputs import Vasprun
    import time
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
