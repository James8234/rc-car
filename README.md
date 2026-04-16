# RC Car Control System

A Python-based control system for a DIY RC car featuring manual and autonomous driving modes, motor control, LiDAR-based obstacle detection, and a real-time user interface.

Built as a modular robotics project, this codebase allows you to control drive motors and steering servos, integrate LiDAR 
sensor data for environmental awareness, and switch between manual input control and autonomous navigation.

## Features

- **Manual Control** — Drive and steer the RC car using keyboard, joystick, or custom input handling.
- **Autonomous Driving** — Basic obstacle avoidance and navigation logic using LiDAR scans.
- **Motor Control**
  - Drive motor control (forward, reverse, speed)
  - Servo motor control for precise steering
- **LiDAR Integration** — Real-time distance scanning and obstacle detection.
- **User Interface** — Dynamic on-screen rendering of telemetry, sensor data, and car status.
- **Modular Design** — Clean separation of concerns across motor control, sensor handling, input, autonomy, and UI modules.



## Getting Started## Requirements

- Python 3.x
- Hardware:
  - RC car chassis with DC drive motors and steering servo
  - LiDAR sensor (e.g. RPLIDAR or similar)
  - Raspberry Pi, Arduino, or compatible single-board computer for control
- Python libraries (depending on your hardware setup):
  - `pyserial`, `RPi.GPIO`, `adafruit-circuitpython-servokit`, or similar for motor/LiDAR control
  - `pygame`, `curses`, 

1. Clone the repository:
   git clone https://github.com/James8234/rc-car.git
   python main.rs
