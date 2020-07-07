i3_project(icetradio
	)

i3_add_library(icetradio
	USE_TOOLS boost gsl
	USE_PROJECTS icetray dataio dataclasses
	)