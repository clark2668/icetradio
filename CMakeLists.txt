i3_project(icetradio
	PYTHON_DIR python
)

i3_add_library(icetradio
	private/icetradio/dataclasses/I3RayTraceRecord.cxx
	private/icetradio/dataclasses/I3RayTraceSolution.cxx

	USE_TOOLS boost python
	USE_PROJECTS icetray dataclasses serialization
)

i3_add_pybindings(icetradio
	private/pybindings/module.cxx

	USE_TOOLS boost python
	USE_PROJECTS icetray dataclasses icetradio
)