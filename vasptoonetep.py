# Attempts at making a semi decent vasp to onetep thingy magik

from ase.io import read, write
import json
import re
import os
import shutil
import pt

starting_dat = '/Users/budmacaulay/Desktop/pycoderun/test.dat'  ### This will be used as the top lines
working_dir = '/Users/budmacaulay/Desktop/RESUBMIT/s104_9laymn' ### It will iterate over all poscars in this directory


os.makedirs(working_dir + '/ONETEPRUN', exist_ok=True)
for subdir, dirs, files in os.walk(working_dir):
    for file in files:
        if file.endswith('POSCAR'):
            print(os.path.join(subdir))
            os.makedirs(working_dir + '/ONETEPRUN/' + subdir.replace(working_dir, ''),exist_ok=True)
# ASE - good at this shit - successfully makes an xyz - pretty nicely perhaps shudda looked at this before.
            write(working_dir + '/ONETEPRUN/' + subdir.replace(working_dir,'') + '/test.xyz',read(subdir + '/POSCAR'))
# BLOCK for lattice here
            latticeblock = ['%BLOCK LATTICE_CART\n', 'ang\n']
            for i in range(0, 3):
                stringer = str(read(subdir + '/POSCAR').cell.T[i])  # lattice dims
                for k in (('[', ''), (']', '')):
                    stringer = stringer.replace(*k)
                latticeblock.append('  ' + stringer + '\n')
            latticeblock.append('%ENDBLOCK LATTICE_CART\n')
# BLOCK for xyz here
            posblock = []
            testfile = open(working_dir + '/ONETEPRUN/' + subdir.replace(working_dir,'') + '/test.xyz', 'r')
            for line in testfile:
                posblock.append(line)
            posblock.pop(0)  # remove the first two lines they're useless
            posblock.pop(0)
# BLOCK for species here - its inside the xyz part because its easier this way
            speciesblock = []
            counter = 0
            while counter < len(posblock):
                speciesblock.append(posblock[counter].split()[0])
                counter += 1
            # turning the species list into a listset
            potblock = list(set(speciesblock))

            counter = 0
            while counter < len(speciesblock): # A temporary method of initializing GGAU while i work on a json
                if speciesblock[counter] == 'Li':
                    speciesblock[counter] = 'Li Li 4 4 8 \n'
                if speciesblock[counter] == 'Ni':
                    speciesblock[counter] = 'Ni Ni 28 9 8 \n'
                if speciesblock[counter] == 'Co':
                    speciesblock[counter] = 'Co Co 27 9 8 \n'
                if speciesblock[counter] == 'Mn':
                    speciesblock[counter] = 'Mn Mn 25 9 8 \n'
                if speciesblock[counter] == 'O':
                    speciesblock[counter] = 'O O 8 9 8 \n'
                counter += 1
            speciesblock = ['%BLOCK SPECIES\n', *speciesblock, '%ENDBLOCK SPECIES\n']

            counter = 0
            while counter < len(posblock):
                posblock[counter] = posblock[counter][posblock[counter].find(''):]
                counter += 1
            posblock = ['%BLOCK POSITIONS_ABS\n', *posblock, 'ENDBLOCK POSITIONS_ABS\n']

# ---------------------------------------- #
        # Attempts at DFT+U #
    # Will probably be a bit difficult #
    # alpha/sigma = confusing variables #
# ---------------------------------------- #

# Snagging important info from the incar
            incfile = open(subdir + '/INCAR', 'r')
            for line in incfile:
                line.strip().split('/n')
                if line.startswith('ENCUT'):
                    print('INCAR read with\n' + line)
                    encut = [int(s) for s in line.split() if s.isdigit()]

# BLOCK PSEUDOS HERE
            counter = 0
            while counter < len(potblock):
                if potblock[counter] == 'Li':
                    potblock[counter] = 'Li  "$HOME/PSONETEP/Li.PBE-paw.abinit"'
                if potblock[counter] == 'Co':
                    potblock[counter] = 'Co "$HOME/PSONETEP/Co.PBE-paw.abinit"'
                if potblock[counter] == 'Mn':
                    potblock[counter] = 'Mn "$HOME/PSONETEP/Mn.PBE-paw.abinit"'
                if potblock[counter] == 'Ni':
                    potblock[counter] = 'Ni "$HOME/PSONETEP/Ni.PBE-paw.abinit"'
                if potblock[counter] == 'O':
                    potblock[counter] = 'O "$HOME/PSONETEP/O.PBE-paw.abinit"'
                counter += 1
            potblock = ['%BLOCK SPECIES_POT', potblock, '%ENDBLOCK SPECIES_POT']

            dat = []
            datfile = open(starting_dat, 'r')  # open starting dat.
            for line in datfile:
                dat.append(line)
            counter = 0
            while counter < len(dat):
                if dat[counter].startswith('cutoff_energy'):
                    dat[counter] = 'cutoff_energy : ' + str(encut[0])
                counter += 1

            newdat = [dat, '\n', speciesblock, '\n', latticeblock, '\n', posblock]
            newdat = [val for sublist in newdat for val in sublist]

            with open(working_dir + '/ONETEPRUN/' + subdir.replace(working_dir,'') + '/automade.dat', 'w+') as outfile:
                for element in newdat:
                    outfile.write(element)

