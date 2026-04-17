from fusion_hat.servo import Servo
from time import sleep
from update_UI import checkForChanges, screen_state
from handle_input import get_user_input
from drive_motor_control import MyMotor
from render_ui import render_screen
import curses
from servo_motor_control import MyServo
from auto_drive import auto_drive_mode


#Sweep from -90 to +90 degreess in steps of 10 degrees

def main(stdscr):
	#Clear Screen
	stdscr.clear()
	stdscr = curses.initscr() # Initialize curses - detecting terminal type
	curses.noecho() # turn off echoing keys to screen
	curses.cbreak() # Makes it so inputs don't require enter key to be pressed
	stdscr.keypad(True) #Provides curses to process special characters
	stdscr.nodelay(True) # getch and getkey become non-blocking

	servo_steering = MyServo(0, 0, "d", "a", 0, -60, 10) #initialized MyServo(PWMpin, angle, rightkey, leftkey, rightAngleLimit, leftAngleLimit)
	servo_lidar = MyServo(1, 0, "h", "f", 90, -90, 10)
	backLeft_motor = MyMotor('M2', 0, 1) #initialize with motor port M2
	backRight_motor = MyMotor('M1', 0, 1)
	key = 'w' #sets a variable so key is defined outside of the function

	#get initial_screen_size
	height, width = stdscr.getmaxyx()
	initial_screen_state = screen_state(height + width, 0, 0)


	render_screen(stdscr, 0, 0) #creates the menu to provide info on how to use the program

	while key != 'q':
		if checkForChanges(stdscr, initial_screen_state, servo_steering.get_angle(), backLeft_motor.get_speed()): #updates the screen if changes are made
			render_screen(stdscr, servo_steering.get_angle(), backLeft_motor.get_speed())

		key = '' #assign a variable so key dose not stay on a or d

		key = get_user_input(stdscr) #the function gets an integer ACII and converts it into char

		if key == 'z':
			auto_drive_mode(backLeft_motor, backRight_motor, servo_steering, servo_lidar)

		backLeft_motor.motor_control(key) #Update motor PWM power
		backRight_motor.motor_control(key)

		servo_steering.drive_servo(key) #updates servo angle
		servo_lidar.drive_servo(key)

curses.wrapper(main)
