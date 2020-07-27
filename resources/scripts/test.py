from icecube import icetray, dataio, dataclasses, phys_services
from I3Tray import I3Tray
from icecube.icetradio import signal_prop


tray = I3Tray()
# tray.context['I3RandomService'] = phys_services.I3GSLRandomService(42)
tray.Add("I3InfiniteSource", stream=icetray.I3Frame.Physics) #add an infinite source in a P-frame to play with
tray.AddModule(signal_prop.SignalProp, "SignalPropMod")
tray.Add("Dump")
tray.Add("I3Writer", filename="quick.i3.zst")
tray.Execute(10)
