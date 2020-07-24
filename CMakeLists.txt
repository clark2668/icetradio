i3_project(icetradio
	PYTHON_DIR python
)

i3_add_library(icetradio
	private/dataclasses/I3RayTraceRecord.cxx

	USE_TOOLS boost python
	USE_PROJECTS icetray dataclasses serialization
)