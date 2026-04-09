from lidar_control import read_tfluna_data, run_lidar, lidar_sweep, checkFwdOpen
from servo_motor_control import MyServo
import serial, time
import numpy as np


def main():
	servo_lidar = MyServo(1, 90, "h", "f", 90, -90)
	lidar = serial.Serial("/dev/serial0", 115200, timeout=0)

	elements = 37
	distanceArr = np.empty(elements)
	angleArr = np.empty(elements)
	full_scan = [90, -90]
	small_scan = [45, -45]


	lidar_sweep(lidar, servo_lidar, distanceArr, angleArr, elements, full_scan)

	print(angleArr)
	print(distanceArr)

	if checkFwdOpen(distanceArr, angleArr, 30):
		print("Front is open")
	else:
		print("Front is not open")

	print("Program ended.")

if __name__ == "__main__":
	main()
#print("Program ended.")
