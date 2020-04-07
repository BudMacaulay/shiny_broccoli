import i_functions

# Input file should probably be below.
bulkLCO = '/Users/budmacaulay/Desktop/BULK/POSCAR'


# The desired output directory should be below.
iterwork = '/Users/budmacaulay/Desktop/iterfold'

# List of all surfaces wanting to investigate

surflist = [[1, 0, 4], [0, 0, 1]]

# List of all metals wanting to substitute.
metalsall = ['Co', 'Mn', 'Ni']

# Actual work here. # Key point to realise that both vac and layers will be in unit planes. So for certain systems you
# may have to fiddle. I/E THE 0,0,1 surface for LCO has massive unit planes. So a vacmax of 16 will result in a
# 200A vaccuum. not ideal. if you have to take it outta a for loop go ahead. Or just change the code in i_functions to
# not be in unitplanes

# TODO
#  Talk to someone about the consistant bug calling pmg that seems to consistantly do weird shit when you call a set
#  vaccuum like the 2 lines below produce completely different structures!?!

# TODO
#  Think about whether it'll be ideal to instead ask for the variables in Angstrom cause that'll deal with a lot of
#  these issues maybe? but that's a tuffie - i/e as of current trying to for loop two very different surfaces is aids.

# Expected results - a centered slab
i_functions.slabsets(bulkLCO, iterwork, surflist[0], vacmin=5, vacmax=15,numberoflayers=5)
# Unexpected - 2 slabs are generated per cell - unsure why pmg does this, but this error is egregious
#i_functions.slabsets(bulkLCO, iterwork, surflist[0], vacmin=4, vacmax=16,numberoflayers=5)

i_functions.slabsets(bulkLCO, iterwork, surflist[1], vacmin=0, vacmax=2, numberoflayers=1)

# Suggest you check your surfaces, before continuing - pmg can be finnicky, Also slabs may not be symmetric which you'll
# need to fix. Theres all sorts of ways of fixing saids things but with so many possible issues with pmg i can't be
# assed to do all this myself. (depending on what goes wrong)

# Will put all the needed files in the folder here

# Generate the neccessary files for each run.
i_functions.possypot(iterwork, potcardir = '/Users/budmacaulay/POT_GGA_PAW_PBE/') # POTCAR
i_functions.pos2inc(initialincarfile='/Users/budmacaulay/Desktop/RESUBMIT/s100_9lay/INCAR', workdir=iterwork) # INCAR
i_functions.kpointer(iterwork, kpointfile='/Users/budmacaulay/Desktop/RESUBMIT/s100_9lay/KPOINTS') # KPOINTS
i_functions.qscript2folder(iterwork,'/Users/budmacaulay/Desktop/qscriptsstuff/') # QSCRIPT
i_functions.json2folder(iterwork) # A JSON - TBU with ANDREAS THINGY

