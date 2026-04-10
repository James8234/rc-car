from fusion_hat import Motor, Servo
import time

class Navigation:
    def __init__(self, t_seconds=1.0):
        # Hardware Setup
        # Assuming DC Motor on M1 and Steering Servo on S1
        self.motor = Motor("M1")
        self.servo = Servo("S1")
        
        # Calibration & Constants
        self.SERVO_CENTER = 90      # Adjust if your wheels aren't perfectly straight at 90
        self.MAX_STEER_ANGLE = 40   # As requested
        self.MOTOR_POWER = 30       # As requested
        self.T_TIME = t_seconds     # The 't' variable from your flowchart
        
        self.DIST_THRESHOLD = 30    # cm
        self.LATERAL_THRESHOLD = 6  # cm
        
        # Initialize state
        self.stop()
        self.set_steering(0)

    # --- Hardware Control Methods ---

    def set_steering(self, angle_offset):
        """
        Sets steering relative to center.
        angle_offset: -40 (left) to 40 (right)
        """
        # Clamp the input to the max allowed angle
        clamped = max(min(angle_offset, self.MAX_STEER_ANGLE), -self.MAX_STEER_ANGLE)
        target_angle = self.SERVO_CENTER + clamped
        self.servo.angle(target_angle)

    def drive(self, direction="fwd", duration=None):
        power = self.MOTOR_POWER if direction == "fwd" else -self.MOTOR_POWER
        self.motor.speed(power)
        
        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self):
        self.motor.speed(0)

    # --- Sensor Logic Placeholder ---

    def get_lidar_data(self, mode="sweep", bias=None):
        """
        Placeholder: Replace this with your actual LiDAR library calls.
        Returns a dict with forward distance, lateral distance, and spike detection.
        """
        # Example return structure based on your flowchart needs
        return {
            "fwd_dist": 100, 
            "dist_perp_obj": 10, 
            "spike_detected": False
        }

    def find_turn_direction(self, scan):
        """Logic to decide left or right based on 180 sweep."""
        # Implementation depends on your environment; defaulting to right for logic flow
        return "right"

    # --- Flowchart Logic ---

    def start_navigation(self):
        print("Starting Navigation...")
        try:
            while True:
                # 180 lidar sweep (simplified to 40 for cruise)
                scan = self.get_lidar_data(mode="cruise")
                
                if scan["fwd_dist"] >= self.DIST_THRESHOLD:
                    # Drive Fwd + Lidar Sweep 40
                    self.drive("fwd")
                else:
                    # Yes -> Stop
                    self.handle_obstacle_avoidance()
                    
        except KeyboardInterrupt:
            self.stop()
            self.set_steering(0)

    def handle_obstacle_avoidance(self):
        self.stop()
        
        # 1. Lidar 180 Sweep & Calculate turn direction
        scan = self.get_lidar_data(mode="180_sweep")
        turn_dir = self.find_turn_direction(scan)
        
        # 2. Turn wheels to Max Angle towards Direction
        steer_val = self.MAX_STEER_ANGLE if turn_dir == "right" else -self.MAX_STEER_ANGLE
        self.set_steering(steer_val)
        
        # 3. Drive for t sec
        self.drive("fwd", duration=self.T_TIME)
        
        # 4. Straighten Wheels & Stop
        self.set_steering(0)
        self.stop()
        
        # 5. Post-Turn Assessment (Biased Sweep)
        self.post_turn_assessment(turn_dir)

    def post_turn_assessment(self, prev_turn):
        # Lidar 180 sweep biased to opposite of turn direction
        bias = "left" if prev_turn == "right" else "right"
        scan = self.get_lidar_data(mode="biased_sweep", bias=bias)
        
        fwd = scan["fwd_dist"]
        lat = scan["dist_perp_obj"]

        # Scenario: Path Clear (fwd >= 30 & dist_perp >= 6)
        if fwd >= self.DIST_THRESHOLD and lat >= self.LATERAL_THRESHOLD:
            # Turn Wheels to Max angle opposite direction
            opp_steer = -self.MAX_STEER_ANGLE if prev_turn == "right" else self.MAX_STEER_ANGLE
            self.set_steering(opp_steer)
            self.drive("fwd", duration=self.T_TIME)
            self.set_steering(0)

        # Scenario: Tight Clearance (fwd >= 30 & dist_perp < 6)
        elif fwd >= self.DIST_THRESHOLD and lat < self.LATERAL_THRESHOLD:
            # Pan Lidar and drive until distance spike
            while not scan["spike_detected"]:
                self.drive("fwd")
                scan = self.get_lidar_data(mode="spike_check")
            self.stop()

        # Scenario: Blocked (fwd < 30)
        elif fwd < self.DIST_THRESHOLD:
            self.drive("reverse", duration=1.0)
            self.stop()

# To run the code:
def main():
    try:
        nav = Navigation(t_seconds=2.0)
        nav.start_navigation()
    except KeyboardInterrupt:
        nav.stop()
        nav.set_steering(0)
        print('program end')
        print()