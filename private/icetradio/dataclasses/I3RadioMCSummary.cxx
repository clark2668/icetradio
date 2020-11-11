#include <icetradio/dataclasses/I3RadioMCSummary.h>

template <typename Archive>
void I3RadioMCSummary::serialize(Archive &ar, unsigned version)
{
	ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
	ar & make_nvp("ray_trace_record", ray_trace_record);
	ar & make_nvp("signals", signals);
}

std::ostream& I3RadioMCSummary::Print(std::ostream& oss) const{
	oss << "[         num ray trace record solutions: " << ray_trace_record.numSolutions << std::endl;
	oss << "]";
	return oss;
}

std::ostream& operator<<(std::ostream& oss, const I3RadioMCSummary& p){
  return(p.Print(oss));
}

// instantiate templates
I3_SERIALIZABLE(I3RadioMCSummary);
I3_SERIALIZABLE(I3IceAntennaRadioMCSummaryMap);
I3_SERIALIZABLE(I3ParticleRadioMCSummaryMap);