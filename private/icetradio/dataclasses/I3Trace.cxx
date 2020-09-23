#include <icetradio/dataclasses/I3Trace.h>

template <typename Archive>
void I3Trace::serialize(Archive &ar, unsigned version)
{
	ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
	ar & make_nvp("traceStartTime", traceStartTime);
	ar & make_nvp("samplingRate", samplingRate);
	ar & make_nvp("trace", trace);
}

std::ostream& I3Trace::Print(std::ostream& oss) const{
	oss << "[         trace start time: " << traceStartTime << std::endl;
	oss << "             sampling rate: " << samplingRate << std::endl;
	oss << "]";
	return oss;
}


std::ostream& operator<<(std::ostream& oss, const I3Trace& p){
  return(p.Print(oss));
}

// instantiate templates
I3_SERIALIZABLE(I3Trace);