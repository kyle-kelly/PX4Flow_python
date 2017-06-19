# PX4Flow_python
Python wrapper to communicate with PX4Flow smart camera via SMBus

## PX4Flow_I2C.py
A class to hold I2C frame data from PX4Flow. You must first create a sensor instance:
'''
#Create sensor instance
bus = smbus.SMBus(1) # This will be 1 or 2
address = 0x42 # 7 Bit I2C Address of the Flow Module
px4flow = px4f.PX4Flow_I2C(bus, address)
'''
You can then ping the hardware to update and receive one of two data frames:
'''
#I2C frame values
px4flow.update()
'''
'''
#Integral I2C frame values
px4flow.integral_update()
'''
Then you can call on any of the values.

## PX4Flow_test.py
Run the test to continuously print selected values from the I2C frame. Press 'ctrl + c' to quit.