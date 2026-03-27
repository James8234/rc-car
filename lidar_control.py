import serial, time

#Access the serial port for serial0 at a baud rate of 115200
lidar = serial.Serial("/dev/serial0", 115200, timeout=0) #mini UART serial device

def read_tfluna_data():
	while True:
		counter = lidar.in_waiting #count the number of bytes of the serial port
		if counter > 8:
			bytes_serial = lidar.read(9) #read 9 bytes
			lidar.reset_input_buffer()
