from fusion_hat.servo import Servo
from handle_input import  clamp_servo_angle

class MyServo:
	def __init__(self, pin, angle):
		self.pin = pin
		self.angle = angle
		self.servo = Servo(pin)

	def drive_servo(self, key):
		servo_offset = 10 #servo needs to be centered

		if key == 'A' or key == 'a':
			self.angle += 10
		if key == 'D' or key == 'd':
			self.angle -= 10

		#Clamp input
		self.angle = clamp_servo_angle(self.angle)

		#update poition of servo
		self.servo.angle(self.angle + servo_offset)
