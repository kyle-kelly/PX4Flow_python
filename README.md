# PX4Flow_python
Python wrapper to communicate with [PX4Flow Smart Camera](https://pixhawk.org/modules/px4flow) via SMBus. The code was designed to run on Python 2.7 on the Raspberry Pi 3. You'll need to [enable I2C communication on the Pi](https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial#i2c-on-pi) and install python-i2c and python-smbus. Then include the following:

```python
import smbus
import PX4Flow_I2C as px4f
```

## PX4Flow_I2C.py
A class to hold I2C frame data from PX4Flow. You must first create a sensor instance:

```python
#Create sensor instance
bus = smbus.SMBus(1) # This will be 1 or 2
address = 0x42 # 7 Bit I2C Address of the Flow Module
px4flow = px4f.PX4Flow_I2C(bus, address)
```

You then ping the hardware to update one of two data frames:

```python
#I2C frame values
px4flow.update()
```

```python
#Integral I2C frame values
px4flow.integral_update()
```

Then you can call on any of the values.

## PX4Flow_test.py
Run the test to continuously print selected values from the I2C frame. Press 'ctrl + c' to quit.