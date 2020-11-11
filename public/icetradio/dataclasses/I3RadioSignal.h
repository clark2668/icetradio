#ifndef RADIOSIGNAL_H
#define RADIOSIGNAL_H

#include <icetray/I3FrameObject.h>
#include <icetray/serialization.h>
#include <dataclasses/I3Vector.h>
#include <dataclasses/I3Position.h>
#include <icetradio/dataclasses/I3EField.h>


class I3RadioSignal : public I3FrameObject {
public:
	int sol_num; 						///< what ray tracing solution is this associated with
	
	int sol_type; 						///< solution type for the ray tracing
										///< uses same solution definitions as NuRadioMC
										///< 1 = direct, 2 = refracted, 3 = reflected
										///< https://github.com/nu-radio/NuRadioMC/blob/master/NuRadioMC/SignalProp/analyticraytracing.py

	double view_angle; 					///< viewing angle in radians
	double arrival_theta; 				///< theta arrival angle at the antenna, in radians, 0->pi
	double arrival_phi;					///< phi arrival angle at the antenna, in radians, 0->2pi
		
	I3Position polarization_vector;		///< polarization vector

	I3EField field_noatt;				///< E-field at antenna without attenuation
	I3EField field_watt;				///< E-field at antenna with attenuation

	std::ostream& Print(std::ostream&) const override;

	bool operator==(const I3RadioSignal& rhs) const {
		return  sol_num == rhs.sol_num;
	}

private:
	friend class icecube::serialization::access;
	template <typename Archive> void serialize(Archive &ar, unsigned version);
};

std::ostream& operator<<(std::ostream& oss, const I3RadioSignal& p);

I3_POINTER_TYPEDEFS(I3RadioSignal);

typedef I3Vector<I3RadioSignal> I3VectorI3RadioSignal;
I3_POINTER_TYPEDEFS(I3VectorI3RadioSignal);

#endif // RADIOSIGNAL_H
