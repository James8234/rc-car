from lidar_control import read_tfluna_data, run_lidar, lidar_sweep, checkFwdOpen, change_direction
from servo_motor_control import MyServo
from drive_motor_control import MyMotor
import serial, time
import numpy as np


def main():
	servo_steering = MyServo(0, 0, "d", "a", 0, -60, 20)
	servo_lidar = MyServo(1, 90, "h", "f", 90, -90, 20)
	lidar = serial.Serial("/dev/serial0", 115200, timeout=0)
	backLeft_motor = MyMotor('M2', 0, 1) #initialize with motor port M2
	backRight_motor = MyMotor('M1', 0, 0.62)


	angleIncrements = servo_steering.get_incrementAngle()
	elements = int(180 / angleIncrements) + 1
#	elements =  63 # int(180 / 5) # = int(elements)
	distanceArr = np.empty(elements)
	angleArr = np.empty(elements)
	full_scan = [90, -90]
	small_scan = [30, -30]
	angles = [45, -25] #limit the steering servo turn degrees
	bools = [False, False, False]


	angle = 0
	servo_steering.set_angle(-30)
	servo_lidar.set_angle(angle)

	while True:
		servo_lidar.set_angle(50)
		distance, strength = read_tfluna_data(lidar)
		if distance is None: distance = 999
		backLeft_motor.set_power(25)
		backRight_motor.set_power(25)
		time.sleep(0.2)

		if distance < 30:
			backLeft_motor.set_power(0)
			backRight_motor.set_power(0)

			lidar_sweep(lidar, servo_lidar, distanceArr, angleArr, elements, full_scan)
			angle, bools = change_direction(distanceArr, angleArr, servo_steering)

			if not bools[1]:
				backLeft_motor.set_power(-25)
				backRight_motor.set_power(-25)
				time.sleep(1)
				backLeft_motor.set_power(0)
				backRight_motor.set_power(0)

				lidar_sweep(lidar, servo_lidar, distanceArr, angleArr, elements, full_scan)
				angle, bools = change_direction(distanceArr, angleArr, servo_steering)

			print(f"your servo wheel angle is {angle}")
			servo_steering.set_angle(angle)
			time.sleep(0.25)

			if servo_steering.get_angle() != -20:
				backLeft_motor.set_power(25)
				backRight_motor.set_power(25)
				time.sleep(1.50)
				servo_steering.set_angle(-20)
#				backLeft_motor.set_power(25)
#				backRight_motor.set_power(25)
#				time.sleep(3.50)


	print("Program ended.")

if __name__ == "__main__":
	main()

#print("Program ended.")
