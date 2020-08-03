# python includes
import numpy as np

from icecube import icetray, dataclasses
from icecube.icetray import I3Units

# we need the NuRadioMC signal propagator module
from NuRadioMC.SignalGen import askaryan

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
			switch_askaryan_model = tray_context['askaryan_model']
			if switch_askaryan_model != self._default_askaryan_model:
				self._askaryan_model = switch_askaryan_module
				icetray.logging.log_info("Signal generation module switched to {}".format(self._askaryan_model))

		self._n_samples = self.GetParameter("n_samples")
		if 'internal_number_of_samples' in tray_context:
			switch_n_samples = tray_context['internal_number_of_samples']
			if switch_n_samples != self._default_n_samples:
				self._n_samples = switch_n_samples
				icetray.logging.log_info("Askaryan number of samples switched to {}".format(self._n_samples))

		self._sampling_rate = self.GetParameter("sampling_rate")
		if 'internal_sampling_rate' in tray_context:
			switch_sampling_rate = tray_context['internal_sampling_rate']
			if switch_sampling_rate != self._default_sampling_rate:
				self._sampling_rate = switch_sampling_rate
				icetray.logging.log_info("Askaryan sampling rate switched to {}".format(self._sampling_rate))

		self._dt = 1./ self._sampling_rate
		icetray.logging.log_debug("Askaryan dt is {}".format(self._dt))
		
	def get_emission(self, frame):

		thetac = np.arccos(1/1.35)

		signal = askaryan.get_time_trace(
			energy = 1e18, # energy of the shower
			theta = thetac, # viewangle
			N=self._n_samples,
			dt=self._dt,
			shower_type='HAD',
			n_index=1.35,
			R=1,
			model=self._askaryan_model
		)

	def recover_factors(self, frame):

		mctree = frame.Get('I3MCTree') # get the I3MCTree
		# print(mctree)

		primary = mctree.primaries[0]
		# print(type(primary))

		# primary = dataclasses.get_most_energetic_primary(mctree)
		daughters = mctree.get_daughters(primary)
		print(daughters)

		# daughters = mctree.children(primary)
		# print(daughters)
		# # print(primaries)
		# if len(primaries) ==1:
		# 	idx=0
		# elif 'I3MCWeightDict' in frame:
		# 	idx = [i for i in range(len(primaries)) if primaries[i].is_neutrino][0]
		# print(idx)

		# etot = 0

		# primary = dataclasses.get_most_energetic_primary(mctree)
		# children = mctree.children(primary)
		# for child in children:
		# 	print(child)
		# 	grandchildren = mctree.children(child)
		# 	for grandchild in grandchildren:
		# 		# print(grandchildren)
		# 		etot+= grandchild.energy

		# print("Etot grandchildren is {}".format(etot))
		# print("Etot primary is {}".format(primary.energy))
		# print("About to print the children")
		# print(children)
		# print(dataclasses.number_of_children(primary.number_of_children))
		# pnu = primary.energy/I3Units.eV
		# pnu = primary.energy
		# for particle in mctree:
			# print(particle)

		# print(primary)

		# print(primary)
		# print(primary.energy)
		# primary = mctree.get_most_energetic_primary()
		# print(primary.Get('energy'))
		# for particle in frame.Get('I3MCTree'):

	def Physics(self, frame):
		self.get_emission(frame)
		# self.recover_factors(frame)
		self.PushFrame(frame)






