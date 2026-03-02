import curses
from render_ui import render_screen

def draw_menu(stdscr, previous_screen_size):

	#get terminal screen size
	height, width = stdscr.getmaxyx()

	if (height + width) != previous_screen_size[0]:
		render_screen(stdscr)

	previous_screen_size[0] = height + width
