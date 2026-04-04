import serial, time
from drive_motor_control import MyMotor

# Access the serial port for serial0 at a baud rate of 115200
#ser = serial.Serial("/dev/serial0", 115200, timeout=0) # mini UART serial device

def read_tfluna_data(ser):
	while True:
		counter = ser.in_waiting # count the number of bytes of the serial port
		if counter > 8:
			bytes_serial = ser.read(9) # read 9 bytes
			ser.reset_input_buffer() # reset buffer

			if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes for correct data format (refer to product manual)
				distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
				strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
				return distance, strength

#def run_lidar():
#try:
#	if ser.isOpen() == False:
#		ser.open() # open serial port if not open

#	while True:
#		distance, strength = read_tfluna_data()

#		print("Distance", format(distance), "cm")
#		time.sleep(.5)
#except KeyboardInterrupt:
#	print("Program ended.")
#	ser.close() # close serial port


def run_lidar(ser):
	backLeft_motor = MyMotor('M2', 0, 1) #initialize with motor port M2
	backRight_motor = MyMotor('M1', 0, 0.62)

	try:
		if ser.isOpen() == False:
			ser.open() # open serial port if not open

		backLeft_motor.quick_start()
		backRight_motor.quick_start()

		while True:

			distance, strength = read_tfluna_data(ser)

			print("Distance", format(distance), "cm")
#			time.sleep(.5)

			backLeft_motor.stop_if_close(distance)
			backRight_motor.stop_if_close(distance)

	except KeyboardInterrupt:
		print("Program ended.")
		ser.close() # close serial port

