"""A script to communicate with PX4Flow from the command line"""

import PX4Flow_I2C as px4f
import smbus
import time
import textwrap

def help():
	print textwrap.dedent("""\
            COMMANDS
            'update': update the I2C frame and print related values
            'integral_update': update the integral I2C frame and print related values
            'quit': quit program
            'help': this menu
            """)

def main():
	"""Initilize I2C parameters and checks for user input"""

	#On I2C bus 1
	bus = smbus.SMBus(1)
	#Default address from docs (hardware assigned)
	address = 0x42

	#Create sensor instance
	px4flow = px4f.PX4Flow_I2C(bus, address)

	print "Initial values:\n"
	#I2C frame values
	print px4flow.frame_count #counts created I2C frames [#frames]
	print px4flow.pixel_flow_x_sum #latest x flow measurement in pixels*10 [pixels]
	print px4flow.pixel_flow_y_sum #latest y flow measurement in pixels*10 [pixels]
	print px4flow.flow_comp_m_x #x velocity*1000 [meters/sec]
	print px4flow.flow_comp_m_y #y velocity*1000 [meters/sec]
	print px4flow.qual #Optical flow quality / confidence [0: bad, 255: maximum quality]
	print px4flow.gyro_x_rate #latest gyro x rate [rad/sec]
	print px4flow.gyro_y_rate #latest gyro y rate [rad/sec]
	print px4flow.gyro_z_rate #latest gyro z rate [rad/sec]
	print px4flow.gyro_range #gyro range [0 .. 7] equals [50 deg/sec .. 2000 deg/sec] 
	print px4flow.sonar_timestamp #time since last sonar update [milliseconds]
	print px4flow.ground_distance #Ground distance in meters*1000 [meters]. Positive value: distance known. Negative value: Unknown distance

	#Integral I2C frame values
	print px4flow.frame_count_since_last_readout #number of flow measurements since last I2C readout [#frames]
	print px4flow.pixel_flow_x_integral #accumulated flow in radians*10000 around x axis since last I2C readout [rad*10000]
	print px4flow.pixel_flow_y_integral #accumulated flow in radians*10000 around y axis since last I2C readout [rad*10000]
	print px4flow.gyro_x_rate_integral #accumulated gyro x rates in radians*10000 since last I2C readout [rad*10000] 
	print px4flow.gyro_y_rate_integral #accumulated gyro y rates in radians*10000 since last I2C readout [rad*10000] 
	print px4flow.gyro_z_rate_integral #accumulated gyro z rates in radians*10000 since last I2C readout [rad*10000] 
	print px4flow.integration_timespan #accumulation timespan in microseconds since last I2C readout [microseconds]
	print px4flow.sonar_timestamp # time since last sonar update [microseconds]
	print px4flow.ground_distance # Ground distance in meters*1000 [meters*1000]
	print px4flow.gyro_temperature # Temperature * 100 in centi-degrees Celsius [degcelsius*100]
	print px4flow.quality # averaged quality of accumulated flow values [0:bad quality;255: max quality]
	
	print "Update I2C Frame:\n"
	px4flow.update()
	#I2C frame values
	print px4flow.frame_count #counts created I2C frames [#frames]
	print px4flow.pixel_flow_x_sum #latest x flow measurement in pixels*10 [pixels]
	print px4flow.pixel_flow_y_sum #latest y flow measurement in pixels*10 [pixels]
	print px4flow.flow_comp_m_x #x velocity*1000 [meters/sec]
	print px4flow.flow_comp_m_y #y velocity*1000 [meters/sec]
	print px4flow.qual #Optical flow quality / confidence [0: bad, 255: maximum quality]
	print px4flow.gyro_x_rate #latest gyro x rate [rad/sec]
	print px4flow.gyro_y_rate #latest gyro y rate [rad/sec]
	print px4flow.gyro_z_rate #latest gyro z rate [rad/sec]
	print px4flow.gyro_range #gyro range [0 .. 7] equals [50 deg/sec .. 2000 deg/sec] 
	print px4flow.sonar_timestamp #time since last sonar update [milliseconds]
	print px4flow.ground_distance #Ground distance in meters*1000 [meters]. Positive value: distance known. Negative value: Unknown distance

	#Integral I2C frame values
	print px4flow.frame_count_since_last_readout #number of flow measurements since last I2C readout [#frames]
	print px4flow.pixel_flow_x_integral #accumulated flow in radians*10000 around x axis since last I2C readout [rad*10000]
	print px4flow.pixel_flow_y_integral #accumulated flow in radians*10000 around y axis since last I2C readout [rad*10000]
	print px4flow.gyro_x_rate_integral #accumulated gyro x rates in radians*10000 since last I2C readout [rad*10000] 
	print px4flow.gyro_y_rate_integral #accumulated gyro y rates in radians*10000 since last I2C readout [rad*10000] 
	print px4flow.gyro_z_rate_integral #accumulated gyro z rates in radians*10000 since last I2C readout [rad*10000] 
	print px4flow.integration_timespan #accumulation timespan in microseconds since last I2C readout [microseconds]
	print px4flow.sonar_timestamp # time since last sonar update [microseconds]
	print px4flow.ground_distance # Ground distance in meters*1000 [meters*1000]
	print px4flow.gyro_temperature # Temperature * 100 in centi-degrees Celsius [degcelsius*100]
	print px4flow.quality # averaged quality of accumulated flow values [0:bad quality;255: max quality]

	print "Update I2C Integral Frame:\n"
	px4flow.integral_update()
	#I2C frame values
	print px4flow.frame_count #counts created I2C frames [#frames]
	print px4flow.pixel_flow_x_sum #latest x flow measurement in pixels*10 [pixels]
	print px4flow.pixel_flow_y_sum #latest y flow measurement in pixels*10 [pixels]
	print px4flow.flow_comp_m_x #x velocity*1000 [meters/sec]
	print px4flow.flow_comp_m_y #y velocity*1000 [meters/sec]
	print px4flow.qual #Optical flow quality / confidence [0: bad, 255: maximum quality]
	print px4flow.gyro_x_rate #latest gyro x rate [rad/sec]
	print px4flow.gyro_y_rate #latest gyro y rate [rad/sec]
	print px4flow.gyro_z_rate #latest gyro z rate [rad/sec]
	print px4flow.gyro_range #gyro range [0 .. 7] equals [50 deg/sec .. 2000 deg/sec] 
	print px4flow.sonar_timestamp #time since last sonar update [milliseconds]
	print px4flow.ground_distance #Ground distance in meters*1000 [meters]. Positive value: distance known. Negative value: Unknown distance

	#Integral I2C frame values
	print px4flow.frame_count_since_last_readout #number of flow measurements since last I2C readout [#frames]
	print px4flow.pixel_flow_x_integral #accumulated flow in radians*10000 around x axis since last I2C readout [rad*10000]
	print px4flow.pixel_flow_y_integral #accumulated flow in radians*10000 around y axis since last I2C readout [rad*10000]
	print px4flow.gyro_x_rate_integral #accumulated gyro x rates in radians*10000 since last I2C readout [rad*10000] 
	print px4flow.gyro_y_rate_integral #accumulated gyro y rates in radians*10000 since last I2C readout [rad*10000] 
	print px4flow.gyro_z_rate_integral #accumulated gyro z rates in radians*10000 since last I2C readout [rad*10000] 
	print px4flow.integration_timespan #accumulation timespan in microseconds since last I2C readout [microseconds]
	print px4flow.sonar_timestamp # time since last sonar update [microseconds]
	print px4flow.ground_distance # Ground distance in meters*1000 [meters*1000]
	print px4flow.gyro_temperature # Temperature * 100 in centi-degrees Celsius [degcelsius*100]
	print px4flow.quality # averaged quality of accumulated flow values [0:bad quality;255: max quality]

	while True:
		
		user_func = raw_input("-->")

		if user_func == 'update':
			px4flow.update()
			#I2C frame values
			#print "counts created I2C frames [#frames] :\t{}".format(px4flow.frame_count)
			#print px4flow.pixel_flow_x_sum #latest x flow measurement in pixels*10 [pixels]
			#print px4flow.pixel_flow_y_sum #latest y flow measurement in pixels*10 [pixels]
			print "X velocity:\t{}\tm/s".format(px4flow.flow_comp_m_x/1000.00) #x velocity*1000 [meters/sec]
			print "Y velocity:\t{}\tm/s".format(px4flow.flow_comp_m_y/1000.00) #y velocity*1000 [meters/sec]
			print "Rotation about X:\t{}\tdeg/s".format(px4flow.gyro_x_rate/3.14*180.0) #latest gyro x rate [rad/sec]
			print "Rotation about Y:\t{}\tdeg/s".format(px4flow.gyro_y_rate/3.14*180.0) #latest gyro y rate [rad/sec]
			print "Rotation about Z:\t{}\tdeg/s".format(px4flow.gyro_z_rate/3.14*180.0) #latest gyro z rate [rad/sec]
			print "Ground Distance:\t{}\tm".format(px4flow.ground_distance/1000.0) #Ground distance in meters*1000 [meters]. Positive value: distance known. Negative value: Unknown distance
			print "Gyro range:\t{}\t".format(px4flow.gyro_range) #gyro range [0 .. 7] equals [50 deg/sec .. 2000 deg/sec] 
			print "Optical flow qualifty \t{}\t".format(px4flow.qual) #Optical flow quality / confidence [0: bad, 255: maximum quality]
			#print px4flow.sonar_timestamp #time since last sonar update [milliseconds]

		elif user_func == 'integral_update':
			px4flow.integral_update()
			#Integral I2C frame values
			print px4flow.frame_count_since_last_readout #number of flow measurements since last I2C readout [#frames]
			print px4flow.pixel_flow_x_integral #accumulated flow in radians*10000 around x axis since last I2C readout [rad*10000]
			print px4flow.pixel_flow_y_integral #accumulated flow in radians*10000 around y axis since last I2C readout [rad*10000]
			print px4flow.gyro_x_rate_integral #accumulated gyro x rates in radians*10000 since last I2C readout [rad*10000] 
			print px4flow.gyro_y_rate_integral #accumulated gyro y rates in radians*10000 since last I2C readout [rad*10000] 
			print px4flow.gyro_z_rate_integral #accumulated gyro z rates in radians*10000 since last I2C readout [rad*10000] 
			print px4flow.integration_timespan #accumulation timespan in microseconds since last I2C readout [microseconds]
			print px4flow.sonar_timestamp # time since last sonar update [microseconds]
			print px4flow.ground_distance # Ground distance in meters*1000 [meters*1000]
			print px4flow.gyro_temperature # Temperature * 100 in centi-degrees Celsius [degcelsius*100]
			print px4flow.quality # averaged quality of accumulated flow values [0:bad quality;255: max quality]
		
		elif user_func == 'help':
			help()

		elif user_func == 'quit':
			quit()
		
		else:
			print "Invalid input. Type 'help' for a list of commands.\n"


if __name__ == "__main__":
    main()
