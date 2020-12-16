import math

from icecube import icetray, dataio, dataclasses, phys_services, icetradio
from I3Tray import I3Tray
from icecube.icetradio import signal_gen, nu_kernel, det_kernel


icetray.set_log_level(icetray.I3LogLevel.LOG_INFO)

# quasi-complete working list
tray = I3Tray()
tray.AddModule("I3Reader", filename='nue_sample.i3.zst')

tray.context['seed'] = 12345
# currently tuned for 1024 samples at 4 GHz
tray.context['internal_signal_trace_length'] = 256e-9 * icetray.I3Units.second
tray.context['internal_sampling_rate'] = 4e9 * icetray.I3Units.hertz # 5 GHz
tray.context['internal_number_of_samples'] =				\
	int(													\
		math.ceil(											\
			tray.context['internal_signal_trace_length']	\
			* tray.context['internal_sampling_rate']		\
			/2.												\
		)													\
		*2													\
	)

# tray.context['internal_dt'] = 1./ tray.context['internal_sampling_rate']
# tray_context = tray.context
# print(tray_info)
# if not 'internal_dt' in tray_context:
	# print("internal_dtds is missing in the tray context")
# if not 'internal_dtds' in tray.TrayInfo()
# ?if tray.context['internal_dtds']:	print("Tray containts internal_dt")


tray.context['I3RandomService'] = phys_services.I3GSLRandomService(tray.context['seed'])
i3file = dataio.I3File("make_gcd_file/sampleGCD.i3.gz", "r")
tray.context['gcd_file'] = i3file
# tray.Add("I3InfiniteSource", stream=icetray.I3Frame.Physics) #add an infinite source in a P-frame to play with
# tray.AddModule(signal_prop.SignalProp, "SignalPropMod")
# tray.Add("Dump")
tray.AddModule(signal_gen.TreeThinner, "TreeThinner")
# tray.AddModule(signal_gen.SignalGen, "SignalGen")
tray.AddModule(nu_kernel.NuKernel, "NuKernel")
tray.AddModule(det_kernel.DetKernel, "DetKernel")
tray.Add("I3Writer", filename="quick.i3.zst")
tray.Execute(3)


# dummy code for rapid prototyping

# class TestModule(icetray.I3Module):
# 	def __init__(self, context):
# 		icetray.I3Module.__init__(self, context)

# 	def Configure(self):
# 		self.something=2

# 	def Physics(self, frame):
# 		trace_record = icetradio.I3RayTraceRecord()
# 		trace_record.numSolutions = 1

# 		# something = icetradio.I3RayTraceSolutionSeries()

# 		trace_solution = icetradio.I3RayTraceSolution()
# 		trace_solution.solutionNumber=1
# 		trace_solution.solutionType = 1
# 		trace_solution.C0 = 2
# 		trace_solution.C1 = 3
# 		trace_solution.pathLength = 20
# 		trace_solution.travelTime = 30
# 		trace_solution.launchVector = dataclasses.I3Position(1,2,3)
# 		trace_solution.receiveVector = dataclasses.I3Position(4,5,6)

# 		print(trace_solution)

# 		trace_record.solutions.append(trace_solution)

# 		frame.Put("atracerecord",trace_record)
# 		self.PushFrame(frame)

# @icetray.traysegment
# def GeneratorSegment(tray, name):
# 	def generator(frame):
# 		frame["tree"] = dataclasses.I3Particle()

# 	tray.Add("I3InfiniteSource")
# 	tray.Add(generator, streams=[icetray.I3Frame.DAQ])


# tray = I3Tray()
# # tray.Add(GeneratorSegment)
# tray.Add("I3InfiniteSource", stream=icetray.I3Frame.Physics)
# # tray.AddModule(signal_prop.SignalProp, "SignalPropMod")
# tray.Add(TestModule)
# tray.Add("Dump")
# tray.Add("I3Writer", filename="dumb.i3.zst")
# tray.Execute(2)