#include <icetray/load_project.h>
#include <public/dataclasses/I3RayTraceRecord.h>

void register_I3RayTraceRecord()
{
	namespace bp = boost::python;

	bp::class<I3RayTraceRecord, I3RayTraceRecord, bp::bases<I3FrameObject> >("I3RayTraceRecord")
		.def_readwrite("num_solutions", &I3RayTraceRecord::number)
	;
}

I3_PYTHON_MODULE(icetradio)
{
	load_project("icetradio", false);

	register_I3RayTraceRecord();
}