from lidar_control import read_tfluna_data, run_lidar, lidar_sweep, checkFwdOpen, change_direction
from servo_motor_control import MyServo
from drive_motor_control import MyMotor
import serial, time
import numpy as np


def main():
	servo_steering = MyServo(0, 0, "d", "a", 30, -30)
	servo_lidar = MyServo(1, 90, "h", "f", 90, -90)
	lidar = serial.Serial("/dev/serial0", 115200, timeout=0)
	backLeft_motor = MyMotor('M2', 0, 1) #initialize with motor port M2
	backRight_motor = MyMotor('M1', 0, 0.62)


	elements = 36
	distanceArr = np.empty(elements)
	angleArr = np.empty(elements)
	full_scan = [90, -90]
	small_scan = [45, -45]
	angles = [30, -30]



#	run_lidar(lidar)

#if __name__ == "__main__":
#	main()



#	lidar_sweep(lidar, servo_lidar, distanceArr, angleArr, elements, full_scan)

	while True:
			backLeft_motor.set_power(25)
			backRight_motor.set_power(25)


			distance, strength = read_tfluna_data(lidar)
			print(f"distance: {distance} cm")

			if distance < 30:
#				print("distance: ", distance, " cm")
				backLeft_motor.set_power(0)
				backRight_motor.set_power(0)

#				lidar_sweep(lidar, servo_lidar, distanceArr, angleArr, elements, full_scan)
				#Sweep function
				angle = 5
				i = 0

#    while i < elements:
#        distance, strength = read_tfluna_data(lidar)
 #       angleArr[i] = servo_lidar.get_angle()
  #      distanceArr[i] = distance

   #     if servo_lidar.get_angle() == scan_angle[0]:
    #        angle = -5
     #   if servo_lidar.get_angle() == scan_angle[1]:
      #      angle = 5
       # time.sleep(0.05)

        #servo_lidar.increment_angle(angle)
       # i += 1

				#end of sweep


#				time.sleep(0.25)

				backLeft_motor.set_power(-25)
				backRight_motor.set_power(-25)

#				time.sleep(1.5)

				backLeft_motor.set_power(0)
				backRight_motor.set_power(0)

#				time.sleep(1)

#	print(angleArr)
#	print(distanceArr)

#		if checkFwdOpen(distanceArr, angleArr, angles):
#			print("Front is open")
#			backLeft_motor.set_power(25)
#			backRight_motor.set_power(25)


#
#			lidar_sweep(lidar, servo_lidar, distanceArr, angleArr, elements, full_scan)
#			angle = change_direction(distanceArr, angleArr, backLeft_motor, backRight_motor)

#		else:
#			print("Front is not open")

#			backLeft_motor.set_power(0)
#			backRight_motor.set_power(0)

#			lidar_sweep(lidar, servo_lidar, distanceArr, angleArr, elements, full_scan)

#			angle = change_direction(distanceArr, angleArr, backLeft_motor, backRight_motor)
#			servo_steering.set_angle(angle)


#			time.sleep(0.05)

#	print(f"your angle is {an}")

#	print("Program ended.")

if __name__ == "__main__":
	main()

#print("Program ended.")
