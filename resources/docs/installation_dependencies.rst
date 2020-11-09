.. _installation_dependencies:

Installation and Dependencies
=============================

Installation
------------

We recommend use of cvmfs py3-4.1.1.

To install :code:`icetradio`, put the entire repository into your metaproject build folder.

Because :code:`icetradio` uses some external python based dependencies
in the form of git submodules, make sure to :code:`git clone --recursive`.

IceCube Dependencies
------------

:code:`icetradio` relies on a working installation of the IceCube :code:`combo`
metaproject. In order to have GCD files that contain radio antennas, we are using
a customized version of the :code:`I3Geometry` class. So, please download 
and compile the version of combo in Brian Clark's `sandbox <http://code.icecube.wisc.edu/svn/sandbox/brianclark/ehe/radio/trunk/>`_
(requires IceCube credentials).

For more information on the changes made to the dataclasses, look `here <https://github.com/clark2668/icetradio/blob/master/resources/docs/dataclasses.rst>`_.


External Dependencies
------------

To handle the radio-related simulations (Askaryan signal generation, ray
tracing, etc.) we use the `NuRadioMC <https://github.com/nu-radio/NuRadioMC>`_ 
package, and its dependencies `NuRadioReco <https://github.com/nu-radio/NuRadioReco>`_
and `radiotools <https://github.com/nu-radio/radiotools>`_.

Dependencies are managed in the :code:`extern` directory.
Because we only use :code:`NuRadioMC` as a "backend" of sorts, you generally
do *not* need to install the :code:`NuRadioMC` dependencies for 
:code:`icetradio` to work.
