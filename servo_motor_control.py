import time
import serial
from fusion_hat import Motor, Servo

class Navigation:
    def __init__(self, t_seconds=1.0, serial_port="/dev/serial0"):
        # --- Hardware Setup ---
        # Assuming: M1 = Drive Motor, S1 = Steering, S2 = LiDAR Pan
        try:
            self.motor = Motor("M1")
            self.steer_servo = Servo("S1")
            self.lidar_servo = Servo("S2")
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
        self.SERVO_CENTER = 90      # Adjust based on your build
        self.MAX_STEER_ANGLE = 40   # 40 degrees as requested
        self.MOTOR_POWER = 30       # 30% power as requested
        self.T_TIME = t_seconds     # Variable 't' from flowchart
        
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
        """Moves lidar servo and returns results for logic analysis."""
        scan_results = []
        for ang in range(start_angle, end_angle + 1, steps):
            self.lidar_servo.angle(ang)
            time.sleep(0.05) 
            dist = self.read_tfluna()
            scan_results.append((ang, dist))
        
        self.lidar_servo.angle(self.SERVO_CENTER) # Return to center
        return scan_results

    # --- Hardware Controls ---
    def set_steering(self, angle_offset):
        """Relative steering (-40 to 40)."""
        clamped = max(min(angle_offset, self.MAX_STEER_ANGLE), -self.MAX_STEER_ANGLE)
        self.steer_servo.angle(self.SERVO_CENTER + clamped)

    def drive(self, direction="fwd", duration=None):
        speed = self.MOTOR_POWER if direction == "fwd" else -self.MOTOR_POWER
        self.motor.speed(speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self):
        self.motor.speed(0)

    # --- Navigation Logic ---
    def find_turn_direction(self, scan_data):
        """Decides direction based on average distance in 180 sweep."""
        left_side = [d for a, d in scan_data if a < 90]
        right_side = [d for a, d in scan_data if a >= 90]
        
        left_avg = sum(left_side) / len(left_side) if left_side else 0
        right_avg = sum(right_side) / len(right_side) if right_side else 0
        
        return "left" if left_avg > right_avg else "right"

    def handle_obstacle_avoidance(self):
        """Flowchart: Stop -> 180 Sweep -> Turn -> Drive t -> Assessment."""
        self.stop()
        
        # 1. Lidar 180 sweep
        scan = self.perform_sweep(0, 180)
        turn_dir = self.find_turn_direction(scan)
        
        # 2. Turn wheels to Max angle towards direction
        steer_val = self.MAX_STEER_ANGLE if turn_dir == "right" else -self.MAX_STEER_ANGLE
        self.set_steering(steer_val)
        
        # 3. Drive for t sec
        self.drive("fwd", duration=self.T_TIME)
        
        # 4. Straighten wheels and Stop
        self.set_steering(0)
        self.stop()
        
        # 5. Assessment
        self.post_turn_assessment(turn_dir)

    def post_turn_assessment(self, prev_turn):
        """Biased assessment after the initial turn."""
        # Biased sweep (looking opposite to the turn)
        bias_range = (90, 180) if prev_turn == "right" else (0, 90)
        scan = self.perform_sweep(bias_range[0], bias_range[1])
        
        # Recalculate forward and lateral (using sweep ends as lateral proxy)
        self.lidar_servo.angle(self.SERVO_CENTER)
        fwd = self.read_tfluna()
        lat = scan[0][1] if prev_turn == "right" else scan[-1][1]

        # Scenario A: Path Clear
        if fwd >= self.DIST_THRESHOLD and lat >= self.LATERAL_THRESHOLD:
            opp_steer = -self.MAX_STEER_ANGLE if prev_turn == "right" else self.MAX_STEER_ANGLE
            self.set_steering(opp_steer)
            self.drive("fwd", duration=self.T_TIME)
            self.set_steering(0)

        # Scenario B: Tight Clearance (Drive until Spike)
        elif fwd >= self.DIST_THRESHOLD and lat < self.LATERAL_THRESHOLD:
            look_angle = 180 if prev_turn == "right" else 0
            self.lidar_servo.angle(look_angle)
            
            last_dist = self.read_tfluna()
            while True:
                self.drive("fwd")
                current_dist = self.read_tfluna()
                # Spike detection (clearing the corner)
                if current_dist > last_dist + 20: 
                    break
                last_dist = current_dist
            self.stop()

        # Scenario C: Blocked
        elif fwd < self.DIST_THRESHOLD:
            self.drive("reverse", duration=1.0)
            self.stop()

    def start(self):
        """Main Flowchart Loop."""
        print("System Startup... performing 180 sweep.")
        self.perform_sweep(0, 180)
        
        try:
            while True:
                # Check forward distance
                self.lidar_servo.angle(self.SERVO_CENTER)
                fwd_dist = self.read_tfluna()
                
                if fwd_dist >= self.DIST_THRESHOLD:
                    # Drive Fwd + Narrow 40 sweep
                    self.drive("fwd")
                    self.perform_sweep(70, 110, steps=10)
                else:
                    self.handle_obstacle_avoidance()
                    
        except KeyboardInterrupt:
            print("\n[!] Keyboard Interrupt. Stopping robot...")
        finally:
            self.stop()
            self.set_steering(0)
            self.ser.close()
            print("Shutdown complete.")

if __name__ == "__main__":
    # Initialize with your preferred 't' time (e.g., 1.5 seconds)
    nav = Navigation(t_seconds=1.5)
    nav.start()
