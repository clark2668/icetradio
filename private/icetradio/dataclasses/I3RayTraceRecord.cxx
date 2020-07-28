#include <icetradio/dataclasses/I3RayTraceRecord.h>

template <typename Archive>
void I3RayTraceRecord::serialize(Archive &ar, unsigned version)
{
	ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
	ar & make_nvp("num_solutions", num_solutions);
}

std::ostream& I3RayTraceRecord::Print(std::ostream& oss) const{
	oss << "[num_solutions: " << num_solutions << std::endl;
	oss << "]";
	return oss;
}

// instantiate templates
I3_SERIALIZABLE(I3RayTraceRecord);