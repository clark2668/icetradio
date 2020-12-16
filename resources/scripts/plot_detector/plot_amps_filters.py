import matplotlib.pyplot as plt
import numpy as np

from icecube import icetray, icetradio
from icecube.icetradio import det_response

response = det_response.load_filter_amplifier_response('ara_amps_filter')

fig, axs = plt.subplots(1,2,figsize=(10,5))
axs[0].plot(response['frequencies'], response['gain'])
axs[0].set_ylabel('Gain (unitless)')
axs[0].set_xlabel('Frequency (MHz)')

axs[1].plot(response['frequencies'], np.unwrap(response['phase']))
axs[1].set_ylabel('Unwrapped phase (rad)')
axs[1].set_xlabel('Frequency (MHz)')
plt.tight_layout()
fig.savefig('system_response.png')


