#!/usr/bin/env python
#
#  Interface for the ADXL345 accelerometer via I2C.  Derived from Adafruit's
#  Adafruit_ADXL345 library available at
#
#    https://github.com/adafruit/Adafruit_Python_ADXL345
#
#  Uses the mraa Python bindings provided by Intel to interact with the I2C
#  buses available on the Terasic DE10-Nano SoC.
#
# ==============================================================================
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import struct
import mraa

# Minimal constants carried over from Arduino library
ADXL345_ADDRESS            = 0x53
ADXL345_DEVID              = 0xE5
ADXL345_THRESH_INACT       = 0x25
ADXL345_TIME_INACT         = 0x26
ADXL345_ACT_INACT_CTL      = 0x27
ADXL345_THRESH_FF          = 0x28
ADXL345_TIME_FF            = 0x29
ADXL345_REG_DEVID          = 0x00 # Device ID
ADXL345_REG_TAP_AXES       = 0x2A
ADXL345_REG_ACT_TAP_STATUS = 0x2B # Read-only
ADXL345_REG_BW_RATE        = 0x2C
ADXL345_REG_POWER_CTL      = 0x2D # Power-saving features control
ADXL345_REG_DATA_FORMAT    = 0x31
ADXL345_REG_DATAX0         = 0x32 # X-axis data 0 (6 bytes for X/Y/Z)
ADXL345_DATARATE_0_10_HZ   = 0x00
ADXL345_DATARATE_0_20_HZ   = 0x01
ADXL345_DATARATE_0_39_HZ   = 0x02
ADXL345_DATARATE_0_78_HZ   = 0x03
ADXL345_DATARATE_1_56_HZ   = 0x04
ADXL345_DATARATE_3_13_HZ   = 0x05
ADXL345_DATARATE_6_25HZ    = 0x06
ADXL345_DATARATE_12_5_HZ   = 0x07
ADXL345_DATARATE_25_HZ     = 0x08
ADXL345_DATARATE_50_HZ     = 0x09
ADXL345_DATARATE_100_HZ    = 0x0A # (default)
ADXL345_DATARATE_200_HZ    = 0x0B
ADXL345_DATARATE_400_HZ    = 0x0C
ADXL345_DATARATE_800_HZ    = 0x0D
ADXL345_DATARATE_1600_HZ   = 0x0E
ADXL345_DATARATE_3200_HZ   = 0x0F
ADXL345_POWERCTL_SLEEP     = 0x04
ADXL345_POWERCTL_MEASURE   = 0x08
ADXL345_POWERCTL_AUTOSLEEP = 0x10
ADXL345_POWERCTL_LINK      = 0x20
ADXL345_DATAFMT_JUSTIFY    = 0x04
ADXL345_DATAFMT_FULL_RES   = 0x08
ADXL345_DATAFMT_INT_INVERT = 0x20
ADXL345_DATAFMT_SPI        = 0x40
ADXL345_DATAFMT_SELF_TEST  = 0x80

ADXL345_RANGE_2_G          = 0x00 # +/-  2g (default)
ADXL345_RANGE_4_G          = 0x01 # +/-  4g
ADXL345_RANGE_8_G          = 0x02 # +/-  8g
ADXL345_RANGE_16_G         = 0x03 # +/- 16g

