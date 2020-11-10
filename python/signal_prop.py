import numpy as np
from icecube import icetray, dataclasses, icetradio

def do_ray_tracing(
	propagator,
	ice_model,
	attenuation_model,
	source,
	target
	):

	"""
	A function to do ray tracing

	Do ray tracing between a source and target


	Parameters
	----------
	propagator: NuRadioMC.SignalProp propagation object
		a propagator from the NuRadioMC.SignaProp class
	
	ice_model: NuRadioMC.utilities medium object
		a medium object from the NuRadioMC.utilities class
	
	attenuation_model: string
		name of the desired attenuation model 
		from the NuRadioMC.utilities attenuation models

	source: I3Position
		I3Position of the source in surface-oriented coordinates 
		in meters

	target: I3Position
		I3Position of the target in surface-oriented coordiantes
		in meters

	Returns
	-------
	trace_record: I3RayTraceRecord
		the ray tracing record for this source/target pair
	"""

	# call the propagator for this source  & target combination
	r = propagator(source,
		target,
		medium=ice_model,
		attenuation_model=attenuation_model,
		n_frequencies_integration=25,
		n_reflections=0)

	r.find_solutions()
	num_solutions = r.get_number_of_solutions()

	# First, we create a I3RayTraceRecord to hold the results of all ray tracing.
	# Then, we loop over all the solutions we have for this source-target pair
	# for each solution iS, we will create a I3RayTraceSolution
	# and fill that solution with the relevant content, including:
	# the solutionNumber, solutionType, C0, C1, travelTime, and pathLength.
	# We will also fill in the launchVector and receiveVector.
	# Note that because I3RayTraceSolution.launchVector and receiveVector
	# are of the I3Position class, but the NuRadioMC function
	# get_launch_vector and get_receive_vector return normal
	# numpy arrays, we have to convert them to I3Positions first.
	# Finally, we will append the vector of solutions in the trace_record
	# with the trace_solutions.

	trace_record = icetradio.I3RayTraceRecord()
	trace_record.numSolutions = num_solutions

	for iS in range(num_solutions):

		trace_solution = icetradio.I3RayTraceSolution()
		
		trace_solution.solutionNumber = iS
		trace_solution.solutionType = r.get_solution_type(iS)
		trace_solution.C0 = r.get_results()[iS]['C0']
		trace_solution.C1 = r.get_results()[iS]['C1']
		trace_solution.travelTime = r.get_travel_time(iS) * icetray.I3Units.ns
		trace_solution.pathLength = r.get_path_length(iS) * icetray.I3Units.m

		# For the launchVector and receiveVector we must get the answer
		# from NuRadioMC (as a numpy array), and then place the answers into
		# I3Position objects to be written out

		launch_vector = r.get_launch_vector(iS)
		receive_vector = r.get_receive_vector(iS)

		trace_solution.launchVector = dataclasses.I3Position(launch_vector[0],
			launch_vector[1],
			launch_vector[2])

		trace_solution.receiveVector = dataclasses.I3Position(receive_vector[0],
			receive_vector[1],
			receive_vector[2])

		trace_record.solutions.append(trace_solution)

	return trace_record









	