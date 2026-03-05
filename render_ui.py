import curses

def render_screen(stdscr):

	#get terminal screen size
	height, width = stdscr.getmaxyx()

	#clear the screen
	stdscr.clear()

	#Defines string that fits within terminal width
	motorControls = "Motor Controls: W Forward, S - Backwards, E - breaks"
	help = "<- A | D ->"[:width-1]
	quit = "Enter q to quit program"[:width-1]

	center =  round(width / 2)
	stdscr.addstr(1, center, "^")
	stdscr.addstr(2, center, "|")
	stdscr.addstr(3, center, motorControls)
	stdscr.addstr(4, center, help)
	stdscr.addstr(5, center, quit)

	#update the screen
	stdscr.refresh()
