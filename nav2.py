import time
import serial
from fusion_hat import Motor, Servo

class Navigation:
    def __init__(self, t_seconds=1.0, serial_port="/dev/serial0"):
        # --- Hardware Setup ---
        try:
            # Assuming: M1 & M2 = Drive Motors, S1 = Steering, S2 = LiDAR Pan
            self.motor_left = Motor("M1")
            self.motor_right = Motor("M2")
            self.steer_servo = Servo(0)
            self.lidar_servo = Servo(1)
        except Exception as e:
            print(f"Hardware Init Error: {e}")
            raise

        # --- TF-Luna Serial Setup ---
        try:
            self.ser = serial.Serial(serial_port, 115200, timeout=0.1)
        except Exception as e:
            print(f"Serial Init Error: {e}")
            raise
        
        # --- Constants & Calibration ---
        self.SERVO_CENTER = 90      
        self.MAX_STEER_ANGLE = 40   
        self.MOTOR_POWER = 30       
        self.T_TIME = t_seconds     
        
        self.DIST_THRESHOLD = 30    # cm
        self.LATERAL_THRESHOLD = 6  # cm
        
        # Initial State
        self.stop()
        self.set_steering(0)
        self.lidar_servo.angle(self.SERVO_CENTER)

    # --- TF-Luna Sensing ---
    def read_tfluna(self):
        """Reads distance in cm from the TF-Luna."""
        while self.ser.in_waiting >= 9:
            if self.ser.read(1) == b'\x59':
                if self.ser.read(1) == b'\x59':
                    data = self.ser.read(7)
                    distance = data[0] + data[1] * 256
                    return distance
        return 999 

    def perform_sweep(self, start_angle, end_angle, steps=5):
        """Moves lidar servo and returns results."""
        scan_results = []
        for ang in range(start_angle, end_angle + 1, steps):
            self.lidar_servo.angle(ang)
            time.sleep(0.05) 
            dist = self.read_tfluna()
            scan_results.append((ang, dist))
        
        self.lidar_servo.angle(self.SERVO_CENTER)
        return scan_results

    # --- Hardware Controls ---
    def set_steering(self, angle_offset):
        """Relative steering (-40 to 40)."""
        clamped = max(min(angle_offset, self.MAX_STEER_ANGLE), -self.MAX_STEER_ANGLE)
        self.steer_servo.angle(self.SERVO_CENTER + clamped)

    def drive(self, direction="fwd", duration=None):
        """Controls both M1 and M2 motors."""
        speed = self.MOTOR_POWER if direction == "fwd" else -self.MOTOR_POWER
        self.motor_left.speed(speed)
        self.motor_right.speed(speed)
        
        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self):
        """Stops both M1 and M2 motors."""
        self.motor_left.speed(0)
        self.motor_right.speed(0)

    # --- Navigation Logic ---
    def find_turn_direction(self, scan_data):
        """Decides direction based on average distance in 180 sweep."""
        left_side = [d for a, d in scan_data if a < 90]
        right_side = [d for a, d in scan_data if a >= 90]
        
        left_avg = sum(left_side) / len(left_side) if left_side else 0
        right_avg = sum(right_side) / len(right_side) if right_side else 0
        
        return "left" if left_avg > right_avg else "right"

    def handle_obstacle_avoidance(self):
        """Flowchart logic: Stop -> Turn -> Drive -> Assess."""
        self.stop()
        
        scan = self.perform_sweep(0, 180)
        turn_dir = self.find_turn_direction(scan)
        
        steer_val = self.MAX_STEER_ANGLE if turn_dir == "right" else -self.MAX_STEER_ANGLE
        self.set_steering(steer_val)
        
        self.drive("fwd", duration=self.T_TIME)
        
        self.set_steering(0)
        self.stop()
        
        self.post_turn_assessment(turn_dir)

    def post_turn_assessment(self, prev_turn):
        """Biased assessment after turn."""
        bias_range = (90, 180) if prev_turn == "right" else (0, 90)
        scan = self.perform_sweep(bias_range[0], bias_range[1])
        
        self.lidar_servo.angle(self.SERVO_CENTER)
        fwd = self.read_tfluna()
        lat = scan[0][1] if prev_turn == "right" else scan[-1][1]

        # Scenario A: Path Clear
        if fwd >= self.DIST_THRESHOLD and lat >= self.LATERAL_THRESHOLD:
            opp_steer = -self.MAX_STEER_ANGLE if prev_turn == "right" else self.MAX_STEER_ANGLE
            self.set_steering(opp_steer)
            self.drive("fwd", duration=self.T_TIME)
            self.set_steering(0)

        # Scenario B: Tight Clearance
        elif fwd >= self.DIST_THRESHOLD and lat < self.LATERAL_THRESHOLD:
            look_angle = 180 if prev_turn == "right" else 0
            self.lidar_servo.angle(look_angle)
            
            last_dist = self.read_tfluna()
            while True:
                self.drive("fwd")
                current_dist = self.read_tfluna()
                if current_dist > last_dist + 20: 
                    break
                last_dist = current_dist
            self.stop()

        # Scenario C: Blocked
        elif fwd < self.DIST_THRESHOLD:
            self.drive("reverse", duration=1.0)
            self.stop()

    def start(self):
        """Main Loop with KeyboardInterrupt handling."""
        print("System Startup... performing 180 sweep.")
        self.perform_sweep(0, 180)
        
        try:
            while True:
                self.lidar_servo.angle(self.SERVO_CENTER)
                fwd_dist = self.read_tfluna()
                
                if fwd_dist >= self.DIST_THRESHOLD:
                    self.drive("fwd")
                    self.perform_sweep(70, 110, steps=10)
                else:
                    print(f"Obstacle at {fwd_dist}cm. Avoiding...")
                    self.handle_obstacle_avoidance()
                    
        except KeyboardInterrupt:
            print("\n[!] Keyboard Interrupt. Stopping robot...")
        finally:
            self.stop()
            self.set_steering(0)
            self.ser.close()
            print("Shutdown complete.")

if __name__ == "__main__":
    nav = Navigation(t_seconds=1.5)
    nav.start()
