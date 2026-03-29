from fusion_hat.servo import Servo
from handle_input import  clamp_servo_angle

class MyServo:
	def __init__(self, pin:float, angle:float):
		self.pin = pin
		self.angle = angle
		self.servo = Servo(pin)

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

	def get_angle(self):
		return self.angle

	def set_angle(self, angle):
		self.angle = self.clamp_servo_angle(angle)

	def increment_angle(self, angle):
		self.angle = self.clamp_servo_angle(self.get_angle() + angle)

	def clamp_servo_angle(self, angle):
		if(angle > 90):
			return 90
		elif(angle < -90):
			return -90
		else:
			return angle

class lidar_servo(MyServo):
	def __init__(self, pin: float, angle: float):
		super().__init__(pin, angle) #call parent constructon

	def drive_servo(self, key):
		servo_offset = 0 #servo needs to be centered
		servo_angle_change = 5

		if key == 'f':
			self.increment_angle(servo_angle_change)
		if key == 'h':
			self.increment_angle(-servo_angle_change)
