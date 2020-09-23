#ifndef Trace_H
#define Trace_H

#include <icetray/I3FrameObject.h>
#include <icetray/serialization.h>
#include <dataclasses/I3Position.h>
#include <dataclasses/I3Vector.h>

class I3Trace : public I3FrameObject {
private:

    /**  
     * Time (in ns) of when the trace started
     */
	double traceStartTime_;

    /**  
     * The sampling rate (in GHz) of the trace
     */
	double samplingRate_;

    /**  
     * Holds the trace samples (probably voltages)
     */	
	std::vector<double> trace_;

public:

	void SetTrace( std::vector<double>& trace_in, double samplingRate_in){ 
		trace_ = trace_in;
		samplingRate_ = samplingRate_in;
	}
	std::vector<double>& GetTrace() { return trace_; }

	void SetTraceStartTime (double t){ traceStartTime_ = t; }
	double GetTraceStartTime() { return traceStartTime_; }

	double GetSamplingRate() { return samplingRate_; }

	std::ostream& Print(std::ostream&) const override;

	bool operator==(const I3Trace& lhs, const I3Trace& rhs) const {
		return (lhs.GetTraceStartTime() == rhs.GetTraceStartTime());
	}

private:

	friend class icecube::serialization::access;
	template <typename Archive> void serialize(Archive &ar, unsigned versfion);
};

std::ostream& operator<<(std::ostream& oss, const I3VectorI3Trace& p);

I3_POINTER_TYPEDEFS(I3VectorI3Trace);

typedef I3Vector<I3EField> I3VectorI3Trace;
I3_POINTER_TYPEDEFS(I3VectorI3Trace);

#endif // Trace_H
