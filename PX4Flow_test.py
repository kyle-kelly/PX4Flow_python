"""
A script to communicate with PX4Flow from the command line
https://gist.github.com/claymcleod/b670285f334acd56ad1c
"""
import sys,os
import curses
import PX4Flow_I2C as px4f
import smbus
import time

def draw_menu(stdscr):

    #On I2C bus 1
	bus = smbus.SMBus(1)
	#Default address from docs (hardware assigned)
	address = 0x42

	#Create sensor instance
	px4flow = px4f.PX4Flow_I2C(bus, address)

	# Clear and refresh the screen for a blank canvas
	stdscr.clear()
	stdscr.refresh()

	# Start colors in curses
	curses.start_color()
	curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

	# Loop where k is the last character pressed
	while (True):

		# Initialization
		stdscr.clear()
		height, width = stdscr.getmaxyx()

		# Declaration of strings
		title = "PX4Flow Optical Sensor Test"[:width-1]

		#I2C frame values
		px4flow.update()
		#print "counts created I2C frames [#frames] :\t{}".format(px4flow.frame_count)
		#print px4flow.pixel_flow_x_sum #latest x flow measurement in pixels*10 [pixels]
		#print px4flow.pixel_flow_y_sum #latest y flow measurement in pixels*10 [pixels]
		x_vel ="X velocity:\t{}\tm/s".format(px4flow.flow_comp_m_x/1000.00)[:width-1] #x velocity*1000 [meters/sec]
		y_vel = "Y velocity:\t{}\tm/s".format(px4flow.flow_comp_m_y/1000.00)[:width-1] #y velocity*1000 [meters/sec]
		x_rot = "Rotation about X:\t{}\tdeg/s".format(px4flow.gyro_x_rate/3.14*180.0)[:width-1] #latest gyro x rate [rad/sec]
		y_rot = "Rotation about Y:\t{}\tdeg/s".format(px4flow.gyro_y_rate/3.14*180.0)[:width-1] #latest gyro y rate [rad/sec]
		z_rot = "Rotation about Z:\t{}\tdeg/s".format(px4flow.gyro_z_rate/3.14*180.0)[:width-1] #latest gyro z rate [rad/sec]
		ground_dist = "Ground Distance:\t{}\tm".format(px4flow.ground_distance/1000.0)[:width-1] #Ground distance in meters*1000 [meters]. Positive value: distance known. Negative value: Unknown distance
		gyro_range = "Gyro range:\t{}\t".format(px4flow.gyro_range)[:width-1] #gyro range [0 .. 7] equals [50 deg/sec .. 2000 deg/sec]
		#print px4flow.sonar_timestamp #time since last sonar update [milliseconds]


		#Integral I2C frame values
		px4flow.integral_update()
		px4flow.frame_count_since_last_readout #number of flow measurements since last I2C readout [#frames]
		px4flow.pixel_flow_x_integral #accumulated flow in radians*10000 around x axis since last I2C readout [rad*10000]
		px4flow.pixel_flow_y_integral #accumulated flow in radians*10000 around y axis since last I2C readout [rad*10000]
		px4flow.gyro_x_rate_integral #accumulated gyro x rates in radians*10000 since last I2C readout [rad*10000] 
		px4flow.gyro_y_rate_integral #accumulated gyro y rates in radians*10000 since last I2C readout [rad*10000] 
		px4flow.gyro_z_rate_integral #accumulated gyro z rates in radians*10000 since last I2C readout [rad*10000] 
		px4flow.integration_timespan #accumulation timespan in microseconds since last I2C readout [microseconds]
		px4flow.sonar_timestamp # time since last sonar update [microseconds]
		px4flow.ground_distance # Ground distance in meters*1000 [meters*1000]
		px4flow.gyro_temperature # Temperature * 100 in centi-degrees Celsius [degcelsius*100]
		px4flow.quality # averaged quality of accumulated flow values [0:bad quality;255: max quality]

		# Centering calculations
		start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
		start_y = int((height // 2) - 15)

		# Turning on attributes for title
		stdscr.attron(curses.color_pair(2))
		stdscr.attron(curses.A_BOLD)

		# Rendering title
		stdscr.addstr(start_y, start_x_title, title)

		# Turning off attributes for title
		stdscr.attroff(curses.color_pair(2))
		stdscr.attroff(curses.A_BOLD)

		# Print rest of text
		stdscr.addstr(start_y + 3, start_x_title, x_vel)
		stdscr.addstr(start_y + 5, start_x_title, y_vel)
		stdscr.addstr(start_y + 7, start_x_title, x_rot)
		stdscr.addstr(start_y + 9, start_x_title, y_rot)
		stdscr.addstr(start_y + 11, start_x_title, z_rot)
		stdscr.addstr(start_y + 13, start_x_title, ground_dist)
		stdscr.addstr(start_y + 15, start_x_title, gyro_range)

		# Refresh the screen
		stdscr.refresh()


def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()