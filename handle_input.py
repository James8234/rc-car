import curses

def get_user_input(stdscr):
	acii_value = stdscr.getch() #Gets a ACII value and convert it to string char
	if acii_value >= 0 and acii_value <= 127: #checks for valid ASCII values
 		return chr(acii_value).lower()
	return None

def clamp_servo_angle(i):
	if(i >= 90):
		i = 90
	if(i <= -90):
		i = -90
	return i
