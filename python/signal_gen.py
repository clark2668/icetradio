# python includes
import numpy as np

from icecube import icetray, dataclasses
from icecube.icetray import I3Units

# we need the NuRadioMC signal propagator module
from NuRadioMC.SignalGen import askaryan

# TODO add GSL RNG as service
# TODO add setting of seed from GSL RNG service

class SignalGen(icetray.I3Module):
	
	def __init__(self, context):
		icetray.I3Module.__init__(self, context)
		
		self._default_askaryan_mode='Alvarez2009'
		
		self.AddParameter("askaryan_model", 
			"What is the Askaryan model to use.",
			self._default_askaryan_mode)

	def Configure(self):

		self._askaryan_model = self.GetParameter("askaryan_model")

	# def get_emission(frame):

		# spectrum = askaryan.get_frequency_spectrum(
		# 	energy * fhad
		# 	viewing_angle
		# 	n_samples
		# 	dt
		# 	"HAD"
		# 	n_index
		# 	R
		# 	model
		# 	seed

		# 	)


	def recover_factors(self, frame):

		mctree = frame.Get('I3MCTree') # get the I3MCTree
		# print(mctree)

		primary = mctree.primaries[0]
		# print(type(primary))

		# primary = dataclasses.get_most_energetic_primary(mctree)
		daughters = mctree.get_daughters(primary)
		print(daughters)

		# daughters = mctree.children(primary)
		# print(daughters)
		# # print(primaries)
		# if len(primaries) ==1:
		# 	idx=0
		# elif 'I3MCWeightDict' in frame:
		# 	idx = [i for i in range(len(primaries)) if primaries[i].is_neutrino][0]
		# print(idx)

		# etot = 0

		# primary = dataclasses.get_most_energetic_primary(mctree)
		# children = mctree.children(primary)
		# for child in children:
		# 	print(child)
		# 	grandchildren = mctree.children(child)
		# 	for grandchild in grandchildren:
		# 		# print(grandchildren)
		# 		etot+= grandchild.energy

		# print("Etot grandchildren is {}".format(etot))
		# print("Etot primary is {}".format(primary.energy))
		# print("About to print the children")
		# print(children)
		# print(dataclasses.number_of_children(primary.number_of_children))
		# pnu = primary.energy/I3Units.eV
		# pnu = primary.energy
		# for particle in mctree:
			# print(particle)

		# print(primary)

		# print(primary)
		# print(primary.energy)
		# primary = mctree.get_most_energetic_primary()
		# print(primary.Get('energy'))
		# for particle in frame.Get('I3MCTree'):

	def Physics(self, frame):
		# self.get_emission(frame)
		# self.recover_factors(frame)
		self.PushFrame(frame)






