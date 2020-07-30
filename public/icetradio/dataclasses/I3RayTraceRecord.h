#ifndef RAYTRACERECORD_H
#define RAYTRACERECORD_H

#include <icetray/I3FrameObject.h>
#include <icetray/serialization.h>
#include <dataclasses/I3Position.h>
#include <dataclasses/I3Vector.h>
#include <icetradio/dataclasses/I3RayTraceSolution.h>

class I3RayTraceRecord : public I3FrameObject {
public:
	int numSolutions;
	I3Vector<I3RayTraceSolution> solutions;
	std::ostream& Print(std::ostream&) const override;

private:
	friend class icecube::serialization::access;
	template <typename Archive> void serialize(Archive &ar, unsigned versfion);
};

I3_POINTER_TYPEDEFS(I3RayTraceRecord);

#endif // RAYTRACERECORD_H
