from icecube import icetray, dataio, dataclasses

class SignalProp(icetray.I3Module):
	def __init__(self, context):
		icetray.I3Module.__init__(self, context)
		self.default_param_value = 42
		self.AddParameter("SomeParam", "Docstrin...", default_param_value)

	def Configure(self):
		self.some_param = self.GetParameter("SomeParam")
		if self.some_param != self.default_param_value:
			print("User changed SomeParam to {}".format(self.some_param))

	def DAQ(self, frame):
		self.PushFrame(frame)