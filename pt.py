## Was considering scraping wikipedia for this information in bulk but scrapers mostly suck in python api. thereofre most
# of this donebyhand

# TODO - fill in the simple blanks, also come up with some interesting way of getting this data easily, other than that
#  it seems cool in conjunction with these systems
#  Transistion this from a dict to a class, that'll probs be better

# Added pymatgens data to this stuff as it has more detailed information. Under the index 'pmgdata' Pretty sure our
# sources are the same so overall shouldn't change much it's just an added layer of info i guess

# No U value source for Sc or Ti have been found. Mostly only inputting those from WangMaxischCedar
# DOI: 10.1103/PhysRevB.73.195107
# Plan on adding the second lit source of the Aryaes version of U values later for the user to use but that's a bit
# of a way off


import pt_Uval
import pt_ot
from pymatgen import Element

pt = {
    "H": {
        'number': 1,
        'name': 'Hydrogen',
        'symbol': 'H',
        'eneg': 2.20,
        'mass': 1.008,
        'eleconf':'1s1',
        'block': 's',
        'group':1,
        'valancecount': 1,
        'spinactive': True,
        'magord':'diamag',
        'hubbardu': False,
        'IEcount': 1,
        'IE_1': 1312.0,
        'vdw': 120,

        'ot':pt_ot.H_ot,
        'pmgdata': Element.H
    },

    "He": {
        'number': 2,
        'name': 'Helium',
        'symbol': 'He',
        'mass': 4.003,
        'eleconf':'1s2',
        'block': 's',
        'group': 18,
        'valancecount': 0,
        'spinactive': False,
        'magord':'diamag',
        'hubbardu': False,

        'vdw': 140,
        'IEcount': 2,
        'IE_1': [2372.3, 5250.5],
        'ox_com':0,
        'oxs':0,

        'ot': pt_ot.He_ot,
        'pmgdata': Element.He
    },
    "Li": {
        'number': 3,
        'name': 'Lithium',
        'symbol': 'Li',
        'eneg': 0.98,
        'mass': 6.938,
        'eleconf':'[He] 2s1',
        'block': 's',
        'group': 1,
        'valancecount': 1,
        'spinactive': True,
        'magord':'diamag',
        'hubbardu': False,

        'vdw': 182,
        'IEcount': 3,
        'IEeng': [520.5, 7298.1, 11815.0],
        'ox_com': 1,
        'oxs': [0, 1],

        'ot': pt_ot.Li_ot,
        'pmgdata': Element.Li
    },
    "Be": {
        'number': 4,
        'name': 'Beryllium',
        'symbol': 'Be',
        'eneg': 1.57,
        'mass': 9.012,
        'eleconf':'[He] 2s2',
        'block': 's',
        'group': 2,
        'valancecount': 2,
        'spinactive': False,
        'magord': 'diamag',
        'hubbardu': False,

        'vdw': 153,
        'IEcount': 3,
        'IEeng': [899.5, 1757.1, 14848.7],
        'ox_com': 2,
        'oxs': [0, 1, 2],

        'ot': pt_ot.Be_ot
    },

    "B": {
        'number': 5,
        'name': 'Boron',
        'symbol': 'B',
        'eneg': 2.04,
        'mass': 10.81,
        'eleconf': '[He] 2s2 2p1',
        'block': 'p',
        'group': 13,
        'valancecount': 3,
        'spinactive': True,
        'magord': 'diamag',
        'hubbardu': False,

        'vdw': 192,
        'IEcount': 3,
        'IEeng': [800.6, 2427.1, 3659.7],
        'ox_com': 3,
        'oxs': [-5, -1, 0, 1, 2, 3],

        'ot': pt_ot.p_ot,
        'pmgdata': Element.B
    },

    "C": {
        'number': 6,
        'name': 'Carbon',
        'symbol': 'C',
        'eneg': 2.55,
        'mass': 12.01,
        'eleconf': '[He] 2s2 2p2',
        'block': 'p',
        'group': 14,
        'valancecount': 4,
        'spinactive': False,
        'magord': 'diamag',
        'hubbardu': False,

        'vdw': 170,
        'IEcount': 3,
        'IEeng': [1086.5, 2352.6, 4620.5],
        'ox_com': [-4, 4],
        'oxs': list(range(-4,4)),

        'ot': pt_ot.p_ot,
        'pmgdata': Element.C
    },

    "N": {
        'number': 7,
        'name': 'Nitrogen',
        'symbol': 'N',
        'eneg': 3.04,
        'mass': 14.00,
        'eleconf': '[He] 2s2 2p3',
        'block': 'p',
        'group': 15,
        'valancecount': 5,
        'spinactive': False,
        'magord': 'diamag',
        'hubbardu': False,

        'vdw': 155,
        'IEcount': 3,
        'IEeng': [1402.3, 2856, 4578.1],
        'ox_com': [-3, 3, 5],
        'oxs': list(range(-3, 5)),

        'ot': pt_ot.p_ot,
        'pmgdata': Element.N
    },

    "O": {
        'number': 8,
        'name': 'Oxygen',
        'symbol': 'O',
        'eneg': 0.98,
        'mass': 15.999,
        'eleconf':'[He] 2s2 2p4',
        'block': 'p',
        'group':16,
        'valancecount': 4,
        'spinactive': True,
        'magord':'paramag',
        'hubbardu': False,

        'vdw': 152,
        'IEcount': 3,
        'IEeng': [1313.9, 3388.3, 5300.5],
        'ox_com': -2,
        'oxs': list(range(-2,2)),

        'ot': pt_ot.O_ot,
        'pmgdata': Element.O
    },

    "F": {
        'number': 9,
        'name': 'Fluorine',
        'symbol': 'F',
        'eneg': 3.98,
        'mass': 18.99,
        'eleconf': '[He] 2s2 2p5',
        'block': 'p',
        'group': 17,
        'valancecount': 7,
        'spinactive': True,
        'magord': 'paramag',
        'hubbardu': False,

        'vdw': 135,
        'IEcount': 3,
        'IEeng': [1681, 3374, 6147],
        'ox_com': -1,
        'oxs': -1,

        'ot': pt_ot.p_ot,
        'pmgdata': Element.F,
    },

    "Ne": {
        'number': 10,
        'name': 'Neon',
        'symbol': 'Ne',
        'mass': 20.18,
        'eleconf': '[He] 2s2 2p6',
        'block': 'p',
        'group': 18,
        'valancecount': 0,
        'spinactive': False,
        'magord': 'diamag',
        'hubbardu': False,

        'vdw': 154,
        'IEcount': 3,
        'IEeng': [2080.7, 3952.3, 6122],
        'ox_com': 0,
        'oxs': 0,

        'ot': pt_ot.p_ot,
        'pmgdata': Element.Ne
    },

    "Na": {
        'number': 11,
        'name': 'Sodium',
        'symbol': 'Na',
        'mass': 22.99,
        'eleconf': '[Ne] 3s1',
        'block': 's',
        'group': 1,
        'valancecount': 1,
        'spinactive': True,
        'magord': 'diamag',
        'hubbardu': False,

        'eneg': 0.93,
        'vdw': 227,
        'IEcount': 3,
        'IEeng': [495.8, 4562, 6910.3],
        'ox_com': 1,
        'oxs': [-1, 1],

        'ot': pt_ot.s_ot,
        'pmgdata': Element.Na
    },

    "Mg": {
        'number': 12,
        'name': 'Magnesium',
        'symbol': 'Mn',
        'mass': 23.30,
        'eleconf': '[Ne] 3s2',
        'block': 's',
        'group': 2,
        'valancecount': 2,
        'spinactive': True,
        'magord': 'paramag',
        'hubbardu': False,

        'eneg': 1.31,
        'vdw': 273,
        'IEcount': 2,
        'IEeng': [737.7, 1450.7],
        'ox_com': 1,
        'oxs': [-1, 1],

        'ot': pt_ot.s_ot,
        'pmgdata': Element.Mg
    },

    "Al": {
        'number': 13,
        'name': 'Aluminium',
        'symbol': 'Al',
        'mass': 26.98,
        'eleconf': '[Ne] 3s2 3p1',
        'block': 'p',
        'group': 13,
        'valancecount': 3,
        'spinactive': True,
        'magord': 'paramag',
        'hubbardu': False,

        'eneg': 1.31,
        'vdw': 184,
        'IEcount': 3,
        'IEeng': [577.5, 1816.7, 2744.8],
        'ox_com': +3,
        'oxs': [-2, -1, 1, 2, 3],

        'ot': pt_ot.p_ot,
        'pmgdata': Element.Al
    },

    "Si": {
        'number': 14,
        'name': 'Silicon',
        'symbol': 'Si',
        'mass': 28.094,
        'eleconf': '[Ne] 3s2 3p2',
        'block': 'p',
        'group': 14,
        'valancecount': 4,
        'spinactive': False,
        'magord': 'diamagnetic',
        'hubbardu': False,

        'eneg': 1.90,
        'vdw': 210,
        'IEcount': 3,
        'IEeng': [786.5, 1577.1, 3231.6],
        'ox_com': [-4,4],
        'oxs': list(range(-4, 4)),

        'ot': pt_ot.p_ot,
        'pmgdata': Element.Si
    },

    "P": {
        'number': 15,
        'name': 'Phosphourus',
        'symbol': 'P',
        'mass': 30.97,
        'eleconf': '[Ne] 3s2 3p3',
        'block': 'p',
        'group': 15,
        'valancecount': 5,
        'spinactive': True,
        'magord': 'diamagnetic',
        'hubbardu': False,

        'eneg': 2.19,
        'vdw': 180,
        'IEcount': 3,
        'IEeng': [1011.8, 1907, 2914.1],
        'ox_com': [-3, 3, 5],
        'oxs': list(range(-3, 5)),

        'ot': pt_ot.p_ot,
        'pmgdata': Element.P
    },

    "S": {
        'number': 16,
        'name': 'Sulphur',
        'symbol': 'S',
        'mass': 32.059,
        'eleconf': '[Ne] 3s2 3p4',
        'block': 'p',
        'group': 16,
        'valancecount': 6,
        'spinactive': False,
        'magord': 'diamag',
        'hubbardu': False,

        'eneg': 2.58,
        'vdw': 180,
        'IEcount': 3,
        'IEeng': [999.6, 2252, 3357],
        'ox_com': [-2, 2, 4, 6],
        'oxs': list(range(-2, 6)),

        'ot': pt_ot.p_ot,
        'pmgdata': Element.S
    },

    "Cl": {
        'number': 17,
        'name': 'Chlorine',
        'symbol': 'Cl',
        'mass': 35.446,
        'eleconf': '[Ne] 3s2 3p5',
        'block': 'p',
        'group': 17,
        'valancecount': 7,
        'spinactive': False,
        'magord': 'diamag',
        'hubbardu': False,

        'eneg': 2.58,
        'vdw': 175,
        'IEcount': 3,
        'IEeng': [1251.2, 2298, 3822],
        'ox_com': [-1, 1, 3, 5, 7],
        'oxs': [-1] + list(range(1, 7)),

        'ot': pt_ot.p_ot,
        'pmgdata': Element.Cl
    },

    "Ar": {
        'number': 18,
        'name': 'Argon',
        'symbol': 'Ar',
        'mass': 32.059,
        'eleconf': '[Ne] 3s2 3p6',
        'block': 'p',
        'group': 18,
        'valancecount': 0,
        'spinactive': False,
        'magord': 'diamag',
        'hubbardu': False,

        'vdw': 188,
        'IEcount': 3,
        'IEeng': [1520.6, 2665.8, 3931],
        'ox_com': 0,
        'oxs': 0,

        'ot': pt_ot.p_ot,
        'pmgdata': Element.Ar
    },

    "K": {
        'number': 19,
        'name': 'Potassium',
        'symbol': 'K',
        'mass': 39.098,
        'eleconf': '[Ar] 4s1',
        'block': 's',
        'group': 1,
        'valancecount': 1,
        'spinactive': True,
        'magord': 'paramag',
        'hubbardu': False,

        'eneg': 0.82,
        'vdw': 275,
        'IEcount': 3,
        'IEeng': [418.8, 3052, 4420],
        'ox_com': 1,
        'oxs': [-1, 1],

        'ot': pt_ot.s_ot,
        'pmgdata': Element.K
    },

    "Ca": {
        'number': 20,
        'name': 'Calcium',
        'symbol': 'Ca',
        'mass': 40.078,
        'eleconf': '[Ar] 4s2',
        'block': 's',
        'group': 2,
        'valancecount': 2,
        'spinactive': False,
        'magord': 'diamag',
        'hubbardu': False,

        'eneg': 1.00,
        'vdw': 231,
        'IEcount': 2,
        'IEeng': [589.8, 1145.4],
        'ox_com': 2,
        'oxs': [1, 2],

        'ot': pt_ot.s_ot,
        'pmgdata': Element.Ca
    },

    ### Important ones below - Have Uvalues so must do stuff


    "Sc": {
        'number': 21,
        'name': 'Scandium',
        'symbol': 'Sc',
        'mass': 44.956,
        'eleconf': '[Ar] 3d1 4s2',
        'block': 'd',
        'group': 3,
        'valancecount': 3,
        'spinactive': True,
        'magord': 'paramag',
        'hubbardu': False,  # Maybe something here

        'eneg': 1.36,
        'vdw': 211,
        'IEcount': 3,
        'IEeng': [633.1, 1235.0, 2388.6],
        'ox_com': 3,
        'oxs': list(range(0, 3)),

        'ot': pt_ot.d_ot,
        'pmgdata': Element.Sc
    },

    "Ti": {
        'number': 22,
        'name': 'Titanium',
        'symbol': 'Ti',
        'mass': 47.867,
        'eleconf': '[Ar] 3d2 4s2',
        'block': 'd',
        'group': 4,
        'valancecount': 4,
        'spinactive': True,
        'magord': 'paramag',
        'hubbardu': False,  # Maybe something here

        'eneg': 1.54,
        'vdw': 211,
        'IEcount': 3,
        'IEeng': [658.8, 1309.8, 2652.5],
        'ox_com': 4,
        'oxs': list(range(-2, 4)),

        'ot': pt_ot.d_ot,
        'pmgdata': Element.Ti
    },

    # Actual values here (1,2 skip a few only do my ones :). If you want to put yours in do yours. I'm lazy)
    "Mn": {
        'number': 25,
        'name': 'Manganese',
        'symbol': 'Mn',
        'eneg': 1.55,
        'mass': 54.938,
        'eleconf':'[Ar] 3d5 4s2',
        'block': 'd',
        'group': 7,
        'valancecount': 5,
        'spinactive': True,
        'magord':'paramag',
        'hubbardu': True,
        'U': pt_Uval.Mn_U,
        'vdw': 161,
        'IEcount': 3,
        'IEeng': [717.3, 1509.0, 3248],
        'ox_com': [2, 4, 7],
        'oxs': [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7],

        'ot': pt_ot.Mn_ot,
        'pmgdata': Element.Mn
    },

    "Fe": {},


    "Co": {
        'number': 27,
        'name': 'Cobalt',
        'symbol': 'Co',
        'eneg': 1.88,
        'mass': 58.933,
        'eleconf':'[Ar] 3d7 4s2',
        'block': 'd',
        'group': 9,
        'valancecount': 7,
        'spinactive': True,
        'magord':'paramag',
        'hubbardu': True,
        'U': pt_Uval.Co_U,
        'vdw': 152,
        'IEcount': 3,
        'IEeng': [760.4, 1648, 3232],
        'ox_com': [2, 3],
        'oxs': [-3, -1, 0, 1, 2, 3, 4, 5],

        'ot': pt_ot.Co_ot,
        'pmgdata': Element.Co
    },


    "Ni": {
        'number': 28,
        'name': 'Nickel',
        'symbol': 'Ni',
        'eneg': 1.91,
        'mass': 58.6934,
        'eleconf':'[Ar] 3d8 4s2',
        'block': 'd',
        'group': 10,
        'valancecount': 8,
        'spinactive': True,
        'magord':'paramag',
        'hubbardu': True,
        'U': pt_Uval.Ni_U,
        'vdw': 163,
        'IEcount': 3,
        'IEeng': [737.1, 1753, 3395],
        'ox_com': 2,
        'oxs': [-2, -1, 0, 1, 2, 3, 4],

        'ot': pt_ot.Ni_ot,
        'pmgdata': Element.Ni
    }
}
