from icecube import icetray, dataio, dataclasses, phys_services, icetradio
from I3Tray import I3Tray
from icecube.icetradio import signal_prop

@icetray.traysegment
def GeneratorSegment(tray, name):
	# def generator(frame):
	# 	frame["tree"] = dataclasses.I3Particle()

	tray.Add("I3InfiniteSource")
	# tray.Add(generator, streams=[icetray.I3Frame.Physics])
	# tray.Add(generator, streams=[icetray.I3Frame.DAQ])
	# tray.Add(lambda frame: frame.Has("tree"), streams=[icetray.I3Frame.DAQ])

# class ExampleModule(icetray.I3Module):
# 	def __init__(self, context):
# 		icetray.I3Module.__init__(self, context)
# 		self.AddParameter("RNG",'I3RandomService', None)

# 	def Configure(self):
# 		self.rng = self.GetParameter("RNG")
# 		if not self.rng:
# 			self.rng = self.context["I3RandomService"]

# 	def DAQ(self, frame):
# 		random_number = self.rng.uniform(1)
# 		frame.Put('RandomNumber', dataclasses.I3Double(random_number))
# 		# frame['RandomNumber'] = dataclasses.I3Double(random_number)
# 		self.PushFrame(frame)


tray = I3Tray()
tray.context['I3RandomService'] = phys_services.I3GSLRandomService(42)
tray.Add(GeneratorSegment)
# tray.Add(ExampleModule)
# tray.Add("I3InfiniteSource")
# tray.AddModule(signal_prop.SignalProp, "SignalPropMod")
tray.Add("Dump")
tray.Add("I3Writer", filename="quick.i3.zst")
tray.Execute(10)
