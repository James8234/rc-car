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

## Project Structure
rc-car/
├── main.py                  # Main entry point — starts the control loop
├── auto_drive.py            # Autonomous driving logic and decision making
├── drive_motor_control.py   # Controls the main drive motors (throttle)
├── servo_motor_control.py   # Controls the steering servo
├── lidar_control.py         # Interface and data processing for the LiDAR sensor
├── handle_input.py          # Keyboard / controller input handling
├── render_ui.py             # Renders the user interface / dashboard
├── update_UI.py             # Updates UI elements in real time
├── test_lidar_main.py       # Standalone test script for LiDAR
└── pycache/             # Python cache directory (ignored)
