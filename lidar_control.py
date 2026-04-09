import serial, time
from drive_motor_control import MyMotor
#from servo_motor_control import MyServo
from time import sleep
#from servo_motor_control import MyServo

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


#import numpy as np

def scan_lidar(ser, servo_lidar, distanceArr, angleArr, elements, scan_angle):
	angle = 5
	i = 0

	while i < elements:
		distance, strength = read_tfluna_data(ser)
		angleArr[i] = servo_lidar.get_angle()
		distanceArr[i] = distance

		if servo_lidar.get_angle() == scan_angle[0]:
			angle = -5
		if servo_lidar.get_angle() <= scan_angle[1]:
			angle = 5
		time.sleep(0.02)

		servo_lidar.increment_angle(angle)
#		print(f"Your angle is {servo_lidar.get_angle()}")
		i += 1

	#set back to starting angle.
	servo_lidar.set_angle(90)
	time.sleep(0.25)

def run_lidar(ser):
	backLeft_motor = MyMotor('M2', 25, 1) #initialize with motor port M2
	backRight_motor = MyMotor('M1', 25, 0.62)

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

