.. _iceradio:

icetradio
~~~~~~~~~

Author and Maintainer: Brian Clark

Overview
========

icetradio is a tool for doing radio simulations in an IceTray framework.

icetradio is currently written to be "NuRadioMC under the hood" 
with IceTray functioning as the steering modules.

Philosophy
==========

icetradio is mainly written in python. This is because all of the modern tools 
for doing radio neutrino simulation are written in python, 
specifically NuRadioMC and PyREx. 

In order to allow information to be written to disk in I3 format, 
icetradio also includes some dataclasses, which are naturally written in cpp. 
The general philosophy is that the simulation operations should 
live within python for as long as possible, and only use the dataclasses 
when it's time to read/write things from/to disk. 
As a result, the dataclasses are *intentionally* primitive.

