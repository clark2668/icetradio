# python includes
import numpy as np

from icecube import icetray, dataclasses, icetradio
from icecube.dataclasses import I3Particle
from icecube.icetradio import util_geo, util_dataclasses

from NuRadioMC.SignalGen import askaryan
from radiotools import helper as hp


def generate_signal(
	deposited_energy,
	shower_axis,
	em_or_had,
	launch_vector,
	distance,
	n_index,
	dt,
	n_samples,
	model,
	seed
	):

	local_launch_vector = util_dataclasses.i3pos_to_np(launch_vector)
	local_shower_axis = util_dataclasses.i3pos_to_np(shower_axis)

	viewing_angle = hp.get_angle(local_shower_axis, local_launch_vector)

	signal = askaryan.get_time_trace(
		energy = deposited_energy,
		theta = viewing_angle,
		N = n_samples,
		dt= dt,
		shower_type=em_or_had,
		n_index=n_index,
		R=distance,
		model=model,
		seed=seed
		)

	# calculate the polarization
	polarization_direction_onsky = util_geo.calculate_polarization_vector(local_launch_vector, local_shower_axis)
	icetray.logging.log_debug("Polarization direction on sky {}".format(polarization_direction_onsky))

	# create the e-fields at the antenna
	this_eR, this_eTheta, this_ePhi = np.outer(polarization_direction_onsky, signal)

	sampling_rate = 1./dt
	eR = util_dataclasses.fill_I3Trace(this_eR, 0, sampling_rate)
	eTheta = util_dataclasses.fill_I3Trace(this_eTheta, 0, sampling_rate)
	ePhi = util_dataclasses.fill_I3Trace(this_ePhi, 0, sampling_rate)

	field = util_dataclasses.fill_I3EField(eR, eTheta, ePhi)

	return field


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
