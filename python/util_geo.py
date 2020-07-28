from icecube import icetray, dataclasses

z_surface = dataclasses.I3Constants.SurfaceElev \
			- dataclasses.I3Constants.OriginElev

def convert_i3_to_global(input_position):
	"""
	Convert from IceCube to surface oriented coordinates

	But because radio calculations need to know the depth of the interaction 
	relative to the surface in order to get the n(z) correct,
	we must convert from "z" in icecube coordinates to 
	"depth" relative to the surface.

	See https://wiki.icecube.wisc.edu/index.php/Coordinate_system#Documentation
	for further discussion.

	Parameters
	----------
	input_position: I3Position
		location in the I3 coordinate system

	Returns
	-------
	output_position: I3Position
		location in the surface oriented coordinate system
	"""

	z_in = input_position.z
	z_out = - (z_surface - z_in)

	output_position = dataclasses.I3Position(input_position.x,
		input_position.y,
		z_out
	)

	return output_position