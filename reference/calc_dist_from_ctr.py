import pynbody
import numpy as np
import pandas as pd
import os
pd.set_option('display.max_column', None)
pd.set_option('display.max_rows', None)
import gc


def findBH(snap):
    BHfilter = pynbody.filt.LowPass('tform',0.0)
    BH = snap.stars[BHfilter]
    return BH

def findBHhalos(snap):
    BH = findBH(snap)
    BHhalos = BH['amiga.grp']
    return BHhalos

def getz(snap):
    return snap.properties['z']

def gettime(snap):
    return pynbody.analysis.cosmology.age(snap)

def gethalocentercoords(halo):
    center = pynbody.analysis.halo.center(halo,mode='ssc',retcen=True)
    return center

def getBHcoords(BH):
    BHcoords = BH['pos']
    return BHcoords[0]

def getBHdistance(halocoords,BHcoords):
    deltax = halocoords[0] - BHcoords[0]
    deltay = halocoords[1] - BHcoords[1]
    deltaz = halocoords[2] - BHcoords[2]
    dist = np.sqrt(deltax**2 + deltay**2 + deltaz**2)
    return dist

def halomass(halo):
    halomass = halo['mass'].sum()
    return halomass

# decide if I want to do this for many files, or just one, or.
file = 'pioneer50h243.1536gst1bwK1BH.001024'
s = pynbody.load(file)
s.physical_units()
h = s.halos()


# find the halos that have BHs
# then find the distances to the centers
BH = findBH(s)
BHhalos = findBHhalos(s)
redshift = getz(s)
print(redshift)

# we have one BH per halo, making assumptions that won't work elsewhere
for i in range(len(BHhalos)):
    thishalo = h[BHhalos[i]]
    thisBH = BH[i]
    BHcoords = getBHcoords(thisBH)
    halocoords = gethalocentercoords(thishalo)
    dist = getBHdistance(halocoords,BHcoords)
    print("Halo ",BHhalos[i], "BH is ",dist," kpc from the center")