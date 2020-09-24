from icecube import icetray, dataio, dataclasses, phys_services, icetradio
from I3Tray import I3Tray
from icecube.icetradio import signal_prop, signal_gen

from random import seed
from random import random
import matplotlib.pyplot as plt
import numpy as np


class PrintTestTrace(icetray.I3Module):
	def __init__(self, context):
		icetray.I3Module.__init__(self, context)

	def Configure(self):
		self.something=2

	def Physics(self, frame):
		dummy_field = frame.Get('DummyEField')

		start_time = dummy_field.eR.traceStartTime
		num_samples = len(dummy_field.eR.trace)
		sampling_rate = dummy_field.eR.samplingRate
		times = np.arange(0, num_samples/sampling_rate - 0.1/sampling_rate, 1./sampling_rate ) + start_time

		fig = plt.figure(figsize=(5,5))
		ax = fig.add_subplot(111)
		ax.plot(times, dummy_field.eR.trace, label='eR')
		ax.plot(times, dummy_field.eTheta.trace, label='eTheta')
		ax.plot(times, dummy_field.ePhi.trace, label='ePhi')
		ax.set_xlim([90, 110])
		ax.set_xlabel('Time (ns)')
		ax.set_ylabel('Field Amplitude')
		ax.legend()

		rand = random()

		title = 'waveform{}.png'.format(rand)
		fig.savefig(title, bbox_inches='tight')

		self.PushFrame(frame)


tray = I3Tray()
tray.AddModule("I3Reader", filename='quick.i3.zst')
tray.Add(PrintTestTrace)
tray.Execute(10)