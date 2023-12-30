"""test_follower.py 

Unit tests for the follower module."""

import unittest
from unittest.mock import Mock
from follower.follower import *


class TestUpdateMotorAngle(unittest.TestCase):
    """
    A test case for the update_motor_angle function.
    """

    def test_update_motor_angle_servo(self):
        """
        Test case for updating motor angle for a servo.
        """
        servo = Mock(spec=Servo)
        servo.angle = 90
        update_motor_angle(servo, 100)
        servo.set_angle.assert_called_once()

    def test_update_motor_angle_stepper(self):
        """
        Test case for updating motor angle for a stepper motor.
        """
        stepper = Mock(spec=Stepper)
        stepper.angle = 90
        update_motor_angle(stepper, 100)
        stepper.move_by_degrees.assert_called_once()


class TestCalculateAverageFacePos(unittest.TestCase):
    """
    Test case for calculate average face position function.
    """

    def test_average_face_position(self):
        """
        Test case for calculating the average face position.
        """
        faces = [(10, 20, 30, 40), (50, 60, 70, 80)]
        avg_x = calculate_average_face_pos(faces)
        self.assertEqual(avg_x, 55)  # (20 + 50) / 2


if __name__ == '__main__':
    unittest.main()

