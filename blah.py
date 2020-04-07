import i_functions
import os
workdir = '/Users/budmacaulay/Desktop/1tnv'
potcardir = '/Users/budmacaulay/POT_GGA_PAW_PBE/'

## Checking my function calls work!
i_functions.slabsets('/Users/budmacaulay/Desktop/BULK/POSCAR', '/Users/budmacaulay/Desktop/testing', [0, 0, 1], vacmin=4, vacmax=16, numberoflayers=2)

i_functions.possypot(workdir, potcardir)

i_functions.pos2inc(workdir, '/Users/budmacaulay/Desktop/RESUBMIT/s100_9lay/INCAR') ## This is outdatedish use the below 1
i_functions.pos2inc2(workdir, '/Users/budmacaulay/Desktop/RESUBMIT/s100_9lay/INCAR', verbose=True) # Has a full print-out option incase something goes wrong

i_functions.kpointer(workdir, '/Users/budmacaulay/Desktop/RESUBMIT/s100_9lay/KPOINTS')

for subdir, dirs, files in os.walk(str(workdir)):
    for file in files:
        if file.endswith('POSCAR'):
            i_functions.dyna(subdir + '/POSCAR', 'bulk') # This is outdated use below instead
            i_functions.dyna2(subdir + 'POSCAR', style=)

i_functions.qscript2folder(workdir,'/Users/budmacaulay/Desktop/qscriptsstuff/')

i_functions.json2folder(workdir)

i_functions.tabluateitall('/Users/budmacaulay/Desktop/newtestssss/removed')

# If you want the structure returned to you for further transformations.
suppy = i_functions.supers('/Users/budmacaulay/Desktop/nuu/POSCAR', workdir, [2, 2, 2])

# the subs function works a little different but will need a structure as an input (It was easier this way as it
# allowed to use the super function at the same time)

# i_functions.bulksub(suppy, 'Co', 'Mn', outputdir='/OUTPUT/DIR')
# i_functions.surfsub(suppy, 'species_toswap', 'swapwiththis', outputdir='/OUTPUT/DIR')

# If you need to call the subs structure without a structure input (i.e want to use a .cif pmg handles that)

# inputstructure = Structure.from_file(inputfile)
# i_functions.bulksub(inputstructure, 'Co', 'Mn', outputdir='/OUTPUT/DIR')

i_functions.vasp2onetep(workdir, '/Users/budmacaulay/Desktop/pycoderun/test.dat')


# TODO - make a onetep qscript thinggy - seems like effort tbh, as of current just porting my current one over seems
#  easier
