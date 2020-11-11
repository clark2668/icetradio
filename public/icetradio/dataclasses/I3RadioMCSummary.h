#ifndef RADIOMCSUMMARY_H
#define RADIOMCSUMMARY_H

#include <icetray/I3FrameObject.h>
#include <icetray/serialization.h>
#include <dataclasses/I3Vector.h>
#include <dataclasses/I3Map.h>
#include <icetradio/dataclasses/I3RayTraceRecord.h>
#include <icetradio/dataclasses/I3RadioSignal.h>
#include <dataclasses/IceAntennaKey.h>



class I3RadioMCSummary : public I3FrameObject {
public:
	I3RayTraceRecord ray_trace_record
	I3Vector<I3RadioSignal> signals;

	std::ostream& Print(std::ostream&) const override;

	bool operator==(const I3RadioMCSummary& rhs) const {
		return  ray_trace_record == rhs.ray_trace_record;
	}

private:
	friend class icecube::serialization::access;
	template <typename Archive> void serialize(Archive &ar, unsigned version);
};

std::ostream& operator<<(std::ostream& oss, const I3RadioMCSummary& p);

I3_POINTER_TYPEDEFS(I3RadioMCSummary);

typedef I3Map<IceAntennaKey, I3RadioMCSummary> I3IceAntennaRadioMCSummaryMap;
typedef I3Map<int, I3IceAntennaRadioMCSummaryMap> I3ParticleRadioMCSummaryMap;

I3_POINTER_TYPEDEFS(I3IceAntennaRadioMCSummaryMap);
I3_POINTER_TYPEDEFS(I3ParticleRadioMCSummaryMap);


#endif // RADIOMCSUMMARY_H
