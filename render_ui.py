import curses

def render_screen(stdscr):

	#get terminal screen size
	height, width = stdscr.getmaxyx()

	#clear the screen
	stdscr.clear()

	#Defines string that fits within terminal width
	motorControls = "Motor Controls: W Forward, S - Backwards, E - breaks"[:width-1]
	servoControls = "Servo Controls: <- A | D ->"[:width-1]
	quit = "Enter q to quit program"[:width-1]

	center =  round(width / 2)

	center_MC = max(round(center - (len(motorControls) / 2)), 0)
	center_SC = max(round(center - (len(servoControls) / 2)), 0)
	center_Q  = max(round(center - (len(quit) / 2)), 0)



	stdscr.addstr(3, center_MC, motorControls)
	stdscr.addstr(4, center_SC, servoControls)
	stdscr.addstr(5, center_Q, quit)

	#update the screen
	stdscr.refresh()
