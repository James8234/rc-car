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

		render_screen(stdscr, servo_angle, motor_speed)

	previous_screen_state[0] = height + width
	previous_screen_state[1] = servo_angle

	return state
