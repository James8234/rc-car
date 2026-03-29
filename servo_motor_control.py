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
			self.increment_angle(servo_angle_change)
		if key == 'd':
			self.increment_angle(-servo_angle_change)

	def get_angle(self):
		return self.angle

	def set_angle(self, angle):
		clamped_angle = self.clamp_angle(angle)
		self.servo.angle(self.clamp_servo_angle(angle))

	def increment_angle(self, angle):
		clamped_angle = self.clamp_servo_angle(self.get_angle() + angle)
		self.angle = clamped_angle
		self.servo.angle(clamped_angle)

	def clamp_servo_angle(self, angle):
		if(angle > 30):
			return 30
		elif(angle < -40):
			return -40
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
