from time import sleep
from fusion_hat.motor import Motor

class MyMotor:
	def __init__(self, motor_port):
		self.motor = Motor(motor_port, is_reversed=False)

	def motor_control(self, key):

		match key:
			case 'w':
				self.motor.power(75)
			case 's':
				self.motor.power(-50)
			case 'e':
				self.motor.stop()
			case 'q':
				self.motor.stop()
				sleep(0.1)

