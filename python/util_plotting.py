import numpy as np
import matplotlib.pyplot as plt

from icecube import icetray, dataclasses
from icecube.icetradio import util_dataclasses

from NuRadioReco.utilities import units, fft

def plot_field_and_trace(the_field, trace_after_antenna, trace_after_amps, info=None):

	"""
	A function to plot the efields, trace after antenna, and trace after amps all together

	Parameters
	----------
	the_field: the I3EField
		the I3EField before the antenna

	trace_after_antenna: array
		voltage trace after the antenna but before amplifiers

	trace_after_amps: array
		voltage trace after the amplifiers and filters

	info : 
		information the user would like put into the output filename


	Returns
	-------
	void

	"""
	print("Plotting the event...")
	eTheta = the_field.eTheta.trace
	ePhi = the_field.ePhi.trace
	dT = 1./the_field.eTheta.samplingRate
	eTheta_fft = fft.time2freq(eTheta, 1./dT)
	ePhi_fft = fft.time2freq(ePhi, 1./dT)

	trace_after_antenna_fft = fft.time2freq(trace_after_antenna, 1./dT)
	trace_after_amps_fft = fft.time2freq(trace_after_amps, 1./dT)

	times = util_dataclasses.get_I3Trace_times(the_field.eTheta)
	frequencies = np.fft.rfftfreq(len(eTheta), dT)

	fig, axs = plt.subplots(3,2,figsize=(10,10))
	axs[0][0].plot(times, eTheta, label='Theta Component')
	axs[0][0].plot(times, ePhi, '--', label='Phi Component')
	axs[0][0].legend()
	axs[0][0].set_xlabel('Time (ns)')
	axs[0][0].set_ylabel('V/m')
	axs[0][0].set_title("E-Fields -- Time Domain")
	
	axs[0][1].plot(frequencies, np.abs(eTheta_fft))
	axs[0][1].plot(frequencies, np.abs(ePhi_fft), '--')
	axs[0][1].set_xlim([0,1])
	axs[0][1].set_ylabel('Spectrum')
	axs[0][1].set_xlabel('Frequency (GHz)')
	axs[0][1].set_title("E-Fields -- Frequency Domain")

	axs[1][0].plot(times, trace_after_antenna)
	axs[1][1].plot(frequencies, np.abs(trace_after_antenna_fft))
	axs[1][0].set_xlabel('Time (ns)')
	axs[1][0].set_ylabel('V')
	axs[1][0].set_title("Trace, After Antenna -- Time Domain")
	axs[1][1].set_xlabel('Freq (GHz)')
	axs[1][1].set_ylabel('V')
	axs[1][1].set_title("Trace, After Antenna -- Frequency Domain")
	axs[1][1].set_xlim([0,1])

	axs[2][0].plot(times, trace_after_amps)
	axs[2][1].plot(frequencies, np.abs(trace_after_amps_fft))
	axs[2][0].set_xlabel('Time (ns)')
	axs[2][0].set_ylabel('V')
	axs[2][0].set_title("Trace, After Amps+Filter -- Time Domain")
	axs[2][1].set_xlabel('Freq (GHz)')
	axs[2][1].set_ylabel('V')
	axs[2][1].set_title("Trace, After Amps+Filter -- Frequency Domain")
	axs[2][1].set_xlim([0,1])

	plt.tight_layout()
	save_tile = 'event.png'
	if info is not None:
		save_tile='event_' + info + 'png'
	fig.savefig(save_tile)
	plt.close(fig)
	del fig, axs