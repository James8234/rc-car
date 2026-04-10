import serial, time
from drive_motor_control import MyMotor
#from servo_motor_control import MyServo
from time import sleep
import numpy as np

#from servo_motor_control import MyServo

# Access the serial port for serial0 at a baud rate of 115200
#ser = serial.Serial("/dev/serial0", 115200, timeout=0) # mini UART serial device

def read_tfluna_data(lidar):
	while True:
		counter = lidar.in_waiting # count the number of bytes of the serial port
		if counter > 8:
			bytes_serial = lidar.read(9) # read 9 bytes
			lidar.reset_input_buffer() # reset buffer

			if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes for correct data format (refer to product manual)
				distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
				strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
				return distance, strength


def lidar_sweep(ser, servo_lidar, distanceArr, angleArr, elements, scan_angle):
	angle = 5
	i = 0

	servo_lidar.set_angle(90)
	time.sleep(0.25)

	while i < elements:
		distance, strength = read_tfluna_data(ser)
		angleArr[i] = servo_lidar.get_angle()
		distanceArr[i] = distance

		if servo_lidar.get_angle() == scan_angle[0]:
			angle = -5
		if servo_lidar.get_angle() == scan_angle[1]:
			angle = 5
		time.sleep(0.04)

		servo_lidar.increment_angle(angle)
		i += 1

	#set back to starting angle.

#	servo_lidar.set_angle(90)
#	time.sleep(0.5)

def checkFwdOpen(distanceArr, angleArr, angles):
#	print(f"Your angles thing contain -0 {angles[0]} -1 {angles[1]}")
#	print(f"Your angleArr contains: {angleArr}")
	start_index = np.nonzero(angleArr == angles[0])
	end_index   = np.nonzero(angleArr == angles[1])
	if start_index[0].size == 0 or end_index[0].size == 0:
		return False

	start_index = start_index[0][0]
	end_index = end_index[0][0]

	if start_index > end_index:
		start_index, end_index = end_index, start_index
	#Check if arrays are empty
#	if start[0].size == 0 or end[0].size == 0:
#		return False
#	print(f"Your start_index is {start_index}")
#	print(f"Your end_index is {end_index}")

#	print("E")
#	print(f"{start}")
#	start_index = start[0] #.item() #convert a single-element array into a scalar
#	end_index = end[0] + 1 #.item() + 1
#	print(f"The distance array contains {distanceArr}")
	a = distanceArr[start_index:end_index + 1] #store the range of values that belong to the angle
	print(f"The aray taken out is {a}")

	if a.size == 0:
		return False

	for i in a:
		if (i < 30):
			return False
	return True

def change_direction(disArr, angArr,  backLeft_motor, backRight_motor):
	Q1 = [90, 45]
	Q2 = [40, 0]
	Q3 = [-5, -45]
	Q4 = [-50, -90]
	angle = 0
	bools = [True, True, True, True]
	bools[0] = checkFwdOpen(disArr, angArr, Q1)
	bools[1] = checkFwdOpen(disArr, angArr, Q2)
	bools[2] = checkFwdOpen(disArr, angArr, Q3)
	bools[3] = checkFwdOpen(disArr, angArr, Q4)

	if bools[1] and bools[2]:
									#	if checkFwdOpen(disArr, angArr, Q2) and checkFwdOpen(disArr, angArr, Q3):
		backLeft_motor.set_power(25)
		backRight_motor.set_power(25)
		angle =  0
	elif  not bools[1] and not bools[2]:
		backLeft_motor.set_power(0)
		backRight_motor.set_power(0)
	elif bools[1]:
		angle = 90
	elif bools[2]:
		angle = -90
	elif bools[0]:
		angle = 90

	elif bools[3]:
		angle = -90

#	if checkFwdOpen(disArr, angArr, Q2):
#		angle = 90
#	else:
#		bools[1] = False
#	if checkFwdOpen(disArr, angArr, Q3):
#		angle = -90
#	else:
#		bools[2] = False
#	if checkFwdOpen(disArr, angArr, Q1):
#		angle = 90
#	else:
#		bools[0] = False
#	if checkFwdOpen(disArr, angArr, Q4):
#		angle = -90
#	else:
#		bools[3] = False

#	if
		         #backLeft_motor.set_power(25)
 				#backRight_motor.set_power(25)


#	else:
		#backup function
#		angle = 0
	print([int(b) for b in bools])

	return angle

def run_lidar(lidar):
	backLeft_motor = MyMotor('M2', 25, 1) #initialize with motor port M2
	backRight_motor = MyMotor('M1', 25, 0.62)

	try:
#		if servo.isOpen() == False:
#			servo.open() # open serial port if not open

		backLeft_motor.quick_start()
		backRight_motor.quick_start()

		while True:

			distance, strength = read_tfluna_data(lidar)

			print("Distance", format(distance), "cm")
#			time.sleep(.5)

			backLeft_motor.stop_if_close(distance)
			backRight_motor.stop_if_close(distance)

	except KeyboardInterrupt:
		print("Program ended.")
		ser.close() # close serial port


