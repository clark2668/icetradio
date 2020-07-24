# python includes
import numpy as np

from icecube import icetray

# we need the NuRadioMC signal propagator module
from NuRadioMC.SignalProp import propagation
from NuRadioMC.utilities import medium

class SignalGen(icetray.I3Module):
	
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

	# do trace will actually do the ray tracing heavy lifting as an interface
	def do_trace(self):
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

		# now, we check for solutions
		r.find_solutions()
		num_solutions = r.get_number_of_solutions()
		print("Number of solutions {}".format(num_solutions))


		#TODO: put in logic for what happens if there is no solution


		# we only need a few things from the ray tracer at this phase
		for iS in range(r.get_number_of_solutions()):
			C0 = r.get_results()[iS]['C0']
			C1 = r.get_results()[iS]['C1']
			sol_type = r.get_solution_type(iS)
			path_length = r.get_path_length(iS)
			travel_time = r.get_travel_time(iS)
			launch_vector = r.get_launch_vector(iS)
			receive_vector = r.get_receive_vector(iS)



	def Configure(self):
		
		self._prop_model = self.GetParameter("propagation_model")
		self._ice_model = self.GetParameter("ice_model")
		self._att_model = self.GetParameter("attenuation_model")

		# get the propagator from NuRadioMC
		self.propagator = propagation.get_propagation_module(self._prop_model)
		
		# get the ice from NuRadioMC
		self.ice = medium.get_ice_model(self._ice_model)

		self.do_trace()

	def DAQ(self, frame):
		self.PushFrame(frame)






