.. _dataclasses:

Dataclasses
===========

IceTray Dataclasses
-------------------

In order to store information about antennas in the IceCube GCD file,
we extended the core :code:`dataclasses` found in IceTray/combo.
The extension is strongly templated after what is already done
for OMs and Tanks in IceCube, and was borrowed directly from the folks
who were working on the `Surface Array <https://code.icecube.wisc.edu/projects/icecube/browser/IceCube/sandbox/SurfaceArray>`_
extensions to IceTray.

IceAntennaKey
^^^^^^^^^^^^^

First, we added the :code:`IceAntennaKey` class, which allows us to generate
keys (in the c++ sense) to be used in maps later. These are indexed by their
:code:`stationID` and :code:`antennaID`.


I3IceAntennaGeo
^^^^^^^^^^^^^^^

Second, there is an extension to the geometry classes, specifically the addition
of the :code:`I3IceAntennaGeo` class. The I3IceAntennaGeo specifies for each anntenna:

- Position (x,y,z) (an I3Position)
- Orientation (an I3Direction)
- Rotation (an I3Direction)
- Antenna Type
- Antenna Model

We follow the `NuRadioReco <https://nu-radio.github.io/NuRadioReco/pages/detector_database_fields.html#antenna-table>`_
method for identifying the antenna orientation. This is why we have both the
Orientation and Rotation directions, instead of just 3 Euler angles (which 
would have defined an I3Direction). Please see the linked page for more 
information on their use.

We also create a map object, the :code:`I3IceAntennaGeoMap` which uses
the :code:`IceAntennaKey` as keys to map to geometry objects

Finally, a :code:`I3IceAntennaGeoMap` was added to the `I3Geometry`, which allows
us to write the the map to disk in G frames and access it later.

An example of how to use this is provided in the `scripts <https://github.com/clark2668/icetradio/blob/master/resources/scripts/make_gcd_file/build_geo.py>`_ directory.