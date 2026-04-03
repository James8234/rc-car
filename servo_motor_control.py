from fusion_hat.servo import Servo
#from handle_input import  clamp_servo_angle

class MyServo:
	def __init__(self, pin:float, angle:float, rightkey, leftkey, rightAngleLimit, leftAngleLimit):
		self.pin = pin
		self.angle = angle
		self.servo = Servo(pin)
		self.controls  = {
			"Right": rightkey,
			"Left": leftkey
		}
		self.range = [rightAngleLimit, leftAngleLimit]


	def drive_servo(self, key):
		servo_offset = 0 #servo needs to be centered
		servo_angle_change = 5

		if key == self.controls["Left"]:
			self.increment_angle(servo_angle_change)
		if key == self.controls["Right"]:
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
		if(angle > self.range[0]):
			return self.range[0]
		elif(angle < self.range[1]):
			return self.range[1]
		else:
			return angle
