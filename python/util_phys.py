import numpy as np
from icecube import icetray, dataclasses
from icecube.dataclasses import I3Particle

def pick_em_or_had(type):

	em_types = [I3Particle.EMinus, I3Particle.Brems]
	had_types = [I3Particle.Hadrons, I3Particle.NuclInt]

	if type in had_types:
		return 'HAD'
	elif type in em_types:
		return 'EM'
	else:
		return 'UDEF'
