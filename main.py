from fusion_hat.servo import Servo
from time import sleep
from menu import draw_menu
from handle_input import get_user_input
from drive_motor_control import MyMotor
from render_ui import render_screen
import curses
from servo_motor_control import MyServo
#import asyncio

#Sweep from -90 to +90 degreess in steps of 10 degrees

def main(stdscr):
	#Clear Screen
	stdscr.clear()
	stdscr = curses.initscr() # Initialize curses - detecting terminal type
	curses.noecho() # turn off echoing keys to screen
	curses.cbreak() # Makes it so inputs don't require enter key to be pressed
	stdscr.keypad(True) #Provides curses to process special characters
	stdscr.nodelay(True) # getch and getkey become non-blocking

	servo_steering = MyServo(0, 0) #initialized steering servo with PWM 0 and angle 0
	servo_lidat = MyServo(0,0) # initialized lidat servo with PWM 0 and angle 0
#	servo1 = MyServo(1, 0)
	backLeft_motor = MyMotor('M1', 25) #initialize with motor port M2
	backRight_motor = MyMotor('M2', 25)
	key = 'w' #sets a variable so key is defined outside of the function

	#get initial_screen_size
	height, width = stdscr.getmaxyx()
	initial_screen_state = [height + width, 0]

	render_screen(stdscr, 10) #creates the menu to provide info on how to use the program

#	motor_control(key)

	while key != 'q':
		draw_menu(stdscr, initial_screen_state, servo_steering.output_angle()) #updates the screen if changes are made
		key = '' #assign a variable so key dose not stay on a or d

		key = get_user_input(stdscr) #the function gets an integer ACII and converts it into char

		backLeft_motor.motor_control(key) #Update motor PWM power
		backRight_motor.motor_control(key)

		servo.drive_servo(key) #updates servo angle
#		servo1.drive_servo(key)

curses.wrapper(main)
