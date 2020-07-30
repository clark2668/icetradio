#include <icetray/load_project.h>
#include <icetray/python/dataclass_suite.hpp>
#include <icetray/python/list_indexing_suite.hpp>
#include <dataclasses/I3Vector.h>
#include <icetradio/dataclasses/I3RayTraceSolution.h>
#include <icetradio/dataclasses/I3RayTraceRecord.h>

void register_I3RayTraceSolution()
{
	namespace bp = boost::python;
	bp::class_<I3RayTraceSolution, I3RayTraceSolutionPtr, bp::bases<I3FrameObject> >("I3RayTraceSolution")

		#define PROPS (solutionNumber) (solutionType) (C0) (C1)  (pathLength) (travelTime) \
		(launchVector) (receiveVector)
		BOOST_PP_SEQ_FOR_EACH(WRAP_RW, I3RayTraceSolution, PROPS)
		#undef PROPS

		.def(bp::dataclass_suite<I3RayTraceSolution>())
	;
}

void register_I3RayTraceRecord()
{
	namespace bp = boost::python;
	bp::class_<I3RayTraceRecord, I3RayTraceRecordPtr, bp::bases<I3FrameObject> >("I3RayTraceRecord")

		#define PROPS (numSolutions) (solutions)
		BOOST_PP_SEQ_FOR_EACH(WRAP_RW, I3RayTraceRecord, PROPS)
		#undef PROPS

		.def(bp::dataclass_suite<I3RayTraceRecord>())
	;
}

void register_I3VectorI3RayTraceSolution()
{
	namespace bp = boost::python;
	
	bp::class_<I3Vector<I3RayTraceSolution > >("I3VectorI3RayTraceSolution")
		.def(bp::dataclass_suite<I3Vector<I3RayTraceSolution > > ());
}



I3_PYTHON_MODULE(icetradio)
{
	load_project("icetradio", false);

	register_I3RayTraceSolution();
	register_I3VectorI3RayTraceSolution();
	register_I3RayTraceRecord();
}