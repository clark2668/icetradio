#include <icetradio/dataclasses/I3RayTraceSolution.h>

// void I3RayTraceRecord::add_element_to_launch_vector(I3Position pos){
// 	launch_vectors.push_back(pos);
// }

template <typename Archive>
void I3RayTraceSolution::serialize(Archive &ar, unsigned version)
{
	ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
	ar & make_nvp("solutionNumber", solutionNumber);
	ar & make_nvp("solutionType", solutionType);
	ar & make_nvp("C0", C0);
	ar & make_nvp("C1", C1);
	ar & make_nvp("pathLength", pathLength);
	ar & make_nvp("travelTime", travelTime);
	ar & make_nvp("launchVector", launchVector);
	ar & make_nvp("receiveVector", receiveVector);
}

std::ostream& I3RayTraceSolution::Print(std::ostream& oss) const{
	oss << "[     solutionNumber: " << solutionNumber << std::endl;
	oss << "        solutionType: " << solutionType << std::endl;
	oss << "                  C0: " << C0 << std::endl;
	oss << "                  C1: " << C1 << std::endl;
	oss << "          pathLength: " << pathLength << std::endl;
	oss << "          travelTime: " << travelTime << std::endl;
	oss << "        launchVector: " << launchVector << std::endl;
	oss << "       receiveVector: " << receiveVector << std::endl;
	oss << "]";
	return oss;
}

std::ostream& operator<<(std::ostream& oss, const I3RayTraceSolution& p){
  return(p.Print(oss));
}

// instantiate templates
I3_SERIALIZABLE(I3RayTraceSolution);