#include <icetray/load_project.h>
#include <icetray/python/dataclass_suite.hpp>
#include <icetray/python/list_indexing_suite.hpp>
#include <dataclasses/I3Vector.h>
#include <icetradio/dataclasses/I3EField.h>
#include <icetradio/dataclasses/I3RadioSignal.h>
#include <icetradio/dataclasses/I3RayTraceRecord.h>
#include <icetradio/dataclasses/I3RayTraceSolution.h>
#include <icetradio/dataclasses/I3Trace.h>

///////////////////////////////
///////////////////////////////
// I3EField
///////////////////////////////
///////////////////////////////
void register_I3EField()
{
	namespace bp = boost::python;
	bp::class_<I3EField, I3EFieldPtr, bp::bases<I3FrameObject> >("I3EField")

		#define PROPS (eR) (eTheta) (ePhi)
		BOOST_PP_SEQ_FOR_EACH(WRAP_RW, I3EField, PROPS)
		#undef PROPS

		.def(bp::dataclass_suite<I3EField>())
	;
}

void register_I3VectorI3EField()
{
	namespace bp = boost::python;
	bp::class_<I3Vector<I3EField > >("I3VectorI3EField")
		.def(bp::dataclass_suite<I3Vector<I3EField > > ());
}

///////////////////////////////
///////////////////////////////
// I3RadioSignal
///////////////////////////////
///////////////////////////////
void register_I3RadioSignal()
{
	namespace bp = boost::python;
	bp::class_<I3RadioSignal, I3RadioSignalPtr, bp::bases<I3FrameObject> >("I3RadioSignal")

		#define PROPS (sol_num) (sol_type) (view_angle) (arrival_theta) (arrival_phi) (polarization_vector) (field_noatt) (field_watt)
		BOOST_PP_SEQ_FOR_EACH(WRAP_RW, I3RadioSignal, PROPS)
		#undef PROPS

		.def(bp::dataclass_suite<I3RadioSignal>())
	;
}

void register_I3VectorI3RadioSignal()
{
	namespace bp = boost::python;
	bp::class_<I3Vector<I3RadioSignal > >("I3VectorI3RadioSignal")
		.def(bp::dataclass_suite<I3Vector<I3RadioSignal > > ());
}

///////////////////////////////
///////////////////////////////
// I3RayTraceRecord
///////////////////////////////
///////////////////////////////
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

///////////////////////////////
///////////////////////////////
// I3RayTraceSolution
///////////////////////////////
///////////////////////////////
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

void register_I3VectorI3RayTraceSolution()
{
	namespace bp = boost::python;
	bp::class_<I3Vector<I3RayTraceSolution > >("I3VectorI3RayTraceSolution")
		.def(bp::dataclass_suite<I3Vector<I3RayTraceSolution > > ());
}


///////////////////////////////
///////////////////////////////
// I3Trace
///////////////////////////////
///////////////////////////////
void register_I3Trace()
{
	namespace bp = boost::python;
	bp::class_<I3Trace, I3TracePtr, bp::bases<I3FrameObject> >("I3Trace")

		#define PROPS (traceStartTime) (samplingRate) (trace)
		BOOST_PP_SEQ_FOR_EACH(WRAP_RW, I3Trace, PROPS)
		#undef PROPS

		.def(bp::dataclass_suite<I3Trace>())
	;
}

void register_I3VectorI3Trace()
{
	namespace bp = boost::python;
	bp::class_<I3Vector<I3Trace > >("I3VectorI3Trace")
		.def(bp::dataclass_suite<I3Vector<I3Trace > > ());
}

I3_PYTHON_MODULE(icetradio)
{
	load_project("icetradio", false);

	register_I3EField();
	register_I3VectorI3EField();
	register_I3Trace();
	register_I3VectorI3Trace();
	register_I3RayTraceSolution();
	register_I3VectorI3RayTraceSolution();
	register_I3RayTraceRecord();
	register_I3RadioSignal();
	register_I3VectorI3RadioSignal();
}