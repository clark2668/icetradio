# python includes
import numpy as np
import os

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

def load_filter_amplifier_response(amplifier_filter_model):
	"""
	A function to do load the amplifier+filter responses

	The intput should be a ASCII file
	It should be the style of the ARA filter/amps file
	https://github.com/ara-software/AraSim/blob/master/data/ARA_Electronics_TotalGain_TwoFilters.txt
	We will always skip the first three rows
	It should be a csv file, with the first column being frequency in MHz
	The second column being gain in linear units
	The third column being the phase in radians
	The files should be put in the icetradio "data" directory

	Parameters
	----------
	amplifier_filter_model: string
		name of the amplifier filter model to be used (no .txt)
	
	Returns
	-------
	antenna_model_dict: dictionary
		dictionary containing the gain and phases
	"""
	data = np.loadtxt(os.path.join(os.environ['icetradio_path'],'data',amplifier_filter_model+'.txt'), 
		skiprows=3, delimiter=',')
	response = {}
	response['frequencies'] = data[:,0]*units.MHz  #radians
	response['gain'] = data[:,1]                   #unitless
	response['phase'] = data[:, 2] * units.rad     #radians
	return response

def load_amplifier_filter_responses(antgeomap, amplifier_model_dict):
	"""
	A function to do load the amplifier/filter responses

	Load all the response objects for every amplifier in the geomap.
	Insert them as a key in the dictionary so we can call them later

	Parameters
	----------
	antgeomap: I3IceAntennaGeometry geometry object
		a map of IceAntKeys to IceAntGeo objects
	
	amplifier_model_dict: dictionary
		dictionary of amplifier+filter responses

	Returns
	-------
	void
	"""
	for iceantkey, g in antgeomap:
		
		amplifier_filter_model = g.amplifierFilterModel # get the amplifier + filter model

		if amplifier_filter_model not in amplifier_model_dict.keys():
			# only add if it's not already in the dict

			the_model = load_filter_amplifier_response(amplifier_filter_model)
			amplifier_model_dict[amplifier_filter_model] = the_model


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

