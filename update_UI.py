import curses
#This function returns true or false if the screen should update

from render_ui import render_screen

def checkForChanges(stdscr, previous_screen_state, servo_angle, motor_speed):

	#Screen state
	state = False

	#get terminal screen size
	height, width = stdscr.getmaxyx()

	if (height + width) != previous_screen_state.get_screen_size():
		state = True
	elif servo_angle != previous_screen_state.get_screen_servo_angle():
		state = True
	elif motor_speed != previous_screen_state.get_screen_motor_power():
		state = True

	previous_screen_state.screen_size = height + width
	previous_screen_state.servo_angle = servo_angle
	previous_screen_state.motor_power = motor_speed

	return state

class screen_state:
	def __init__(self, screen_size, servo_angle, motor_power):
		self.set_screen_size(screen_size)
		self.set_screen_servo_angle(servo_angle)
		self.set_screen_motor_power(motor_power)

	def get_screen_size(self):
		return self.screen_size
	def get_screen_servo_angle(self):
		return self.servo_angle
	def get_screen_motor_power(self):
		return self.motor_power
	def set_screen_size(self, screen_size):
		self.screen_size = screen_size
	def set_screen_servo_angle(self, servo_angle):
		self.servo_angle = servo_angle
	def set_screen_motor_power(self, motor_power):
		self.motor_power = motor_power

