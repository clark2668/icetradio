# python includes
import numpy as np

# icecube includes
from icecube import icetray, dataclasses
from icecube.dataclasses import I3Particle

# NuRadioMC includes
from NuRadioMC.SignalGen import askaryan

class SignalGen(icetray.I3Module):
	
	def __init__(self, context):
		icetray.I3Module.__init__(self, context)
		
		self._default_askaryan_model = 'Alvarez2009'
		self._default_n_samples = 1000
		self._default_sampling_rate = 5e9 * icetray.I3Units.hertz
		self._default_energy_cut = 0.1e15 * icetray.I3Units.eV

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

		self.AddParameter("energy_cut",
			"Minimum energy deposition to be considered",
			self._default_energy_cut)

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

		self._energy_cut = self.GetParameter("energy_cut")
		if 'energy_cut' in tray_context:
			if tray_context['energy_cut'] != self._energy_cut:
				self._energy_cut = tray_context['energy_cut']
				icetray.log_info.log_info("Minimum energy cut switched tio {}".format(self._energy_cut))
		
	def get_emission(self, frame):

		# for more information on how the askaryan module works
		# and it's various parameters, please consult NuRadioMC
		# https://github.com/nu-radio/NuRadioMC/blob/master/NuRadioMC/SignalGen/askaryan.py

		nindex = 1.35
		thetac = np.arccos(1/nindex)

		signal = askaryan.get_time_trace(
			energy = 1e18,
			theta = thetac,
			N=self._n_samples,
			dt=self._dt,
			shower_type='HAD',
			n_index=nindex,
			R=1,
			model=self._askaryan_model,
			seed=self._seed
		)

	def thin_i3mctree(self, frame):
		
		mctree = frame.Get('I3MCTree') # get the I3MCTree
		primary = mctree.primaries[0]
		
		# make a thinned mctree which only contains relevant energy depositions
		thin_mctree = dataclasses.I3MCTree()
		thin_mctree.add_primary(primary)

		num_particles = len(mctree) # and get its length
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
				# specifically EPlus, EMinus, Brems, DeltaE, PairProd, NuclInt, Hadrons, PiPlus or PiMinus
				if particle.is_cascade:
					icetray.logging.log_info("Cascade!")
					thin_mctree.append_child(primary, particle)

		frame.Put("I3MCTreeThin", thin_mctree)

	def Physics(self, frame):
		# self.get_emission(frame)
		self.thin_i3mctree(frame)
		self.PushFrame(frame)






