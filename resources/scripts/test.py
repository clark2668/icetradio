from icecube import icetray, dataio, dataclasses, phys_services
from I3Tray import I3Tray
from icecube.icetradio import signal_prop, signal_gen


tray = I3Tray()
tray.AddModule("I3Reader", filename='numu_sample.i3.zst')
# tray.context['I3RandomService'] = phys_services.I3GSLRandomService(42)
# tray.Add("I3InfiniteSource", stream=icetray.I3Frame.Physics) #add an infinite source in a P-frame to play with
# tray.AddModule(signal_prop.SignalProp, "SignalPropMod")
tray.AddModule(signal_gen.SignalGen, "SignalGen")
tray.Add("Dump")
tray.Add("I3Writer", filename="quick.i3.zst")
tray.Execute(6)
