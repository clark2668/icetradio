#ifndef RAYTRACESOLUTION_H
#define RAYTRACESOLUTION_H

#include <icetray/I3FrameObject.h>
#include <icetray/serialization.h>
#include <dataclasses/I3Position.h>
#include <dataclasses/I3Vector.h>

class I3RayTraceSolution : public I3FrameObject {
public:
	double C0;
	double C1;
	int solutionNumber;
	int solutionType;
	double pathLength;
	double travelTime;
	I3Position launchVector;
	I3Position receiveVector;
	std::ostream& Print(std::ostream&) const override;

	bool operator==(const I3RayTraceSolution& rhs) const {
		return C0 == rhs.C0;
	}

private:
	friend class icecube::serialization::access;
	template <typename Archive> void serialize(Archive &ar, unsigned versfion);
};

std::ostream& operator<<(std::ostream& oss, const I3RayTraceSolution& p);

I3_POINTER_TYPEDEFS(I3RayTraceSolution);

typedef I3Vector<I3RayTraceSolution> I3VectorI3RayTraceSolution;
I3_POINTER_TYPEDEFS(I3VectorI3RayTraceSolution);

#endif // RAYTRACESOLUTION_H
