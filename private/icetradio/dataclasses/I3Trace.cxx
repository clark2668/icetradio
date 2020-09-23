#include <icetradio/dataclasses/I3Trace.h>

template <typename Archive>
void I3Trace::serialize(Archive &ar, unsigned version)
{
	ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
	ar & make_nvp("traceStartTime_", traceStartTime_);
	ar & make_nvp("samplingRate_", samplingRate_);
	ar & make_nvp("trace_", trace_);
}

std::ostream& I3Trace::Print(std::ostream& oss) const{
	oss << "[         trace start time: " << traceStartTime_ << std::endl;
	oss << "             sampling rate: " << samplingRate_ << std::endl;
	oss << "]";
	return oss;
}

std::ostream& operator<<(std::ostream& oss, const I3Trace& p){
  return(p.Print(oss));
}

// instantiate templates
I3_SERIALIZABLE(I3Trace);