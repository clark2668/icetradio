#include <icetradio/dataclasses/I3EField.h>

template <typename Archive>
void I3EField::serialize(Archive &ar, unsigned version)
{
	ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
	ar & make_nvp("showerID", showerID);
	ar & make_nvp("rayTracingID", rayTracingID);
	ar & make_nvp("azimuth", azimuth);
	ar & make_nvp("zenith", zenith);
}

std::ostream& I3EField::Print(std::ostream& oss) const{
	oss << "[         showerID: " << showerID << std::endl;
	oss << "      rayTracingID: " << rayTracingID << std::endl;
	oss << "           azimuth: " << azimuth << std::endl;
	oss << "            zenith: " << zenith << std::endl;
	oss << "]";
	return oss;
}

std::ostream& operator<<(std::ostream& oss, const I3EField& p){
  return(p.Print(oss));
}

// instantiate templates
I3_SERIALIZABLE(I3EField);