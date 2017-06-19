import smbus
import time

class PX4Flow_I2C(object):
	"""
	Class to hold I2C frame data from PX4Flow

	typedef struct i2c_frame
	{
	    uint16_t frame_count;// counts created I2C frames [#frames]
	    int16_t pixel_flow_x_sum;// latest x flow measurement in pixels*10 [pixels]
	    int16_t pixel_flow_y_sum;// latest y flow measurement in pixels*10 [pixels]
	    int16_t flow_comp_m_x;// x velocity*1000 [meters/sec]
	    int16_t flow_comp_m_y;// y velocity*1000 [meters/sec]
	    int16_t qual;// Optical flow quality / confidence [0: bad, 255: maximum quality]
	    int16_t gyro_x_rate; // latest gyro x rate [rad/sec]
	    int16_t gyro_y_rate; // latest gyro y rate [rad/sec]
	    int16_t gyro_z_rate; // latest gyro z rate [rad/sec]
	    uint8_t gyro_range; // gyro range [0 .. 7] equals [50 deg/sec .. 2000 deg/sec] 
	    uint8_t sonar_timestamp;// time since last sonar update [milliseconds]
	    int16_t ground_distance;// Ground distance in meters*1000 [meters]. Positive value: distance known. Negative value: Unknown distance
	} i2c_frame;

		typedef struct i2c_integral_frame
	{
	    uint16_t frame_count_since_last_readout;//number of flow measurements since last I2C readout [#frames]
	    int16_t pixel_flow_x_integral;//accumulated flow in radians*10000 around x axis since last I2C readout [rad*10000]
	    int16_t pixel_flow_y_integral;//accumulated flow in radians*10000 around y axis since last I2C readout [rad*10000]
	    int16_t gyro_x_rate_integral;//accumulated gyro x rates in radians*10000 since last I2C readout [rad*10000] 
	    int16_t gyro_y_rate_integral;//accumulated gyro y rates in radians*10000 since last I2C readout [rad*10000] 
	    int16_t gyro_z_rate_integral;//accumulated gyro z rates in radians*10000 since last I2C readout [rad*10000] 
	    uint32_t integration_timespan;//accumulation timespan in microseconds since last I2C readout [microseconds]
	    uint32_t sonar_timestamp;// time since last sonar update [microseconds]
	    int16_t ground_distance;// Ground distance in meters*1000 [meters*1000]
	    int16_t gyro_temperature;// Temperature * 100 in centi-degrees Celsius [degcelsius*100]
	    uint8_t quality;// averaged quality of accumulated flow values [0:bad quality;255: max quality]
	} __attribute__((packed)) i2c_integral_frame;

	"""
	def __init__(self, bus, address):
		self.name = "PX4Flow"
		self.bus = bus
		self.address = address

		"""Initialize with negative values"""
		#I2C frame values
		self.frame_count = -1 #counts created I2C frames [#frames]
		self.pixel_flow_x_sum = -1 #latest x flow measurement in pixels*10 [pixels]
		self.pixel_flow_y_sum = -1 #latest y flow measurement in pixels*10 [pixels]
		self.flow_comp_m_x = -1 #x velocity*1000 [meters/sec]
		self.flow_comp_m_y = -1 #y velocity*1000 [meters/sec]
		self.qual = -1 #Optical flow quality / confidence [0: bad, 255: maximum quality]
		self.gyro_x_rate = -1 #latest gyro x rate [rad/sec]
		self.gyro_y_rate = -1 #latest gyro y rate [rad/sec]
		self.gyro_z_rate = -1 #latest gyro z rate [rad/sec]
		self.gyro_range = -1 #gyro range [0 .. 7] equals [50 deg/sec .. 2000 deg/sec] 
		self.sonar_timestamp = -1 #time since last sonar update [milliseconds]
		self.ground_distance = -1 #Ground distance in meters*1000 [meters]. Positive value: distance known. Negative value: Unknown distance

	    #Integral I2C frame values
		self.frame_count_since_last_readout = -1 #number of flow measurements since last I2C readout [#frames]
		self.pixel_flow_x_integral = -1 #accumulated flow in radians*10000 around x axis since last I2C readout [rad*10000]
		self.pixel_flow_y_integral = -1 #accumulated flow in radians*10000 around y axis since last I2C readout [rad*10000]
		self.gyro_x_rate_integral = -1 #accumulated gyro x rates in radians*10000 since last I2C readout [rad*10000] 
		self.gyro_y_rate_integral = -1 #accumulated gyro y rates in radians*10000 since last I2C readout [rad*10000] 
		self.gyro_z_rate_integral = -1 #accumulated gyro z rates in radians*10000 since last I2C readout [rad*10000] 
		self.integration_timespan = -1 #accumulation timespan in microseconds since last I2C readout [microseconds]
		self.sonar_timestamp = -1 # time since last sonar update [microseconds]
		self.ground_distance = -1 # Ground distance in meters*1000 [meters*1000]
		self.gyro_temperature = -1 # Temperature * 100 in centi-degrees Celsius [degcelsius*100]
		self.quality = -1 # averaged quality of accumulated flow values [0:bad quality;255: max quality]

	def update(self):
		"""Send 0x0 to PX4FLOW module and receive back 22 bytes of data in registers 0x00-0x15"""

		self.bus.write_byte(self.address, 0x0)
		i2c_frame = self.bus.read_i2c_block_data(self.address, 0x00, 22)

		self.frame_count = i2c_frame[0] | (i2c_frame[1] << 8)
		self.pixel_flow_x_sum = self.twos_comp(i2c_frame[2] | (i2c_frame[3] << 8), 16)
		self.pixel_flow_y_sum = self.twos_comp(i2c_frame[4] | (i2c_frame[5] << 8), 16)
		self.flow_comp_m_x = self.twos_comp(i2c_frame[6] | (i2c_frame[7] << 8), 16)
		self.flow_comp_m_y = self.twos_comp(i2c_frame[8] | (i2c_frame[9] << 8), 16)
		self.qual = self.twos_comp(i2c_frame[10] | (i2c_frame[11] << 8), 16)
		self.gyro_x_rate = self.twos_comp(i2c_frame[12] | (i2c_frame[13] << 8), 16)
		self.gyro_y_rate = self.twos_comp(i2c_frame[14] | (i2c_frame[15] << 8), 16)
		self.gyro_z_rate = self.twos_comp(i2c_frame[16] | (i2c_frame[17] << 8), 16)
		self.gyro_range = i2c_frame[18]
		self.sonar_timestamp = i2c_frame[19]
		self.ground_distance = self.twos_comp(i2c_frame[20] | (i2c_frame[21] << 8), 16)

	def integral_update(self):
		"""Send 0x16 to PX4FLOW module and receive back 25 bytes of data in registers 0x16-0x2E"""

		self.bus.write_byte(self.address, 0x16)
		i2c_integral_frame = self.bus.read_i2c_block_data(self.address, 0x16, 25)

		self.frame_count_since_last_readout = i2c_integral_frame[0] | (i2c_integral_frame[1] << 8)
		self.pixel_flow_x_integral = self.twos_comp(i2c_integral_frame[2] | (i2c_integral_frame[3] << 8), 16)
		self.pixel_flow_y_integral = self.twos_comp(i2c_integral_frame[4] | (i2c_integral_frame[5] << 8), 16)
		self.gyro_x_rate_integral = self.twos_comp(i2c_integral_frame[6] | (i2c_integral_frame[7] << 8), 16)
		self.gyro_y_rate_integral = self.twos_comp(i2c_integral_frame[8] | (i2c_integral_frame[9] << 8), 16)
		self.gyro_z_rate_integral = self.twos_comp(i2c_integral_frame[10] | (i2c_integral_frame[11] << 8), 16)
		self.integration_timespan = i2c_integral_frame[12] | (i2c_integral_frame[13] << 8) | (i2c_integral_frame[14] << 16) | (i2c_integral_frame[15] << 24)
		self.sonar_timestamp = i2c_integral_frame[16] | (i2c_integral_frame[17] << 8) | (i2c_integral_frame[18] << 16) | (i2c_integral_frame[19] << 24)
		self.ground_distance = self.twos_comp(i2c_integral_frame[20] | (i2c_integral_frame[21] << 8), 16)
		self.gyro_temperature = self.twos_comp(i2c_integral_frame[22] | (i2c_integral_frame[23] << 8), 16)
		self.quality = i2c_integral_frame[24]

	def twos_comp(self, val, bits):
	    """compute the 2's complement of int value val"""
	    
	    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
	        val = val - (1 << bits)        # compute negative value
	    return val                         # return positive value as is
