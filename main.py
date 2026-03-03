from fusion_hat.servo import Servo
from time import sleep
from menu import draw_menu
from handle_input import get_user_input, clamp_servo_angle
from render_ui import render_screen
import curses

#Sweep from -90 to +90 degreess in steps of 10 degrees

def main(stdscr):
	#Clear Screen
	stdscr.clear()
	stdscr = curses.initscr() # Initialize curses - detecting terminal type
	curses.noecho() # turn off echoing keys to screen
	curses.cbreak() # Makes it so inputs don't require enter key to be pressed
	stdscr.keypad(True) #Provides curses to process special characters
	stdscr.nodelay(True) # getch and getkey become non-blocking

	servo = Servo(0) #initialized with PWM 0
	servo_offset = 10 #servo needs to be centered
	i = 0  #angle of servo
	key = 'a' #sets a variable so key is defined outside of the function

	#get initial_screen_size
	height, width = stdscr.getmaxyx()
	initial_screen_size = [height + width]

	render_screen(stdscr) #creates the menu to provide info on how to use the program

	while key != 'q':
		draw_menu(stdscr, initial_screen_size) #updates the screen if changes are made
		key = '' #assign a variable so key dose not stay on a or d

		key = get_user_input(stdscr) #the function gets an integer ACII and converts it into char

		if key == 'A' or key == 'a':
			i = i + 10
		if key == 'D' or key == 'd':
			i = i - 10

		#Clamp input
		i = clamp_servo_angle(i)

		servo.angle(i + servo_offset)

#	stdscr.refresh() # updates screen after chages where made
#	stdscr.getkey() 

curses.wrapper(main)
