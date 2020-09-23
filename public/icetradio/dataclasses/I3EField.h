#ifndef EFIELD_H
#define EFIELD_H

#include <icetray/I3FrameObject.h>
#include <icetray/serialization.h>
#include <dataclasses/I3Vector.h>
#include <icetradio/dataclasses/I3Trace.h>


class I3EField : public I3FrameObject {
public:
	I3Trace eR;
	I3Trace eTheta;
	I3Trace ePhi;

	// TODO: find a way to enforce that eR, eTheta, and ePhi all have the same length, sampling rate, etc.
	// TODO: support setting eR, eThta, and ePhi all at the same time
	
	std::ostream& Print(std::ostream&) const override;

	bool operator==(const I3EField& rhs) const {
		return eR == rhs.eR;
	}

private:
	friend class icecube::serialization::access;
	template <typename Archive> void serialize(Archive &ar, unsigned versfion);
};

std::ostream& operator<<(std::ostream& oss, const I3EField& p);

I3_POINTER_TYPEDEFS(I3EField);

typedef I3Vector<I3EField> I3VectorI3EField;
I3_POINTER_TYPEDEFS(I3VectorI3EField);

#endif // EFIELD_H
