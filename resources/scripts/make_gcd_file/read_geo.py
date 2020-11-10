from icecube import icetray, dataclasses, dataio, icetradio
from icecube.icetradio import util_geo
import os
import numpy as np

i3file = dataio.I3File("sampleGCD.i3.gz","r")

thegeo = util_geo.get_iceantennageo(i3file)

# now, loop over the keys and the geometry objects
# this is how we will want to access them in the core of icetradio
for iceantkey, g in thegeo:
	print(iceantkey)
	print(g.position)


i3file.close()
