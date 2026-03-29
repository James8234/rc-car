from time import sleep
from fusion_hat.motor import Motor

class BaseMotor:
    power_offset = 0.0

    def __init__(self, motor_port, speed):
        self.motor = Motor(motor_port, is_reversed=False)
        self.speed = speed

    def _apply_offset(self, speed_value):
        adjusted = speed_value + self.power_offset
        return max(-100, min(100, adjusted))

    def _set_power(self, speed_value):
        self.motor.power(self._apply_offset(speed_value))

    def _change_offset(self, delta):
        self.__class__.power_offset = round(self.__class__.power_offset + delta, 2)
        self._print_offsets()

    @staticmethod
    def _print_offsets():
        print(
            f"Left offset: {LeftMotor.power_offset:.2f} | "
            f"Right offset: {RightMotor.power_offset:.2f}"
        )

    def motor_control(self, key):
        last_speed = self.speed

        match key:
            case '1':
                self.speed = 25
            case '2':
                self.speed = 40
            case '3':
                self.speed = 75
            case '4':
                self.speed = 100

        if last_speed != self.speed:
            self._set_power(self.speed)

        match key:
            case 'w':
                self._set_power(self.speed)
            case 's':
                self._set_power(-self.speed)
            case 'e':
                self.motor.stop()
            case 'q':
                self.motor.stop()
                sleep(0.1)


class LeftMotor(BaseMotor):
    power_offset = 0.0

    def motor_control(self, key):
        match key:
            case 'u':
                self._change_offset(0.05)
                return
            case 'j':
                self._change_offset(-0.05)
                return
        super().motor_control(key)


class RightMotor(BaseMotor):
    power_offset = 0.0

    def motor_control(self, key):
        match key:
            case 'i':
                self._change_offset(0.05)
                return
            case 'k':
                self._change_offset(-0.05)
                return
        super().motor_control(key)
