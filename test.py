from time import sleep
import serial
from fusion_hat.servo import Servo
from fusion_hat.motor import Motor
import numpy as np

ser = serial.Serial("/dev/serial0", 115200,timeout=0) # mini UART serial device

#Global Variables
steering_offset = 15
lidar_offset = 0
Motor_Power = 30


def read_tfluna_data():
    ''' reads data from the lidar and returns the distance in cm'''
    while True:
        counter = ser.in_waiting # count the number of bytes of the serial port
        if counter > 8:
            bytes_serial = ser.read(9) # read 9 bytes
            ser.reset_input_buffer() # reset buffer

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
                distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
                strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
                temperature = bytes_serial[6] + bytes_serial[7]*256 # temp in next two bytes
                temperature = (temperature/8.0) - 256.0 # temp scaling and offset
                return distance/100.0,strength,temperature

steering_servo = Servo(0,offset=steering_offset)

lidar_servo = Servo(1,offset = lidar_offset)

left_motor = Motor('M0',is_reversed=False)
right_motor = Motor('M1',is_reversed=True)



if ser.isOpen() == False:
    ser.open() # open serial port if not open

try:
    while True:
        distance = read_tfluna_data()
        print(f"Distance: {distance} cm")
        sleep(1)

        steering_servo.angle = 40
        sleep(1)
        steering_servo.angle = 0
        sleep(1)
        steering_servo.angle = -40
        sleep(1)
        steering_servo.angle = 0
        left_motor.power = Motor_Power
        right_motor.power = Motor_Power
        sleep(1)
        left_motor.power = 0
        right_motor.power = 0
        print('Repeat Loop')
        sleep(4)

except KeyboardInterrupt:
    print("Program terminated by user")
    lidar_servo.stop()
    steering_servo.stop()
    left_motor.stop()
    right_motor.stop()
