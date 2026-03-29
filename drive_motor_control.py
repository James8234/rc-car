from time import sleep
from fusion_hat.motor import Motor

class MyMotor:
	def __init__(self, motor_port, speed):
		self.motor = Motor(motor_port, is_reversed=False)
		self.speed = speed

	def motor_control(self, key):
		last_speed = self.speed

		match key:
			case '1':
				self.speed = 25
			case '2':
				self.speed = 40
			case '3':
				self.speed = 75
			case '4':
				self.speed = 100

		if last_speed != self.speed:
			self.motor.power(self.speed)

		match key:
			case 'w':
				self.motor.power(self.speed)
			case 's':
				self.motor.power(-self.speed)
			case 'e':
				self.speed = 0
				self.motor.stop()
			case 'q':
				self.motor.stop()
				sleep(0.1)

	def get_speed(self):
		return self.speed
