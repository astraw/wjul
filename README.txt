========================================
wjUL - Python UniversalLibrary for Linux
========================================

wjUL is a Python wrapper for Warren Jasper's mcclibhid_ library. wjUL
runs on Linux, but endeavors to be compatible with
PyUniversalLibrary_, which runs on Windows. Eventually, wjUL may
support more devices than the USB devices supported by the mcclibhid_
library.

`Andrew Straw`_ is the author of wjUL.

.. _mcclibhid: ftp://lx10.tx.ncsu.edu/pub/Linux/drivers/USB
.. _PyUniversalLibrary: https://code.astraw.com/projects/PyUniversalLibrary/
.. _Andrew Straw: http://www.its.caltech.edu/~astraw/

Release history
---------------

(See the Download and install section to download.)

wjUL - the Python package
 * 2007-12-04 - released version 0.2.1 (fixes minor packaging bugs)
 * 2007-11-26 - released version 0.1

mcclibhid - the Ubuntu package of Warren Jasper's code
 * 2007-11-26 - released version 1.21-0ads4

Download and install
--------------------

 1. Install Warren Jasper's mcclibhid library. On Ubuntu Gutsy (7.10)
 i386, this is available at libmcclibhid_1.21-0ads4_i386.deb_. You can
 test this program, and your USB1208FS device, by typing
 "testusb1208FS" at the command prompt. You should get a text-based
 menu system that allows you to blink the light, perform analog output
 and input.

.. _libmcclibhid_1.21-0ads4_i386.deb: http://debs.astraw.com/gutsy/libmcclibhid_1.21-0ads4_i386.deb

 2. Install the wjUL library. On Ubuntu Gutsy (7.10) i386, this is
 available at python-wjul_0.2.1-0ads1_all.deb_. The source code,
 containing example programs, is python-wjul_0.2.1.orig.tar.gz_.

.. _python-wjul_0.2.1-0ads1_all.deb: http://debs.astraw.com/gutsy/python-wjul_0.2.1-0ads1_all.deb
.. _python-wjul_0.2.1.orig.tar.gz: http://debs.astraw.com/gutsy/python-wjul_0.2.1.orig.tar.gz

Usage Notes
-----------

You may need to unplug and re-plug the USB device to get permissions
to access it.

Simple Usage Example
--------------------

Here is an example program (included with the source as
examples/analog_input_scan.py). After downloading and installing wjUL,
numpy_, and matplotlib_, run this Python script::

  import wjUL.UL as UL
  import numpy
  import pylab

  BoardNum = 0
  Gain = UL.BIP5VOLTS

  LowChan = 0
  HighChan = 0

  Count = 1000
  Rate = 1000

  Options = UL.CONVERTDATA
  ADData = numpy.zeros((Count,), numpy.int16)
  Rate = UL.cbAInScan(BoardNum, LowChan, HighChan, Count,
                      Rate, Gain, ADData, Options)

  ADData_volts = [ UL.cbToEngUnits(BoardNum, Gain, adc_unit) for adc_unit in ADData]

  time = numpy.arange( ADData.shape[0] )/float(Rate)

  pylab.plot( time, ADData_volts )
  pylab.xlabel( 'time (sec)')
  pylab.ylabel( 'ADC input (V)')
  pylab.show()

.. _numpy: http://scipy.org/NumPy
.. _matplotlib: http://matplotlib.sourceforge.net/

Work in Progress
----------------

I have only tested the analog input and output capabilities of the
USB1208FS device. I do not expect other devices or components of this
device to work, although I don't anticipate adding support would be
particularly difficult.
