#include <icetray/load_project.h>
#include <icetradio/dataclasses/I3RayTraceRecord.h>
#include <icetray/python/dataclass_suite.hpp>

void register_I3RayTraceRecord()
{
	namespace bp = boost::python;

	bp::class_<I3RayTraceRecord, I3RayTraceRecordPtr, bp::bases<I3FrameObject> >("I3RayTraceRecord")
		.def_readwrite("num_solutions", &I3RayTraceRecord::num_solutions)
		.def(bp::dataclass_suite<I3RayTraceRecord>())
	;
}

I3_PYTHON_MODULE(icetradio)
{
	load_project("icetradio", false);

	register_I3RayTraceRecord();
}