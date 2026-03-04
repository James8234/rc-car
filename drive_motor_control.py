from time import sleep
from fusion_hat.motor import Motor

def motor_control(key):
	#create object for motor port M2
	#is_reverse=True means the motor direction is inverted
	motor = Motor('M2', is_reversed=False)


#	if key == 'W' or key == 'w':
	motor.power(75)
#		sleep(1)

	if key == 'S' or key == 's':
		motor.power(-50)
#		sleep(1)

	motor.power(0)

	if key == 'D' or key == 'd':
		motor.stop() #Ensure motor stopped on exit
		sleep(.1) #short exit delay for safety
