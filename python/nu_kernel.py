# python includes
import numpy as np

# icecube includes
from icecube import icetray, dataclasses, icetradio
from icecube.dataclasses import I3Particle
from icecube.icetradio import util_geo, signal_prop

# NuRadioMC includes
from NuRadioMC.SignalGen import askaryan
from radiotools import helper as hp
from radiotools import coordinatesystems as cstrans
from NuRadioMC.SignalProp import propagation
from NuRadioMC.utilities import medium



class NuKernel(icetray.I3Module):

	'''
	This is the neutrino kernel.
	It does all of the heavy lifting up until the antenna.
	The antenna response/ detector response will be handled by the detector kernel.
	In order to do this, it needs to know lots of information about the
	ray tracing and about the askaryan generator.
	So most of the default parameters deal with that.
	'''

	def __init__(self, context):
		icetray.I3Module.__init__(self, context)
		
		# signal generation parameters
		#############################################
		#############################################
		self._default_askaryan_model = 'Alvarez2009'
		self._default_n_samples = 1000
		self._default_sampling_rate = 5e9 * icetray.I3Units.hertz

		# there is no default seed, we should always make the user specify
		# the seed, otherwise we risk undefined behavior at the 
		# icetray <-> nuradiomc <-> numpy interface

		self.AddParameter("seed", 
			"Seed for random number generator",
			None)

		self.AddParameter("askaryan_model", 
			"Askaryan model",
			self._default_askaryan_model)

		self.AddParameter("n_samples", 
			"Number of samples in Askaryan trace from signal class",
			self._default_n_samples)

		self.AddParameter("sampling_rate", 
			"Sampling rate of Askaryan trace from signal class",
			self._default_sampling_rate)

		# signal propagation parameters
		#############################################
		#############################################
		self._default_prop_mode='analytic'
		self._default_ice_model='ARAsim_southpole'
		self._default_att_model='SP1'
		
		self.AddParameter("propagation_model", 
			"What type of propagation. Only analytic supported currently",
			self._default_prop_mode)
		
		self.AddParameter("ice_model", 
			"Index of refraction profile",
			self._default_ice_model)
		
		self.AddParameter("attenuation_model", 
			"Attenuation model",
			self._default_att_model)

		# and some geometry information
		#############################################
		#############################################
		self.AddParameter("gcd_file",
			"GCD file containing the antenna geometry",
			None)


	def Configure(self):

		tray_context = self.context # get the tray context


		# signal generation parameters
		#############################################
		#############################################

		# for the seed only, we will require that it either have been passed in 
		# as an argument or otherwise be in the context (in that order)
		# otherwise, we should throw a fatal error

		self._seed = self.GetParameter("seed")
		if not self._seed:
			self._seed = tray_context['seed']
			if not self._seed:
				icetray.logging.log_info("No seed found for signal generation, \
					either as an argument or in the context. Abort!")
			icetray.logging.log_info("Signal generation seed: {}".format(self._seed))

		# for all other objects, we can check for positional or context overrides,
		# and otherwise, just leave things as the default

		self._askaryan_model = self.GetParameter("askaryan_model")
		if 'askaryan_model' in tray_context:
			if tray_context['askaryan_model'] != self._default_askaryan_model:
				self._askaryan_model = tray_context['askaryan_model']
				icetray.logging.log_info("Signal generation module switched to {}".format(self._askaryan_model))

		self._n_samples = self.GetParameter("n_samples")
		if 'internal_number_of_samples' in tray_context:
			if tray_context['internal_number_of_samples'] != self._default_n_samples:
				self._n_samples = tray_context['internal_number_of_samples']
				icetray.logging.log_info("Askaryan number of samples switched to {}".format(self._n_samples))

		self._sampling_rate = self.GetParameter("sampling_rate")
		if 'internal_sampling_rate' in tray_context:
			if tray_context['internal_sampling_rate'] != self._default_sampling_rate:
				self._sampling_rate = tray_context['internal_sampling_rate']
				icetray.logging.log_info("Askaryan sampling rate switched to {}".format(self._sampling_rate))

		self._dt = 1./ self._sampling_rate
		icetray.logging.log_debug("Askaryan dt is {}".format(self._dt))

		# signal propagation parameters
		#############################################
		#############################################
		self._prop_model = self.GetParameter("propagation_model")
		self._ice_model = self.GetParameter("ice_model")
		self._att_model = self.GetParameter("attenuation_model")

		# get the propagator from NuRadioMC
		self.propagator = propagation.get_propagation_module(self._prop_model)
		
		# get the ice from NuRadioMC
		self.ice = medium.get_ice_model(self._ice_model)

		# GCD filel information
		#############################################
		#############################################
		if 'gcd_file' not in tray_context:
			icetray.logging.log_fatal("No GCD file is specified. Please set gcd_file in the tray context")
		self.gcd = tray_context['gcd_file']


	def run_nu_kernel(self, frame):

		# get the list of particles from the *thinned* mctree
		if 'I3MCTreeThin' not in frame:
			icetray.logging.log_fatal('Frame does not contain the thinned tree I3MCTreeThin \n Please tray.AddModule(TreeThinner) first!')
		mctree = frame.Get('I3MCTreeThin')

		# load the list of antennas
		antgeo = util_geo.get_iceantennageo(self.gcd)

		# now, we loop over every particle, and every antenna, and do ray tracing
		for particle in mctree:

			# get the source (vertex) position, and move it into surface oriented coordinates
			source = particle.pos
			source = util_geo.convert_i3_to_global(source)

			for iceantkey, g in antgeo:
				
				# get the target (antenna) position, and move it into surface oriented coordinates
				target = g.position
				target = util_geo.convert_i3_to_global(target)

				# do ray tracing
				record = signal_prop.do_ray_tracing(
					propagator=self.propagator,
					ice_model=self.ice,
					attenuation_model=self._att_model,
					source=source,
					target=target)


	def Physics(self, frame):
		self.run_nu_kernel(frame)
		self.PushFrame(frame)
