#ifndef EField_H
#define EField_H

#include <icetray/I3FrameObject.h>
#include <icetray/serialization.h>
#include <dataclasses/I3Position.h>
#include <dataclasses/I3Vector.h>

class I3EField : public I3FrameObject {
public:
	int showerID;
	int rayTracingID;
	double azimuth;
	double zenith;
	std::ostream& Print(std::ostream&) const override;

	bool operator==(const I3VectorI3EField& rhs) const {
		return showerID == rhs.showerID;
	}

private:
	friend class icecube::serialization::access;
	template <typename Archive> void serialize(Archive &ar, unsigned versfion);
};

std::ostream& operator<<(std::ostream& oss, const I3VectorI3EField& p);

I3_POINTER_TYPEDEFS(I3VectorI3EField);

typedef I3Vector<I3EField> I3VectorI3EField;
I3_POINTER_TYPEDEFS(I3VectorI3EField);

#endif // EField_H
