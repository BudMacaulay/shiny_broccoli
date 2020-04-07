# This mini library for onetep stuff - including some ngwf info. this will be ported in from the main pt stuff but it's
# put seperately cause im lazy and this stuff is confuisng

# ONETEP HAS FORMAT; species
# needs a elenumber. symbol, and ngwf info - most of this is done except the ngwf stuff so here is that stuff below.
# It seems finnicky what ngfw you should choose so i'll fiddle with it.

#Maingroup - p orbs have 4 i guess - infact can probs set all of these to 4
H_ot = {
    "ngwf_num": 2,
    "ngwf_rad": 6.0
}

He_ot = {

}

Li_ot = {
    "ngwf_num": 4,
    "ngwf_rad": 6.0
}

Be_ot = {
    "ngwf_num": 4,
    "ngwf_rad": 6.0
}

O_ot = {
    "ngwf_num": 4,
    "ngwf_rad": 6.0
}
# Generally tms can just have these values, it might work out that you need to reduce the rad if your cells are small
Mn_ot = {
    "ngwf_num": 10,
    "ngwf_rad": 6.0
}

Co_ot = {
    "ngwf_num": 10,
    "ngwf_rad": 6.0
}

Ni_ot = {
    "ngwf_num": 10,
    "ngwf_rad": 6.0
}



# Set of potentially useful onetep ngwf values, not sure how correct they are but they should be somewhat decent. As 
# always probs need conv on these but this is just a tool to quickly make onetep inputs so it doesn't matter.

## sblock one below
s_ot = {
    "ngwf_num":4,
    "ngwf_raf":6.0
}
## pblock one below
p_ot = {
    "ngwf_num": 4,
    "ngwf_rad": 6.0
}

# dblock one below
d_ot = {
    "ngwf_num": 10,
    "ngwf_rad:": 6.0
}

# fblock one below
f_ot = {
    "ngwf_num": 18,
    "ngwf_rad:": 6.0
}
