from fusion_hat.servo import Servo
from handle_input import  clamp_servo_angle

class MyServo:
	def __init__(self, pin:float, angle:float):
		self.pin = pin
		self.angle = angle
		self.servo = Servo(pin)
#		self.left_button = left_button.lower()
#		self.right_button = right_button.lower()

	def drive_servo(self, key):
		servo_offset = 0 #servo needs to be centered
		servo_angle_change = 5

		if key == 'a':
			self.angle += servo_angle_change
		if key == 'd':
			self.angle -= servo_angle_change

		#Clamp input
		self.angle = clamp_servo_angle(self.angle)

		#update poition of servo
		self.servo.angle(self.angle + servo_offset)

	def output_angle(self):
		return self.angle

class lidar_servo(MyServo):
	def __init__(self, pin: float, angle: float):
		super().__init__(pin, angle) #call parent constructon

	def drive_servo(self, key):
		servo_offset = 0 #servo needs to be centered
		servo_angle_change = 5

		if key == 'f':
			self.angle += servo_angle_change
		if key == 'h':
			self.angle -= servo_angle_change

		#Clamp input
		self.angle = clamp_servo_angle(self.angle)

		#update poition of servo
		self.servo.angle(self.angle + servo_offset)


#h	def pan_lidar_servo(self):

# The idea is that you want the lidar to pan -90 and 90. This means you need to keep addding untill you reach 90 
# or subtract untill you reach -90.

#		self.angle += 10

#		self.angle -= 10

#		self.angle = clamp_servo_angle(self.angle)
#		self.servo.angle(self.angle)
#		self.servo.angle(self.angle)
