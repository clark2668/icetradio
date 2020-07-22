from icecube import icetray

# we need the NuRadioMC signal propagator module
from NuRadioMC.SignalProp import propagation

class SignalProp(icetray.I3Module):
	
	def __init__(self, context):
		icetray.I3Module.__init__(self, context)
		
		self._default_prop_mode='analytic'
		self.AddParameter("propagation_model", 
			"What type of propagation. Only analytic supported currently",
			self._default_prop_mode)

	def Configure(self):
		self.prop_model = self.GetParameter("propagation_model")
		if self.prop_model != self._default_prop_mode:
			print("propagation_model changed to {}".format(self.prop_model))

		# get the propagator from NuRadioMC
		self.propagator = propagation.get_propagation_module(self.prop_model)

	def DAQ(self, frame):
		self.PushFrame(frame)