class ADXL345(object):
    """
    ADXL345 triple-axis accelerometer
    """
    def __init__(self, address=ADXL345_ADDRESS, i2c=None, **kwargs):
        """
        Initialize the ADXL345 accelerometer using its I2C interface.  i2c and
        kwargs do nothing; they are retained for compatibility with
        Adafruit_ADXL345.
        """
        self.device = mraa.I2c(0)
        # Check that accelerometer is connected, then enable it
        self.device.address(ADXL345_ADDRESS)

        device_id = self.device.readReg(ADXL345_REG_DEVID)
        if device_id == ADXL345_DEVID:
            # Put device into ready-to-measure mode
            self.device.writeReg(ADXL345_REG_POWER_CTL, ADXL345_POWERCTL_MEASURE)
        else:
            raise RuntimeError('Expected deviceid %02x but got %02x' % (ADXL345_DEVID, device_id))

    def set_range(self, value):
        """
        Set the range of the accelerometer to the provided value.  Range value
        should be one of these constants:
          - ADXL345_RANGE_2_G   = +/-2G
          - ADXL345_RANGE_4_G   = +/-4G
          - ADXL345_RANGE_8_G   = +/-8G
          - ADXL345_RANGE_16_G  = +/-16G
        """
        # Read the data format register to preserve bits.  Update the data
        # rate, make sure that the FULL-RES bit is enabled for range scaling
        format_reg = self.device.readReg(ADXL345_REG_DATA_FORMAT) & ~0x0F
        format_reg |= value
        format_reg |= ADXL345_DATAFMT_FULL_RES
        # Write the updated format register.
        self.device.writeReg(ADXL345_REG_DATA_FORMAT, format_reg)

    def get_range(self):
        """
        Retrieve the current range of the accelerometer.  See set_range for
        the possible range constant values that will be returned.
        """
        return self.device.readReg(ADXL345_REG_DATA_FORMAT) & 0x03

    def set_power_ctl(self, value):
        """
        Change the power control settings register
        """
        self.device.writeReg(ADXL345_REG_POWER_CTL, value)

    def get_power_ctl(self):
        """
        Retrieve the current power control settings.
        """
        return self.device.readReg(ADXL345_REG_POWER_CTL)

    def set_data_rate(self, rate):
        """
        Set the data rate of the aceelerometer.  Rate should be one of the
        following constants:
          - ADXL345_DATARATE_0_10_HZ = 0.1 Hz
          - ADXL345_DATARATE_0_20_HZ = 0.2 Hz
          - ADXL345_DATARATE_0_39_HZ = 0.39 Hz
          - ADXL345_DATARATE_0_78_HZ = 0.78 Hz
          - ADXL345_DATARATE_1_56_HZ = 1.56 Hz
          - ADXL345_DATARATE_3_13_HZ = 3.13 Hz
          - ADXL345_DATARATE_6_25HZ  = 6.25 Hz
          - ADXL345_DATARATE_12_5_HZ = 12.5 Hz
          - ADXL345_DATARATE_25_HZ   = 25 Hz
          - ADXL345_DATARATE_50_HZ   = 50 Hz
          - ADXL345_DATARATE_100_HZ  = 100 Hz
          - ADXL345_DATARATE_200_HZ  = 200 Hz
          - ADXL345_DATARATE_400_HZ  = 400 Hz
          - ADXL345_DATARATE_800_HZ  = 800 Hz
          - ADXL345_DATARATE_1600_HZ = 1600 Hz
          - ADXL345_DATARATE_3200_HZ = 3200 Hz
        """
        # Note: The LOW_POWER bits are currently ignored,
        # we always keep the device in 'normal' mode
        self.device.writeReg(ADXL345_REG_BW_RATE, rate & 0x0F)

    def get_data_rate(self):
        """
        Retrieve the current data rate.  See set_data_rate for the possible
        data rate constant values that will be returned.
        """
        return self.device.readReg(ADXL345_REG_BW_RATE) & 0x0F

    def read(self):
        """
        Read the current value of the accelerometer and return it as a tuple
        of signed 16-bit X, Y, Z axis values.
        """
        raw = self.device.readBytesReg(ADXL345_REG_DATAX0, 6)
        return struct.unpack('<hhh', raw)

    def read_g(self):
        """
        Read the current value of the accelerometer and return it as a tuple
        of signed G measurements for the X, Y, Z axis values.
        """
        raw_x, raw_y, raw_z = self.read()

        # when ADXL345_DATAFMT_FULL_RES is set, each bit is a fixed 0.004 G
        actual_x = raw_x * 0.004
        actual_y = raw_y * 0.004
        actual_z = raw_z * 0.004
        return (actual_x, actual_y, actual_z)
