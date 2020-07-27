# import icecube.icetray
from icecube.load_pybindings import load_pybindings
# icecube.icetray.load('icetradio', False)
load_pybindings(__name__, __path__)
# del icecube
del load_pybindings