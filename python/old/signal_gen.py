# python includes
import numpy as np

# icecube includes
from icecube import icetray, dataclasses, icetradio
from icecube.dataclasses import I3Particle
from icecube.icetradio import util_geo

# NuRadioMC includes
from NuRadioMC.SignalGen import askaryan
from radiotools import helper as hp
from radiotools import coordinatesystems as cstrans
from NuRadioMC.SignalProp import propagation
from NuRadioMC.utilities import medium

class SignalGen(icetray.I3Module):
	
	def __init__(self, context):
		icetray.I3Module.__init__(self, context)
		
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

	def Configure(self):

		tray_context = self.context # get the tray context

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
		
	def get_test_emission(self, frame):

		propagator = propagation.get_propagation_module('analytic')
		ice = medium.get_ice_model('ARAsim_southpole')

		# work up a simple example to test functionality
		ant = np.array([0,0,-100])
		vertex = np.array([-2543.18,2319.96,-1828.74])
		azi = 2.4658
		zen = 1.0863
		inelast = 0.55
		inttype = 'cc'
		flavor = 14
		energy = 9.20e+18
		n_index = ice.get_index_of_refraction(vertex)
		cherenkov_angle = np.arccos(1./n_index)
		shower_axis = -1 * hp.spherical_to_cartesian(zen, azi)

		r = propagator(vertex,
			ant,
			medium=ice,
			attenuation_model='SP1',
			n_frequencies_integration=25,
			n_reflections=0
			)
		r.find_solutions()
		num_solutions = r.get_number_of_solutions()
		viewing_angles = []
		distances = []
		launch_vectors = []
		receive_vectors = []
		# print('num solutions is {}'.format(num_solutions))
		for iS in range(num_solutions):
			launch_vectors.append(r.get_launch_vector(iS))
			receive_vectors.append(r.get_receive_vector(iS))
			# launch_vector = r.get_launch_vector(iS)
			viewing_angles.append(hp.get_angle(shower_axis, launch_vectors[iS]))
			distances.append(r.get_path_length(iS))
			# viewing_angle = hp.get_angle(shower_axis, launch_vector)

		#fem, fhad = helper._get_em_had_fraction(inelast, inttype, flavor)
		fem=0
		fhad=0.55

		signal = askaryan.get_time_trace(
			energy = energy * fhad,
			theta = viewing_angles[0],
			N = self._n_samples,
			dt = self._dt,
			shower_type='HAD',
			n_index = n_index,
			R=distances[0],
			model=self._askaryan_model,
			seed=self._seed
		)

		polarization_direction_onsky = util_geo.calculate_polarization_vector(launch_vectors[0], shower_axis)
		icetray.logging.log_debug("Polarization direction on sky {}".format(polarization_direction_onsky))

		this_eR, this_eTheta, this_ePhi = np.outer(polarization_direction_onsky, signal)

		# create traces for the eR, eTheta, and ePhi components inside
		eR = icetradio.I3Trace()
		eTheta = icetradio.I3Trace()
		ePhi = icetradio.I3Trace()

		eR.trace = this_eR
		eR.traceStartTime = 0
		eR.samplingRate = self._sampling_rate
		eTheta.trace = this_eTheta
		eTheta.traceStartTime = 0
		eTheta.samplingRate = self._sampling_rate
		ePhi.trace = this_ePhi
		ePhi.traceStartTime = 0
		eTheta.samplingRate = self._sampling_rate


		# put those traces inside an EField
		field = icetradio.I3EField()
		field.eR = eR
		field.eTheta = eTheta
		field.ePhi = ePhi

		frame.Put("DummyEField", field)



		# for more information on how the askaryan module works
		# and it's various parameters, please consult NuRadioMC
		# https://github.com/nu-radio/NuRadioMC/blob/master/NuRadioMC/SignalGen/askaryan.py

		# nindex = 1.35
		# thetac = np.arccos(1/nindex)

		# signal = askaryan.get_time_trace(
		# 	energy = 1e18,
		# 	theta = thetac,
		# 	N=self._n_samples,
		# 	dt=self._dt,
		# 	shower_type='HAD',
		# 	n_index=nindex,
		# 	R=1,
		# 	model=self._askaryan_model,
		# 	seed=self._seed
		# )



	def Physics(self, frame):
		self.get_test_emission(frame)
		self.PushFrame(frame)


class TreeThinner(icetray.I3Module):

	def __init__(self, context):
		icetray.I3Module.__init__(self, context)
		
		self._default_energy_cut = 0.1e15 * icetray.I3Units.eV

		self.AddParameter("energy_cut",
			"Minimum energy deposition to be considered",
			self._default_energy_cut)
	
	def Configure(self):

		tray_context = self.context # get the tray context

		self._energy_cut = self.GetParameter("energy_cut")
		if 'energy_cut' in tray_context:
			if tray_context['energy_cut'] != self._energy_cut:
				self._energy_cut = tray_context['energy_cut']
				icetray.log_info.log_info("Minimum energy cut switched tio {}".format(self._energy_cut))
		
	def Physics(self, frame):

		if 'I3MCTreeThin' in frame:
			icetray.logging.log_fatal('File already contains the thinned I3MCTree')

		mctree = frame.Get('I3MCTree') # get the I3MCTree
		primary = mctree.primaries[0]
		
		# make a thinned mctree which only contains relevant energy depositions
		thin_mctree = dataclasses.I3MCTree()
		thin_mctree.add_primary(primary)

		num_particles = len(mctree) # get number of particles in the mctree
		if num_particles == 1:
			
			# catch the case where there was no interaction and just return outright
			icetray.logging.log_info("There are no children of the primary")
		
		else:

			# otherwise, loop through the mctree and look for energy depositions
			for particle in mctree:
			
				# skip the primary
				if particle == primary:
					continue

				# don't worry about this particle if it's energy is below the threshold
				if particle.energy < self._energy_cut:
					continue

				# and only add cascades cascades ("energy depositions") to the thin_mctree
				# includes EPlus, EMinus, Brems, DeltaE, PairProd, NuclInt, Hadrons, PiPlus or PiMinus
				# see https://docs.icecube.aq/combo/trunk/projects/dataclasses/particle.html is_cascade function
				if particle.is_cascade:
					thin_mctree.append_child(primary, particle)

		frame.Put("I3MCTreeThin", thin_mctree)

		self.PushFrame(frame)



