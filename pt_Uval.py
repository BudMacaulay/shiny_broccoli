### Standard Hubbard U info, it's a pain but most of this info has been scowed from the web to be put in here. If you
# see a glaring error tell me, otherwise add what you need to it.


# Important GGAU values - keynote is oneteps implementation of these suckers. It would appear that onetep sucks and have
# overqualified people working for them, as a result if you want Z values read this:
# https://www.onetep.org/pmwiki/uploads/Main/Documentation/ONETEP_DFT_U.pdf

# Looks like generally the Z and sigma values are fiddly and used if you want to break magnetic symmetry and probe your
# system therefore i've set them to -10 and 0 respectively. seems easiest.

# TODO - add other datasets of common U values as these could be important. Also some specification of U range could be
#  a cool addition but meh.
H_U = {}


Mn_U = {
    "cedar": {
        "Lval":2,
        "Uval":3.90,
        "Jval":0.00,
        "alpha":0,
        "Z": -10,
        "sigma":0
    }
}
Co_U = {
    "cedar": {
        "Lval":2,
        "Uval":3.32,
        "Jval":0.00,
        "alpha":0,
        "Z": -10,
        "sigma":0
    }
}

Ni_U = {
    "cedar": {
        "Lval":2,
        "Uval":5.40,
        "Jval":0.00,
        "alpha":0,
        "Z": -10,
        "sigma":0
    }
}