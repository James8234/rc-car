from lidar_control import read_tfluna_data, run_lidar, lidar_sweep, checkFwdOpen, change_direction
from servo_motor_control import MyServo
import serial, time
import numpy as np


def main():
	servo_steering = MyServo(0, 0, "d", "a", 30, -30)
	servo_lidar = MyServo(1, 90, "h", "f", 90, -90)
	lidar = serial.Serial("/dev/serial0", 115200, timeout=0)

	elements = 37
	distanceArr = np.empty(elements)
	angleArr = np.empty(elements)
	full_scan = [90, -90]
	small_scan = [45, -45]
	angles = [30, -30]


	lidar_sweep(lidar, servo_lidar, distanceArr, angleArr, elements, full_scan)

	while True:
#	print(angleArr)
#	print(distanceArr)

		if checkFwdOpen(distanceArr, angleArr, angles):
			print("Front is open")
			lidar_sweep(lidar, servo_lidar, distanceArr, angleArr, elements, full_scan)
		else:
			print("Front is not open")
			lidar_sweep(lidar, servo_lidar, distanceArr, angleArr, elements, full_scan)

			angle = change_direction(distanceArr, angleArr)
			servo_steering.set_angle(angle)


			time.sleep(0.05)

#	print(f"your angle is {an}")

	print("Program ended.")

if __name__ == "__main__":
	main()
#print("Program ended.")
