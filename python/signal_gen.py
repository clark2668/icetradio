# python includes
import numpy as np

from icecube import icetray, dataclasses
from icecube.icetray import I3Units


# we need the NuRadioMC signal propagator module
from NuRadioMC.SignalProp import propagation
from NuRadioMC.utilities import medium

class SignalGen(icetray.I3Module):
	
	def __init__(self, context):
		icetray.I3Module.__init__(self, context)
		
		# self._default_prop_mode='analytic'
		
		# self.AddParameter("propagation_model", 
		# 	"What type of propagation. Only analytic supported currently",
		# 	self._default_prop_mode)

	def Configure(self):
		self.something=2

	def recover_factors(self, frame):

		mctree = frame.Get('I3MCTree') # get the I3MCTree
		print(mctree)

		""" First, recover information about the primary
		"""

		# primary = dataclasses.get_most_energetic_primary(mctree)
		# pnu = primary.energy/I3Units.eV
		# pnu = primary.energy
		for particle in mctree:
			print(particle)

		# print(primary)

		# print(primary)
		# print(primary.energy)
		# primary = mctree.get_most_energetic_primary()
		# print(primary.Get('energy'))
		# for particle in frame.Get('I3MCTree'):

	def DAQ(self, frame):
		self.recover_factors(frame)
		self.PushFrame(frame)






