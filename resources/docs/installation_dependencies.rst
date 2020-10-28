Installation and Dependencies
=============================

Installation
============

To install :code:`icetradio`, put the entire repository into your metaproject build folder.

Because :code:`icetradio` uses some external python based dependencies
in the form of git submodules, make sure to :code:`git clone --recursive`.

Dependencies
============

To handle the radio-related simulations (Askaryan signal generation, ray
tracing, etc.) we use the `NuRadioMC <https://github.com/nu-radio/NuRadioMC>`_ 
package, and its dependencies `NuRadioReco <https://github.com/nu-radio/NuRadioReco>`_
and `radiotools <https://github.com/nu-radio/radiotools>`_.

Dependencies are managed in the :code:`extern` directory.
Because we only use :code:`NuRadioMC` as a "backend" of sorts, you generally
do *not* need to install the :code:`NuRadioMC` dependencies for 
:code:`icetradio` to work.
