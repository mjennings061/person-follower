"""test_motor_control.py

Unit tests for the motor_control module."""

import unittest
from follower.motor_control import Servo, Stepper


class TestMotorControl(unittest.TestCase):

    def test_servo_movement(self):
        servo = Servo(3)
        servo.set_angle(90)
        assert(servo.angle == 90)

    def test_stepper_movement(self):
        stepper = Stepper([11, 13, 15, 16])
        stepper.move_by_degrees(45)
        assert(stepper.angle == 135)

    def test_stepper_movement_anticlockwise(self):
        stepper = Stepper([11, 13, 15, 16])
        stepper.move_by_degrees(-90)
        assert(stepper.angle == 0)

    def test_stepper_movement_default(self):
        stepper = Stepper()
        stepper.move_by_degrees(50)
        assert(stepper.angle == 140)

    def test_edge_case_stepper_movement(self):
        stepper = Stepper([11, 13, 15, 16])
        stepper.move_by_degrees(360)
        assert(stepper.angle == 90)  # Full rotation should reset angle to 0
        stepper.move_by_degrees(-360)
        assert(stepper.angle == 90)  # Full rotation in opposite direction should also reset angle to 0


if __name__ == '__main__':
    unittest.main()
