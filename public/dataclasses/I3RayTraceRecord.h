#ifndef RAYTRACERECORD_H
#define RAYTRACERECORD_H

#include <icetray/I3FrameObject.h>
#include <icetray/serialization.h>

class I3RayTraceRecord : public I3FrameObject {
public:
	int num_solutions;

private:
	friend class icecube::serialization::access;
	template <typename Archive>
	void serialize(Archive &ar, unsigned version);
};

I3_POINTER_TYPEDEFS(I3RayTraceRecord);

#endif
