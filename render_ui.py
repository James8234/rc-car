import curses

def render_screen(stdscr):

	#get terminal screen size
	height, width = stdscr.getmaxyx()

	#clear the screen
	stdscr.clear()

	#Defines string that fits within terminal width
	help = "<- A | D ->"[:width-1]
	quit = "Enter q to quit program"[:width-1]

	center =  round(width / 2)

	stdscr.addstr(0, center, help)
	stdscr.addstr(1, center, quit)

	#update the screen
	stdscr.refresh()
