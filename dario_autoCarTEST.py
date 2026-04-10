import time, serial
from fusion_hat.motor import Motor
from fusion_hat.servo import Servo
from lidar_control import read_tfluna_data

def lidar_sweep():
	pass

ser = serial.Serial("/dev/serial0", 115200, timeout=0)

m1 = Motor("M1")
m2 = Motor("M2")

s = 20
m1.power(s)
m2.power(s)



try:
	while True:
		
except KeyboardInterrupt:
	m1.power(0)
	m2.power(0)
	print("program end")
	time.sleep(.5)

