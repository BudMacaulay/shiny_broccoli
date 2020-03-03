import itertools
import random
from random import randint
import operator as op
from functools import reduce

comp1 = ["Co", "X"]
comp2 = ["Co", "A", "B"]
comp3 = ["Co", "A", "B", "C"]
# TRYING TO RE-REMEMBER year 10 mathematics
for _ in range(0, 25):
    lenny = randint(1, 10)
    noCo = randint(1, lenny)
    sets1 = list(itertools.product(comp1, repeat=lenny))
    sets2 = list(itertools.product(comp2, repeat=lenny))
    sets3 = list(itertools.product(comp3, repeat=lenny))

    filtsets1 = [i for i in sets1 if i.count('Co') == noCo]  # nCr (n!/r!(n-r!))
    filtsets2 = [i for i in sets2 if i.count('Co') == noCo]  # nCr (1st) * 2^(n-k)
    filtsets3 = [i for i in sets3 if i.count('Co') == noCo]  # nCr * 3^(n-k)
    if len(filtsets2) == len(filtsets1) * 2 ** (lenny - noCo):
        print('1t')
    if len(filtsets3) == len(filtsets1) * 3 ** (lenny - noCo):
        print('2t')
    if len(filtsets3) == len(filtsets3) * (len(comp3) - 1) ** (lenny - noCo):
        print('3t')

# My systems
# ratio of preferably 111 532 OR 811
comp = ["Co", "Mn", "Ni"]

noCo = 16


# sets = list(itertools.product(comp, repeat=18))
# filtsets = [i for i in sets if i.count('Mn') == 1]
# filtsets = [i for i in sets if i.count('Co') == noCo]

def ncr(n, r):
    r = min(r, n - r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer / denom
