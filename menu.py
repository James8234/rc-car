import curses
#from fusion_hat.servo import Servo
#from servo_motor_control import MyServo


from render_ui import render_screen

def draw_menu(stdscr, previous_screen_state, servo_angle):

	#get terminal screen size
	height, width = stdscr.getmaxyx()

	if (height + width) != previous_screen_state[0]:
		render_screen(stdscr, servo_angle)

	previous_screen_state[0] = height + width
	previous_screen_state[1] = servo_angle
