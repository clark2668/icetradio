# python includes
import numpy as np

from icecube import icetray, dataclasses, icetradio
from icecube.dataclasses import I3Particle
from icecube.icetradio import util_geo, util_dataclasses

from NuRadioMC.SignalGen import askaryan
from NuRadioReco.utilities import units, fft
from radiotools import helper as hp
from NuRadioReco.detector import antennapattern

def fold_efields():

	print("This will eventually do efield folding")


def load_antenna_responses(antgeomap, antenna_pattern_dict):

	"""
	A function to do load the antenna responses

	Load all the response objects for every antenna in the geomap.
	Insert them as a key in the dictionary so we can call them later,


	Parameters
	----------
	antgeomap: I3IceAntennaGeometry geometry object
		a map of IceAntKeys to IceAntGeo objects
	
	antenna_model_dict: dictionary
		dictionary of 

	Returns
	-------
	void
	"""

	for iceantkey, g in antgeomap:
		
		antenna_model = g.antennaModel # get the antenna model

		if antenna_model not in antenna_pattern_dict.keys():
			# only add this antenna if it's not already in the dictt

			antenna_provider = antennapattern.AntennaPatternProvider()
			antenna_pattern = antenna_provider.load_antenna_pattern(antenna_model)
			antenna_pattern_dict[antenna_model] = antenna_pattern

