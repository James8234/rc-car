import time, serial
from fusion_hat.motor import Motor
from lidar_control import read_tfluna_data

ser = serial.Serial("/dev/serial0", 115200, timeout=0)

m1 = Motor("M1")
m2 = Motor("M2")

s = 20
m1.power(s)
m2.power(s)

try:
	while True:
		d,s = read_tfluna_data(ser)
		print("distance: ", d, " cm")
		if d < 30:
			m1.power(0)
			m2.power(0)
			print("stopped!")
		else:
			m1.power(20)
			m2.power(20)
			print("going")

		time.sleep(0.1)
except KeyboardInterrupt:
	m1.power(0)
	m2.power(0)
	print("program end")
	time.sleep(.5)

