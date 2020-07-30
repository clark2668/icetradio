#include <icetradio/dataclasses/I3RayTraceRecord.h>

// void I3RayTraceRecord::add_element_to_launch_vector(I3Position pos){
// 	launch_vectors.push_back(pos);
// }

template <typename Archive>
void I3RayTraceRecord::serialize(Archive &ar, unsigned version)
{
	ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
	ar & make_nvp("numSolutions", numSolutions);
	ar & make_nvp("solutions", solutions);
}

std::ostream& I3RayTraceRecord::Print(std::ostream& oss) const{
	oss << "[numSolutions: " << numSolutions << std::endl;
	for(auto sample : solutions) oss << solutions << ", ";
	oss << "]";
	return oss;
}

// bool operator==(const I3RayTraceRecord& lhs, const I3RayTraceRecord& rhs)
// {
//   return (lhs.GetNumSolutions() == rhs.GetNumSolutions());
// }

// instantiate templates
I3_SERIALIZABLE(I3RayTraceRecord);