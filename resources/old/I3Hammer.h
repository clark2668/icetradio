#ifndef HAMMER_H
#define HAMMER_H

#include <icetray/I3FrameObject.h>
#include <icetray/serialization.h>
#include <dataclasses/I3Vector.h>

class I3Hammer : public I3FrameObject {

private:
	double height_;

public:

	I3Hammer() {};
	~I3Hammer() {};

	void SetHeight(double height){ height_ = height; }
	double GetHeight() {return height_; }

	std::ostream& Print(std::ostream&) const override;

	bool operator==(const I3Hammer& rhs) const {
		return height_ == rhs.height_;
	}

private:
	friend class icecube::serialization::access;
	template <typename Archive> void serialize(Archive &ar, unsigned versfion);
};

std::ostream& operator<<(std::ostream& oss, const I3Hammer& p);

I3_POINTER_TYPEDEFS(I3Hammer);

typedef I3Vector<I3Hammer> I3VectorI3Hammer;
I3_POINTER_TYPEDEFS(I3VectorI3Hammer);

#endif // HAMMER_H
