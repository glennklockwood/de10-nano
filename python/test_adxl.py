#!/usr/bin/env python
"""
Demonstrate functionality of the mraa_adxl345 Python module
"""

import time
import mraa_adxl345

axdl = mraa_adxl345.ADXL345()

print "Power control register:", "{0:#010b}".format(axdl.get_power_ctl())
print "Data rate register:    ", "{0:#010b}".format(axdl.get_data_rate())
print "Data format register:  ", "{0:#010b}".format(axdl.device.readReg(mraa_adxl345.ADXL345_REG_DATA_FORMAT))
print "Data range:            ", "{0:#010b}".format(axdl.get_range())
print "Raw readings:          ", axdl.read()
print "Measured Gs:           ", axdl.read_g()

print "Setting data rate to 100 Hz"
axdl.set_data_rate(mraa_adxl345.ADXL345_DATARATE_100_HZ)

for _ in range(20):
    print "Measured Gs: %7.2f %8.2f %8.2f" % axdl.read_g()
    time.sleep(1)
