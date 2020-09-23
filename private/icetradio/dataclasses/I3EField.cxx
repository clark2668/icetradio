#include <icetradio/dataclasses/I3EField.h>

template <typename Archive>
void I3EField::serialize(Archive &ar, unsigned version)
{
	ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
	ar & make_nvp("eR", eR);
	ar & make_nvp("eTheta", eTheta);
	ar & make_nvp("ePhi", ePhi);
}

std::ostream& I3EField::Print(std::ostream& oss) const{
	oss << "[         eR trace start time: " << eR.traceStartTime << std::endl;
	oss << "]";
	return oss;
}

std::ostream& operator<<(std::ostream& oss, const I3EField& p){
  return(p.Print(oss));
}

// instantiate templates
I3_SERIALIZABLE(I3EField);