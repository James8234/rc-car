from fusion_hat.servo import Servo
from handle_input import  clamp_servo_angle

class MyServo:
	def __init__(self, pin, angle):
		self.pin = pin
		self.angle = angle
		self.servo = Servo(pin)

	def drive_servo(self, key):
		servo_offset = 0 #servo needs to be centered
		servo_angle_change = 5
		if key == 'A' or key == 'a':
			self.angle += servo_angle_change
		if key == 'D' or key == 'd':
			self.angle -= servo_angle_change

		#Clamp input
		self.angle = clamp_servo_angle(self.angle)

		#update poition of servo
		self.servo.angle(self.angle + servo_offset)

	def output_angle(self):
		return self.angle

#h	def pan_lidar_servo(self):

# The idea is that you want the lidar to pan -90 and 90. This means you need to keep addding untill you reach 90 
# or subtract untill you reach -90.

#		self.angle += 10

#		self.angle -= 10

#		self.angle = clamp_servo_angle(self.angle)
#		self.servo.angle(self.angle)
#		self.servo.angle(self.angle)
