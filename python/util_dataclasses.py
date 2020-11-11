import numpy as np

from icecube import icetray, dataclasses, icetradio

def fill_I3EField(
	eR,
	eTheta,
	ePhi
	):

	"""
	Create an I3EField

	Parameters
	----------
	eR: np array
		eR samples of the field

	eTheta: np array
		eTheta samples of the field

	ePhi: double or float
		ePhi samples of the field

	Returns
	-------
	field: I3EField
		field containing the three components
	"""

	field = icetradio.I3EField()
	field.eR = eR
	field.eTheta = eTheta
	field.ePhi = ePhi

	return field

def fill_I3Trace(
	voltage_samples,
	trace_start_time,
	sampling_rate,
	):

	"""
	Create an I3Trace

	Parameters
	----------
	voltage_samples: numpy array
		the samples to go in the trace

	trace_start_time: double or float
		the start time of the trace in s

	sampling_rate: double or float
		the sampling rate of the trace (specifies dt) in Hz

	Returns
	-------
	trace: I3Trace
		trace containing the voltage samples
	"""

	trace = icetradio.I3Trace()
	trace.trace = voltage_samples
	trace.traceStartTime = trace_start_time
	trace.samplingRate = sampling_rate

	return trace

def i3pos_to_np(pos, refframe='car'):
	if refframe=='car':
		return np.array([pos.x, pos.y, pos.z])
	elif refframe=='sph':
		return np.array([pos.r, pos.theta, pos.phi])

def np_to_i3pos(pos, refframe='car'):
	if len(pos)>3:
		icetray.logging.log_error("Input np array has too many ({}) elements. Returning I3Position at 0,0,0".format(len(pos)))
		return dataclasses.I3Position(0.,0.,0.)
	if refframe=='car':
		return dataclasses.I3Position(pos[0], pos[1], pos[2])
	elif refframe=='sph':
		return dataclasses.I3Position(pos[0], pos[1], pos[2], dataclasses.I3Position.sph)
	else:
		icetray.logging.log_error("Input has unrecognized ref frame ({}) elements. Returning I3Position at 0,0,0".format(refframe))
		return dataclasses.I3Position(0.,0.,0.)		



