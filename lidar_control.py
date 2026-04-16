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


def lidar_sweep(lidar, servo_lidar, distanceArr, angleArr, elements, scan_angle):
	angle = servo_lidar.get_incrementAngle()
	i = 0

	servo_lidar.set_angle(90)
	time.sleep(0.25)

	while i < elements:
		distance, strength = read_tfluna_data(lidar)
		angleArr[i] = servo_lidar.get_angle()
		distanceArr[i] = distance

		if servo_lidar.get_angle() == scan_angle[0]:
			angle = -angle
		if servo_lidar.get_angle() == scan_angle[1]:
			angle = angle
		time.sleep(0.05)

		servo_lidar.increment_angle(angle)
		i += 1

	print(f"Your dis arr is {distanceArr}")
	print(f"your angle arr is {angleArr}")
#	servo_lidar.set_angle(90)
	time.sleep(0.25)

def checkFwdOpen(disArr, angleArr, angles):
	print("Check has started -------------------")
	print(f"The original array distance is: {disArr}")
	print(f"the angleArr is: {angleArr}")
	print(f"the section we want to check is : {angles}")


	# np.nonzero returns the indice where the condition is True.
	# Thee condition True is when the provided angles[0] is equal to an element in angleArr
	start_index = np.nonzero(angleArr == angles[0])
	end_index   = np.nonzero(angleArr == angles[1])


	if start_index[0].size == 0 or end_index[0].size == 0:
		return False

	start_index = start_index[0][0]
	end_index = end_index[0][0]

	if start_index > end_index:
		start_index, end_index = end_index, start_index

	a = disArr[start_index:end_index + 1] #store the range of values that belong to the angle

	print(f"The original array distance is: {disArr}")
	print(f"The cut out array dis is : {a}")
#	print(f"Your angles are: {angles[0]} and {angles[1]}, The section is: {a}")
#	print(f"Your checkFwnOpen array is {a}")

	if a.size == 0:
		return False

	for i in a:
		if (i < 30):
			return False
	return True

def change_direction(disArr, angArr,  backLeft_motor, backRight_motor):
	Q1 = [90, 50]
	Q2 = [30, -30]
	Q3 = [-50, -90]

	print(f"disArr")
	angle = 0
	bools = [True, True, True]
	print("Q1 check -----------")
	bools[0] = checkFwdOpen(disArr, angArr, Q1)
	print("Q2 check -----------")
	bools[1] = checkFwdOpen(disArr, angArr, Q2)
	print("Q3 check -----------")
	bools[2] = checkFwdOpen(disArr, angArr, Q3)

	if bools[1]:
		angle =  0
	elif bools[0]:
		angle = 45
	elif bools[2]:
		angle = -15


#	print(f"Q1 - {bools[0]}, Q2 - {bools[1]}, Q3 - {bools[2]}")
#	print(f"Your angle arr is: {angArr}")

	print([int(b) for b in bools])

	return angle, bools 

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


