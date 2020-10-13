.. _iceradio:

icetradio
~~~~~~~~~

Author and Maintainer: Brian Clark

Overview
========

:code:`icetradio` is a tool for doing radio simulations in an IceTray framework.

:code:`icetradio` is currently written to be "NuRadioMC under the hood" 
with IceTray functioning as the steering modules.

Philosophy
==========

:code:`icetradio` is mainly written in python. This is because all of the modern tools 
for doing radio neutrino simulation are written in python, 
specifically NuRadioMC and PyREx. 

In order to allow information to be written to disk in I3 format, 
:code:`icetradio` also includes some dataclasses, which are naturally written in cpp. 
The general philosophy is that the simulation operations should 
live within python for as long as possible, and only use the dataclasses 
when it's time to read/write things from/to disk. 
As a result, the dataclasses are *intentionally* primitive.

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