print("If you need goofy parameters i suggest you do something else - this'll work for boring stuff fortunately")



# TODO - consider LDOS functionality etc, however this looks like it should be fairly easy to implement.

## Rewriting this function better!
os.makedirs(working_dir + '/ONETEPRUN', exist_ok=True) # Make the directory
for subdir, dirs, files in os.walk(working_dir):
    for file in files:
        if file.endswith('POSCAR'):
            print(os.path.join(subdir))
            os.makedirs(working_dir + '/ONETEPRUN/' + subdir.replace(working_dir, ''),exist_ok=True)
# ASE - good at this shit - successfully makes an xyz - pretty nicely perhaps shudda looked at this before.
            write(working_dir + '/ONETEPRUN/' + subdir.replace(working_dir,'') + '/test.xyz',read(subdir + '/POSCAR'))

            latticeblock = ['%BLOCK LATTICE_CART\n', 'ang\n']
            for i in range(0, 3):
                stringer = str(read(subdir + '/POSCAR').cell.T[i])  # lattice dims
                for k in (('[', ''), (']', '')):
                    stringer = stringer.replace(*k)
                latticeblock.append('  ' + stringer + '\n')
            latticeblock.append('%ENDBLOCK LATTICE_CART\n')

            posblock = []
            testfile = open(working_dir + '/ONETEPRUN/' + subdir.replace(working_dir,'') + '/test.xyz', 'r')
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
            eleblock = ['%BLOCK SPECIES']# Block species
            pottyblock = ['%BLOCK SPECIES_POT']
            hubbardblock = ['%BLOCK HUBBARD']
            # for loop should make the speciesblock, Hubbardblock and the
            for element in potlist:
                print(element)
                print("using buddy pt for " + pt.get(element).get("name") + " - check your ele exists, if not add it")
                # TODO - replace line below with a join() method - im too lazy
                eleblock.append((element + ' ')*2 + str(pt.get(element).get("number")) + ' ' + str(pt.get(element).get("ot").get("ngwf_num")) + ' ' + str(pt.get(element).get("ot").get("ngwf_rad"))+ '\n')
                # TODO - find an adequate method to define cluster location of pseudos - also should discuss psuedos to use with someone
                pottyblock.append(str(element) + '!Bfiddle')
                if pt.get(element).get("hubbardu"):
                    # TODO - implement a method of asking for the type of u values wanted (as of current only cedar is added)
                    hubbardblock.append('{0} {1} {2} {3} {4} {5}'.format(str(element), str(
                        pt.get(element).get("U").get("cedar").get("Lval")), str(
                        pt.get(element).get("U").get("cedar").get("Uval")), str(
                        pt.get(element).get("U").get("cedar").get("Z")), str(
                        pt.get(element).get("U").get("cedar").get("alpha")), str(
                        pt.get(element).get("U").get("cedar").get("sigma"))) + '\n')
                else:
                    print("Hubbard U is off for this element")
                    hubbardblock.append(str(element) + ' 0 0 0 -10 0 0 \n')

            pottyblock.append('%ENDBLOCK SPECIES_POT')
            eleblock.append('%ENDBLOCK SPECIES')
            hubbardblock.append('%ENDBLOCK HUBBARD')
            posblock = ['%BLOCK POSITIONS_ABS\n', *posblock, 'ENDBLOCK POSITIONS_ABS\n']

            dat = []
            datfile = open(starting_dat, 'r')  # open starting dat.
            for line in datfile:
                dat.append(line)
            counter = 0
            while counter < len(dat):
                if dat[counter].startswith('cutoff_energy'):
                    dat[counter] = 'cutoff_energy : ' + str(encut[0])
                counter += 1

            newdat = [dat, '\n', eleblock, '\n', pottyblock, '\n', hubbardblock, '\n', latticeblock, '\n', posblock]
            newdat = [val for sublist in newdat for val in sublist]

            with open(working_dir + '/ONETEPRUN/' + subdir.replace(working_dir,'') + '/automade.dat', 'w+') as outfile:
                for element in newdat:
                    outfile.write(element)
