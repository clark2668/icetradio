#ifndef TRACE_H
#define TRACE_H

#include <icetray/I3FrameObject.h>
#include <icetray/serialization.h>
#include <dataclasses/I3Vector.h>

class I3Trace : public I3FrameObject {
public:

    /**  
     * Time (in ns) of when the trace started
     */
	double traceStartTime;

    /**  
     * The sampling rate (in GHz) of the trace
     */
	double samplingRate;

    /**  
     * Holds the trace samples (probably voltages)
     */	
	std::vector<double> trace;


	std::ostream& Print(std::ostream&) const override;

	bool operator==(const I3Trace& rhs) const {
		return traceStartTime == rhs.traceStartTime;
	}

private:
	friend class icecube::serialization::access;
	template <typename Archive> void serialize(Archive &ar, unsigned versfion);
};

std::ostream& operator<<(std::ostream& oss, const I3Trace& p);

I3_POINTER_TYPEDEFS(I3Trace);

typedef I3Vector<I3Trace> I3VectorI3Trace;
I3_POINTER_TYPEDEFS(I3VectorI3Trace);

#endif // TRACE_H
