#include <icetradio/dataclasses/I3Hammer.h>

template <typename Archive>
void I3Hammer::serialize(Archive &ar, unsigned version)
{
	ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
	ar & make_nvp("height", height_);
}

std::ostream& I3Hammer::Print(std::ostream& oss) const{
	oss << "[         height: " << height_ << std::endl;
	oss << "]";
	return oss;
}


std::ostream& operator<<(std::ostream& oss, const I3Hammer& p){
  return(p.Print(oss));
}

// instantiate templates
I3_SERIALIZABLE(I3Hammer);