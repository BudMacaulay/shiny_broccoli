# # # A list of useful functions in my aim to write a more consistant and understandable codebase.
# # #
# # #
# # #


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
