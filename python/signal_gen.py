# python includes
import numpy as np

from icecube import icetray, dataclasses, icetradio
from icecube.dataclasses import I3Particle
from icecube.icetradio import util_geo, util_dataclasses

from NuRadioMC.SignalGen import askaryan
from NuRadioReco.utilities import units, fft
from radiotools import helper as hp


def generate_signal(
	deposited_energy,
	shower_axis,
	em_or_had,
	launch_vector,
	distance,
	arrival_time,
	n_index,
	attenuation_values,
	dt,
	n_samples,
	model,
	seed,
	keep_unattenuated_fields=False
	):

	"""
	A function to generate askaryan fields at the antennas

	Get the askaryan signals/fields at the antenna. This means that the fields
	returned by this function will already include the polarization factors,
	the 1/R, and the attenuation due to the ice.

	Parameters
	----------
	deposited_energy: double or float
		energy deposited in the shower in eV
	
	shower_axis: I3Position
		the shower axis
	
	launch_vector: I3Position
		the launch vector of the ray that makes the signal

	distance: float
		the path length traveled by the signal in m (including ray bending!)

	arrival_time: float
		the time the field arrives at the antenna, in seconds (including ray bending!)

	n_index: float
		the index of refraction at the vertex

	atttenuation_values: complex np array
		the complex frequency-dependent attenuation factors

	dt: float
		the time between samples for the askaryan emission, in seconds

	n_samples: int
		the number of samples to have in the Askaryan emission

	model: string
		what Askaryan model should be used to generate the emission
		options are described in NuRadioMC.SignalGen.askaryan
		https://github.com/nu-radio/NuRadioMC/blob/master/NuRadioMC/SignalGen/askaryan.py

	seed: int
		what random number seed should be used in generating the askaryan emission

	keep_unattenuated_fields: bool
		whether or not to keep a copy of the E-fields that does not have attenuation factors applied
		default is False, to reduce file output sizes

	Returns
	-------
	signal: I3RadioSignal
		the radio signal container for this event
	"""

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

	signal_spectrum = fft.time2freq(signal, 1./dt)
	attenuated_signal_spectrum = signal_spectrum * attenuation_values
	attenuated_signal = fft.freq2time(attenuated_signal_spectrum, 1./dt)

	# calculate the polarization
	polarization_direction_onsky = util_geo.calculate_polarization_vector(local_launch_vector, local_shower_axis)
	icetray.logging.log_debug("Polarization direction on sky {}".format(polarization_direction_onsky))

	# create the e-fields at the antenna
	this_eR_attenuated, this_eTheta_attenuated, this_ePhi_attenuated = np.outer(polarization_direction_onsky, attenuated_signal)

	# store the eR, eTheta, ePhi components in trace for attenuated field
	sampling_rate = 1./dt
	eR_attenuated = util_dataclasses.fill_I3Trace(this_eR_attenuated, arrival_time, sampling_rate)
	eTheta_attenuated = util_dataclasses.fill_I3Trace(this_eTheta_attenuated, arrival_time, sampling_rate)
	ePhi_attenuated = util_dataclasses.fill_I3Trace(this_ePhi_attenuated, arrival_time, sampling_rate)

	# put those traces into fields
	field_watt = util_dataclasses.fill_I3EField(eR_attenuated, eTheta_attenuated, ePhi_attenuated)

	# and finally, create and return a signal object
	signal = icetradio.I3RadioSignal()
	signal.view_angle = viewing_angle * icetray.I3Units.rad
	signal.polarization_vector = util_dataclasses.np_to_i3pos(polarization_direction_onsky, 'sph')
	signal.field_watt = field_watt

	if keep_unattenuated_fields:
		# make a copy of the fields that doesn't include the attenuation factor
		# we can generally *not* save this information as a space saving measure
		this_eR, this_eTheta, this_ePhi = np.outer(polarization_direction_onsky, signal)
		eR = util_dataclasses.fill_I3Trace(this_eR, arrival_time, sampling_rate)
		eTheta = util_dataclasses.fill_I3Trace(this_eTheta, arrival_time, sampling_rate)
		ePhi = util_dataclasses.fill_I3Trace(this_ePhi, arrival_time, sampling_rate)
		field_noatt = util_dataclasses.fill_I3EField(eR, eTheta, ePhi)
		signal.field_noatt = field_noatt

	return signal


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
