#include <icetradio/dataclasses/I3RayTraceRecord.h>

template <typename Archive>
void I3RayTraceRecord::serialize(Archive &ar, unsigned version)
{
	ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
	ar & make_nvp("num_solutions", num_solutions);
}

// instantiate templates
I3_SERIALIZABLE(I3RayTraceRecord);