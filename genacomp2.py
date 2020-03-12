# rewriting genacomp below
def genacomp(initialstructure, species, desired_composition):
    # step 1 - load structure and half it (allows easier symmterisation of surfaces)

    obby = Structure.from_file('C:/Users/Bud/Desktop/test/104vac11/sup121Co4Mnbulksub/POSCAR')

    species = ['Co','Mn','Ni']
    desired_composition = [1, 1, 8]
    initiallayers = 5
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

    # need to half the listy here
    flat_list = [item for sublist in listy for item in sublist]

    listy.pop(3)
    for c in flat_list:
        for k in obby:
            if c == k.coords[2]:
                print('k')
                cutstru.append(k)
                break

