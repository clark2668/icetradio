# python includes
import numpy as np

# icecube includes
from icecube import icetray, dataclasses, icetradio
from icecube.dataclasses import I3Particle
from icecube.icetradio import util_dataclasses, util_geo, util_phys, signal_prop, signal_gen

# NuRadioMC includes
from radiotools import helper as hp
from NuRadioReco.detector import antennapattern

class DetKernel(icetray.I3Module):

	'''
	This is the detector kernel.
	It does all of the heavy lifting after the antenna.
	The ray tracing and signal generation belong to the neutrino kernel.
	'''

	def __init__(self, context):
		icetray.I3Module.__init__(self, context)
		
		# there is no default seed, we should always make the user specify
		# the seed, otherwise we risk undefined behavior at the 
		# icetray <-> nuradiomc <-> numpy interface

		self.AddParameter("seed", 
			"Seed for random number generator",
			None)

		self.AddParameter("n_samples_signalclass", 
			"Number of samples in Askaryan trace from signal class",
			None)

		self.AddParameter("sampling_rate_signalclass", 
			"Sampling rate of Askaryan trace from signal class",
			None)

		# and some geometry information
		#############################################
		#############################################

		self.AddParameter("ant_geo_map",
			"The I3IceAntennaGeoMap",
			None)


	def Configure(self):

		tray_context = self.context # get the tray context

		# signal generation parameters
		#############################################
		#############################################

		# for the seed only, we will require that it either have been passed in 
		# as an argument or otherwise be in the context (in that order)
		# otherwise, we should throw a fatal error
		# we will also require the user to tell us the sampling rate and num samples
		# from the signal class

		self._seed = self.GetParameter("seed")
		if not self._seed:
			self._seed = tray_context['seed']
			if not self._seed:
				icetray.logging.log_fatal("No seed found for signal generation, \
					either as an argument or in the context. Abort!")
			icetray.logging.log_info("Signal generation seed: {}".format(self._seed))

		self._internal_n_samples = self.GetParameter("n_samples_signalclass")
		if not self._internal_n_samples:
			self._internal_n_samples = tray_context['internal_number_of_samples']
			if not self._seed:
				icetray.logging.log_fatal("No internal number of samples found in context. Abort!")
			icetray.logging.log_info("Internal number of samples: {}".format(self._internal_n_samples))

		self._internal_sampling_rate = self.GetParameter("sampling_rate_signalclass")
		if not self._internal_sampling_rate:
			self._internal_sampling_rate = tray_context['internal_sampling_rate']
			if not self._seed:
				icetray.logging.log_fatal("No internal sampling rate found in context. Abort!")
			icetray.logging.log_info("Internal sampling rate: {}".format(self._internal_sampling_rate))

		self._internal_dt = 1./ self._internal_sampling_rate
		icetray.logging.log_debug("Internal dt is {}".format(self._internal_dt))

		# GCD file information
		#############################################
		#############################################
		if 'gcd_file' not in tray_context:
			icetray.logging.log_fatal("No GCD file is specified. Please set gcd_file in the tray context")
		self.antgeomap = util_geo.get_iceantennageo(tray_context['gcd_file'])

	def run_det_kernel(self, frame):

		# we'll need an array of frequencies at which we'll calculate attens etc
		# declare it here so we don't wast time declaring it over and over again
		ff = np.fft.rfftfreq(self._internal_n_samples, self._internal_dt)

		if 'ParticleRadioMCSummaryMap' not in frame:
			icetray.logging.log_warn('Frame does not contain ParticleRadioMCSummaryMap. Do nothing (frame will not be pushed). \n(Btw, please make sure tray.AddModule(NuKernel) is included!')
			return 1
		particle_radio_mc_map = frame.Get('ParticleRadioMCSummaryMap')

		# load the list of antennas
		antgeomap = self.antgeomap

		# loop over antennas
		for iceantkey, g in antgeomap:

			# TODO: put this into the Configure
			antenna_model = g.antennaModel
			antenna_provider = antennapattern.AntennaPatternProvider()
			antenna_pattern = antenna_provider.load_antenna_pattern(antenna_model)
			antenna_orientation = np.asarray([g.orientation.theta, g.orientation.phi, g.rotation.theta, g.rotation.phi])
			# VEL = antenna_pattern.get_antenna_response_vectorized(ff, zenith, azimuth)

			# # loop over vertices
			# for particle, radiomcmap in particle_radio_mc_map:

			# 	if iceantkey not in radiomcmap.keys():
			# 		icetray.logging.log_info("Antenna key {} is not in the map for this particle")
			# 		continue # skip to the next particle

			# 	# get the radio summary for this antenna/vertex combination
			# 	this_radio_mc_summary = radiomcmap[iceantkey]

			# 	# now, we must fold the Efield with a model of the antenna


	def Physics(self, frame):
		retval = self.run_det_kernel(frame)
		self.PushFrame(frame)
