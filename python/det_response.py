# python includes
import numpy as np

from icecube import icetray, dataclasses, icetradio
from icecube.dataclasses import I3Particle
from icecube.icetradio import util_geo, util_dataclasses

from NuRadioMC.SignalGen import askaryan
from NuRadioReco.utilities import units, fft
from radiotools import helper as hp
from NuRadioReco.detector import antennapattern

def fold_efields(efield, zenith, azimuth, antenna_orientation, antenna_pattern):

	"""
	A function to do fold efields with the antenna response

	Apply the complex response of the antenna (the vector effective length)
	to an efield, and return the efield after the antenna

	Parameters
	----------
	signal: icetradio.I3EField
		the efield at the antenna

	zenith: float
		the zenith angle (in radians!) of the signal incident on the antenna

	azimuth: float
		the azimuth angle (in radians!) of the signal incident on the antenna

	antenna_orientation: array
		array of floats, specifically the orientation_theta, orientation_phi,
		rotation_theta, and rotation_phi, as they are defined in the NuRadioReco framework
		see https://nu-radio.github.io/NuRadioReco/pages/detector_database_fields.html#antenna-table
		or also the definitions in I3IceAntennaGeo
		https://code.icecube.wisc.edu/projects/icecube/browser/IceCube/sandbox/brianclark/ehe/radio/trunk/dataclasses/public/dataclasses/geometry/I3IceAntennaGeo.h 

	antenna_pattern: NuRadioReco.detector.antennapattern
		the antenna pattern for this antenna

	Returns
	-------
	trace: 
		the voltage trace that will be observed after being folded with the antenna
	"""
					
	# get the frequencies where the efield needs to be evaluated
	ff = util_dataclasses.get_frequencies_I3EField(efield)
	
	# get the fourier transforms of the field
	eR_freq = fft.time2freq(efield.eR.trace, efield.eR.samplingRate)
	eTheta_freq = fft.time2freq(efield.eTheta.trace, efield.eTheta.samplingRate)
	ePhi_freq = fft.time2freq(efield.ePhi.trace, efield.ePhi.samplingRate)

	# get the vector effective length (VEL)
	antenna_response = antenna_pattern.get_antenna_response_vectorized(ff, zenith, azimuth, *antenna_orientation)
	VEL = np.array([antenna_response['theta'], antenna_response['phi']])
	voltage_fft = np.sum(VEL * np.array([eTheta_freq, ePhi_freq]), axis=0)

	# we need to make sure to cancel out the DC offset
	voltage_fft[np.where(ff < 5 * units.MHz)] = 0.
	voltage_trace = fft.freq2time(voltage_fft, efield.eR.samplingRate)
	return voltage_trace


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

