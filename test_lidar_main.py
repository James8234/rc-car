from lidar_control import read_tfluna_data, run_lidar
import serial, time

#print("Program ended.")

#ser = serial.Serial("/dev/serial0", 115200, timeout=0)

#class lidar_module:
#	def __init__(self, ser):
#		self.ser = ser
#print("Program ended.")

#ser = serial.Serial("/dev/serial0", 115200, timeout=0)

def main():
	ser = serial.Serial("/dev/serial0", 115200, timeout=0)
	read_tfluna_data(ser)
#	lidar = lidar_module(ser)
	run_lidar(ser)
	print("Program ended.")
#	read_tfluna_data()

if __name__ == "__main__":
	main()
#print("Program ended.")
