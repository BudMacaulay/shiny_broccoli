import os
from operator import itemgetter

import pandas as pd
from pymatgen import Structure
from pymatgen.io.vasp.outputs import Outcar
from pymatgen.io.vasp.outputs import Vasprun

# Should be a method for me to quickly generate tables of my data and then additionally plot shit - could be cool!
# Ideal to call in conjunction with the get vasp thingy.
# TODO - catch cases with people submitting half-finished folders - as of current is should just raise a flag!!
# TODO - figure out why this thing takes a full 8years to complete - pmg parser is aids?!?
# --------------------- WORKING DIRECTORY HERE --------------------- #
workdir = input("give full path to a working directory you'd like to iterate across")

if workdir == '':
    workdir = '/Users/budmacaulay/Desktop/RESUBMIT/s104_9lay/'  # Mostly here to save my poor pasting fingers -
    # feel free to self specify/remove if you're fucking
    # around with testing/fixing

data = []  # Premake the lofl
# Iterator / / / standard stuff really
for subdir, dirs, files in os.walk(workdir):
    for file in files:
        if file.endswith('OUTCAR'):
            try:
                print(subdir.replace(workdir, ''))
                # load OUTCAR
                file_ou = Outcar(subdir + '/OUTCAR')
                # load POSCAR
                file_POS = Structure.from_file(subdir + '/POSCAR')
                # load vasprun - not sure if this is even working tbh.
                file_vr = Vasprun(subdir + '/vasprun.xml')

                # Add things to a list
                data.append([subdir.replace(workdir, ''), file_POS.composition, file_POS.composition.num_atoms,
                             file_ou.final_energy, file_ou.final_energy / file_POS.composition.num_atoms,
                             file_vr.converged])
            except:  # ignore this painful except catcher - was testing on mostly malformed XMLs and this seemed ideal
                data.append([subdir.replace(workdir, ''), file_POS.composition, file_POS.composition.num_atoms,
                             file_ou.final_energy, file_ou.final_energy / file_POS.composition.num_atoms, '!!!',
                             'FLAG RAISED'])
                print(
                    'STUPID ERROR - pymatgen doesnt like your outcar or vasprun ??? - Are all jobs complete?')  # Someone competent can fix
                # this?! (so not me) as of current it's sorta clean
                pass

# WILL NOW CLEAN UP THE RUN I/E ATTEMPT TO ALPHABETIZE THE FOLDERS
data = sorted(data, key=itemgetter(0))
TITLE = ['FOLDER NAME', 'COMPOSITION', 'NO. ATOMS', 'TOTAL ENERGY', 'ENERGY / ATOM', 'CHECK_CONV RESULT', 'FLAGS?']
data = [[TITLE], data]
data = [item for sublist in data for item in sublist]  # A goofy workaround to ensure the title is toppage

# Sending excel file to workdir - someone can change this to make it save as their desired type if they want - - -
datadf = pd.DataFrame(data)
writer = pd.ExcelWriter(workdir + '/TABSFROMRUNS.xlsx')
datadf.to_excel(writer)
writer.save()
