from time import sleep
from fusion_hat.motor import Motor

class MyMotor:
	def __init__(self, motor_port, speed, speed_scale):
		self.motor = Motor(motor_port, is_reversed=False)
		self.speed = speed
		self.speed_scale = speed_scale

	def motor_control(self, key):
		last_speed = self.speed

		match key:
			case '1':
				self.speed = 25 * self.speed_scale
			case '2':
				self.speed = 40 * self.speed_scale
			case '3':
				self.speed = 75 * self.speed_scale
			case '4':
				self.speed = 90 * self.speed_scale

		if last_speed != self.speed:
			self.motor.power(self.speed)

		match key:
			case 'w':
				if self.speed == 0: #lets say your stopped at hit gas w, the car should move
					self.speed = 25 * self.speed_scale
				self.motor.power(self.speed)
			case 's':
				self.motor.power(-self.speed)
			case 'e':
				self.speed = 0
				self.motor.stop()
			case 'q':
				self.motor.stop()
				sleep(0.1)

	def stop_if_close(self, distance):
		if distance <= 30:
			self.speed = 0
			self.motor.stop()
			print(f"Wheel has stopped {distance}")
		else:
			self.speed = 25
			self.motor.power(self.speed)
	def quick_start(self):
		self.speed = 25 * self.speed_scale
		self.motor.power(self.speed)

	def get_speed(self):
		return self.speed

	def set_power(self, power):
		self.speed = 0
		self.motor.stop()
		sleep(0.1)
