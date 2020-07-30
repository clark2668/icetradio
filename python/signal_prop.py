# python includes
import numpy as np

from icecube import icetray, dataclasses, icetradio

# we need the NuRadioMC signal propagator module
from NuRadioMC.SignalProp import propagation
from NuRadioMC.utilities import medium

class SignalProp(icetray.I3Module):
	
	def __init__(self, context):
		icetray.I3Module.__init__(self, context)
		
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
	
	def Configure(self):
		
		self._prop_model = self.GetParameter("propagation_model")
		self._ice_model = self.GetParameter("ice_model")
		self._att_model = self.GetParameter("attenuation_model")

		# get the propagator from NuRadioMC
		self.propagator = propagation.get_propagation_module(self._prop_model)
		
		# get the ice from NuRadioMC
		self.ice = medium.get_ice_model(self._ice_model)

	# do trace will actually do the ray tracing heavy lifting as an interface
	def do_trace(self, frame):
		# x1 is "source" position, while x2 is the target
		x1 = np.array([478, 0, -149])
		x2 = np.array([635, 0, -5])
	
		# call the propagator for this source  & target combination
		r = self.propagator(x1,
			x2,
			medium=self.ice,
			attenuation_model=self._att_model,
			n_frequencies_integration=25, # set this to 25
			n_reflections=0
		)

		
		r.find_solutions() # find solutions
		num_solutions = r.get_number_of_solutions()

		trace_record = icetradio.I3RayTraceRecord()
		trace_record.numSolutions = num_solutions

		# we only need a few things from the ray tracer at this phase
		for iS in range(num_solutions):

			trace_solution = icetradio.I3RayTraceSolution()

			trace_solution.solutionNumber = iS
			trace_solution.solutionType = r.get_solution_type(iS)
			trace_solution.C0 = r.get_results()[iS]['C0']
			trace_solution.C1 = r.get_results()[iS]['C1']
			trace_solution.travelTime = r.get_travel_time(iS) * icetray.I3Units.nanosecond
			trace_solution.pathLength = r.get_path_length(iS) * icetray.I3Units.meter

			launch_vector = r.get_launch_vector(iS)
			receive_vector = r.get_receive_vector(iS)

			trace_solution.launchVector = dataclasses.I3Position(launch_vector[0],
				launch_vector[1],
				launch_vector[2]
			)
			
			trace_solution.receiveVector = dataclasses.I3Position(receive_vector[0],
				receive_vector[1],
				receive_vector[2]
			)
			trace_record.solutions.append(trace_solution)

		frame.Put("RayTraceRecord",trace_record)

	def Physics(self, frame):
		self.do_trace(frame)
		self.PushFrame(frame)






