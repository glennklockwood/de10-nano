This repository contains code that exercises the features of Terasic's DE10-Nano
SoC dev board.

- `mraa_adxl345.py` - provides a Python interface for ADXL345 accelerometers
  connected via I2C using the MRAA library's Python bindings.
- `test_adxl.py` - use the `mraa_adxl345` module above to exercise a few
  features of the ADXL345 accelerometer as integrated in the DE10-Nano SoC
  board.
