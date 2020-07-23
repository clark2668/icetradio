from icecube import icetray, dataio, dataclasses, icetradio
from I3Tray import I3Tray
from icecube.icetradio import signal_prop

tray = I3Tray()
tray.AddModule(signal_prop.SignalProp, "SignalPropMod")
tray.Add("Dump")
tray.Execute(10)
