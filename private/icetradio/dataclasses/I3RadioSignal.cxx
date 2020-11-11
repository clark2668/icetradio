#include <icetradio/dataclasses/I3RadioSignal.h>

template <typename Archive>
void I3RadioSignal::serialize(Archive &ar, unsigned version)
{
	ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
	ar & make_nvp("sol_num", sol_num);
	ar & make_nvp("sol_type", sol_type);
	ar & make_nvp("view_angle", view_angle);
	ar & make_nvp("arrival_theta", arrival_theta);
	ar & make_nvp("arrival_phi", arrival_phi);
	ar & make_nvp("polarization_vector", polarization_vector);
	ar & make_nvp("field_noatt", field_noatt);
	ar & make_nvp("field_watt", field_watt);
}

std::ostream& I3RadioSignal::Print(std::ostream& oss) const{
	oss << "[         sol num: " << sol_num << std::endl;
	oss << "[         sol type: " << sol_type << std::endl;
	oss << "[         view angle: " << view_angle << std::endl;
	oss << "]";
	return oss;
}

std::ostream& operator<<(std::ostream& oss, const I3RadioSignal& p){
  return(p.Print(oss));
}

// instantiate templates
I3_SERIALIZABLE(I3RadioSignal);