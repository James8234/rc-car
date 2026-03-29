import curses
#This function returns true or false if the screen should update

from render_ui import render_screen

def checkForChanges(stdscr, previous_screen_state, servo_angle, motor_speed):

	#Screen state
	state = False

	#get terminal screen size
	height, width = stdscr.getmaxyx()

	if (height + width) != previous_screen_state[0]:
		state = True
	elif servo_angle != previous_screen_state[1]:
		state = True
	elif motor_speed != previous_screen_state[2]:
		state = True

	previous_screen_state[0] = height + width
	previous_screen_state[1] = servo_angle
	previous_screen_state[2] = motor_speed

	return state
