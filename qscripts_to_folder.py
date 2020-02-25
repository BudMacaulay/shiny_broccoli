import glob
import math
import os

from pymatgen.io.vasp.inputs import Poscar

# A short script to drag a qscript across all vaspruns within a directory of directories, will set the name to the name
# of the folder as this seems easiest - if you want something different do it yourself - - -
# Note - Not sure of oneteps scaling per core so have not thought much on it tbh. Since this all should be user based it
# should be fine

# TODO - Could be cool to make it split the systems based on their size and make qsubs for michael and sbatches for
#  iridis but lots of effort - seems like a long way off though. I can just prearrange some of my folders to be big and
#  small systems :)

# TODO - could remove the import of pmgs poscar handler and instead directly read the poscar as that'll probs be fast.

# I'm lazy and refuse to think outside the box therefore - will only update qsub and sbatch really.

# - - - - - INITIAL QSCRIPTS SHOULD BE HERE I GUESS - - - - - #
# Read Example folder i guess.
qscript_dir = input('Paste a qscript directory')

if qscript_dir == '':
    qscript_dir = '/Users/budmacaulay/Desktop/qscripttest'

workdir = input('Paste a working directory to iterate over')
if workdir == '':
    workdir = '/Users/budmacaulay/Desktop/qscripttest/HELPME__/'

# Consistancy checking - how many are there
fileList = glob.glob(qscript_dir + "/qscript_*")
if len(fileList) > 1:  # more than 1 also spits an error
    print('There is more than 1 qscript file in the current directory - what manager do you want to use?')
    for i in fileList:
        print('- - - - ' + i.replace(qscript_dir + '/qscript_', ''))
    scheddy = input('type which one :)')
elif len(fileList) == 0:
    print('no qscript found dying now')
    exit()
elif len(fileList) == 1:
    print('qscript found - ' + fileList[0].replace(qscript_dir + '/qscript_', ''))
    scheddy = fileList[0].replace(qscript_dir + '/qscript_', '')

# - - - - - END DIRECTORY INITIALIZATION HERE BUDDY - - - - - #

# TODO - Maybe have a creative way of checking cores per node. As of current it'll just ask how many atoms per node is
#  wanted :) and then it'll ask how many cores there are per node - - - should be fine as long as submission is to make
#  it such that it knows 1 atom per core is decent

# - - - - - ATOMS PER NODE HERE I GUESS - - - - #

atomspernode = input('How many atoms you want per node - for iridis 40 should be great :)')
corespernode = input('How many cores per node does your thingy magick have!')
if atomspernode == '':
    atomspernode = '20'

if corespernode == '':
    corespernode = '24'

atomspercore = int(atomspernode) / int(corespernode)  # check if its near 1 ish :)

if atomspercore < 0.2:
    print(atomspercore + 'seems a little low')
elif atomspercore > 2.0:
    print(atomspercore + 'seems a little high')

maxnodes = input('whats the max nodes you want to call for these runs?')
if maxnodes == '':
    maxnodes = 4
maxnodes = int(maxnodes)

# - - - - - END ATOMS PER NODE HERE SIR - - - - #


# / / / ITERATOR / / /
qscriptlist = []
# Open the selected qscript
with open(qscript_dir + '/qscript_' + scheddy) as infile:  # should read scheduling manager preferably
    for l in infile:
        qscriptlist.append(l)
        qscriptlist = list(map(lambda s: s.strip(), qscriptlist))

    for subdir, dirs, files in os.walk(workdir):
        for file in files:
            if file.endswith('POSCAR'):
                print(subdir.replace(workdir, ''))  # Printing the current dir
                pos = Poscar.from_file(subdir + '/POSCAR')
                # Count no. atoms
                print(str(sum(pos.natoms)) + ' atoms in poscar')
                nodescalled = math.ceil(sum(pos.natoms) / int(atomspernode))
                if nodescalled > int(maxnodes):
                    nodescalled = maxnodes

                qscript_new = [
                    i.replace("{qs2fcorecount}", str(int(corespernode) * nodescalled)) for i
                    in qscriptlist]

                qscript_str = '\n'.join(qscript_new)
                # Writing should be here
                with open(subdir + '/qscript', 'w') as outterfile:
                    outterfile.write(qscript_str)
# / / / ITERATOR / / /
