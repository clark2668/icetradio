from icecube import icetray, dataio, dataclasses, phys_services, icetradio
from I3Tray import I3Tray
from icecube.icetradio import signal_prop, signal_gen




# tray = I3Tray()
# tray.AddModule("I3Reader", filename='numu_sample.i3.zst')
# tray.context['I3RandomService'] = phys_services.I3GSLRandomService(42)
# tray.Add("I3InfiniteSource", stream=icetray.I3Frame.Physics) #add an infinite source in a P-frame to play with
# tray.AddModule(signal_prop.SignalProp, "SignalPropMod")
# tray.AddModule(signal_gen.SignalGen, "SignalGen")
# tray.Add("Dump")
# tray.Add("I3Writer", filename="quick.i3.zst")
# tray.Execute(2)


class TestModule(icetray.I3Module):
	def __init__(self, context):
		icetray.I3Module.__init__(self, context)

	def Configure(self):
		self.something=2

	def Physics(self, frame):
		trace_record = icetradio.I3RayTraceRecord()
		trace_record.numSolutions = 1

		# something = icetradio.I3RayTraceSolutionSeries()

		trace_solution = icetradio.I3RayTraceSolution()
		trace_solution.solutionNumber=1
		trace_solution.solutionType = 1
		trace_solution.C0 = 2
		trace_solution.C1 = 3
		trace_solution.pathLength = 20
		trace_solution.travelTime = 30
		trace_solution.launchVector = dataclasses.I3Position(1,2,3)
		trace_solution.receiveVector = dataclasses.I3Position(4,5,6)

		print(trace_solution)

		trace_record.solutions.append(trace_solution)

		frame.Put("atracerecord",trace_record)
		self.PushFrame(frame)

@icetray.traysegment
def GeneratorSegment(tray, name):
	def generator(frame):
		frame["tree"] = dataclasses.I3Particle()

	tray.Add("I3InfiniteSource")
	tray.Add(generator, streams=[icetray.I3Frame.DAQ])


tray = I3Tray()
# tray.Add(GeneratorSegment)
tray.Add("I3InfiniteSource", stream=icetray.I3Frame.Physics)
# tray.AddModule(signal_prop.SignalProp, "SignalPropMod")
tray.Add(TestModule)
tray.Add
tray.Add("Dump")
tray.Add("I3Writer", filename="dumb.i3.zst")
tray.Execute(2)