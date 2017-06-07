"""A script to communicate with PX4Flow from the command line"""

import smbus
import time

def help():
	print("""
	i2c_address		Update the I2C address of the PX4Flow
					Valid addresses are 0x42-0x49

	quit				Quits program
	""")

def i2c_address(address):
	"""Updates I2C address for Px4FLOW"""
	new_address = raw_input("Enter new address: ")
	if (new_address >= 0x42 && new_address <= 0x49):
		return new_address
	else:
		print "Invalid address!\n"
		return address

def update(address, bus):
	"""Send 0x0 to PX4FLOW module and receive back 22 bytes of data"""

	bus.write_byte(address, 0x0)

	i2c_frame = bus.read_i2c_block_data(address, 0x00, 22)


def intergal_update(address, bus):
	"""Send 0x16 to PX4FLOW module and receive back 25 bytes of data"""

	bus.write_byte(address, 0x16)

	i2c_integral_frame = bus.read_i2c_block_data(address, 0x16, 25)

def main():
	"""Initilize I2C parameters and checks for user input"""

	#On I2C bus 1
	bus = smbus.SMBus(1)
	#Default address from docs (hardware assigned)
	address = 0x42

	while True:
		
		user_func = raw_input()

		if user_func == 'i2c_address':
			address = i2c_address(address)

		elif user_func == 'update':
			update(address, bus)

		elif user_func == 'integral_update':
			integral_update(address, bus)
		
		elif user_func == 'help':
			help()

		elif user_func == 'quit':
			quit()
		
		else:
			print "Invalid input. Type 'help' for a list of commands.\n"


if __name__ == "__main__":
    main()
