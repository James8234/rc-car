import curses
#from fusion_hat.servo import Servo
#from servo_motor_control import MyServo


def render_screen(stdscr, servo_angle, motor_speed):

	#get terminal screen size
	height, width = stdscr.getmaxyx()

	#clear the screen
	stdscr.clear()

	#Defines string that fits within terminal width
	motorControls = "Motor Controls: W Forward, S - Backwards, E - breaks"[:width-1]
	servoControls = "Wheel Servo Controls: <- A | D ->"[:width-1]
	lidar_servo_controls = "Lidar Servo Control: <- F | H ->"[:width-1]
	speedControls = "1 - slow | 2 - regular | 3 - fast | 4 - crazy fast"[:width-1]
	steering_angle = f"Your steering angle is: {servo_angle}"[:width-1]
	wheel_speed = f"Your speed is: {motor_speed}"[:width-1]
	quit = "Enter q to quit program"[:width-1]
	Tangle = f"Your angle is {servo_angle}"

	center =  round(width / 2)

	center_MC = max(round(center - (len(motorControls) / 2)), 0)
	center_SC = max(round(center - (len(servoControls) / 2)), 0)
	center_PC = max(round(center - (len(speedControls) / 2)), 0)
	center_Q  = max(round(center - (len(quit) / 2)), 0)
	center_LC = max(round(center - (len(lidar_servo_controls) / 2)), 0)


	stdscr.addstr(3, center_MC, motorControls)
	stdscr.addstr(4, center_SC, servoControls)
	stdscr.addstr(5, center_LC, lidar_servo_controls)
	stdscr.addstr(7, center_PC, speedControls)
	stdscr.addstr(3, 0, steering_angle)
	stdscr.addstr(4, 0, wheel_speed)
	stdscr.addstr(8, center_Q, quit)
#	stdscr.addstr(7, center, Tangle)

	#update the screen
	stdscr.refresh()
