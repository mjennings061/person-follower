"""servo_control.py

This file contains code for adjusting servo positions based on face detection."""

import logging
import RPi.GPIO as GPIO
from time import sleep


class Servo:
    """Represents a servo motor."""

    # Constants.
    PWM_FREQUENCY = 50  # Hz
    DEFAULT_PIN = 3
    DEFAULT_ANGLE = 90
    MOVEMENT_DELAY = 0.25

    def __init__(self, pin=DEFAULT_PIN):
        """Initializes the servo.

        Args:
            pin: The pin that the servo is connected to on the GPIO header.
        """
        logging.info(f'Setup servo on pin {pin}.')
        self.pin = pin

        # Setup the GPIO pin.
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.PWM_FREQUENCY)
        
        # Move the servo to the default angle.
        self.set_angle(self.DEFAULT_ANGLE)

    def set_angle(self, angle):
        """Sets the angle of the servo.

        Args:
            angle: The angle to set the servo to.
        """
        logging.info(f'Moving to {angle} degrees.')

        # Update the servo angle.
        self.angle = angle

        # Calculate the duty cycle.
        duty = angle / 18 + 2

        # Move the servo to the given angle.
        self.pwm.start(duty)

        # Allow the servo to move to the given angle.
        sleep(self.MOVEMENT_DELAY)

        # Stop the servo from moving to reduce jitter.
        self.pwm.stop()

    def __del__(self):
        """Cleans up the GPIO pins."""
        logging.info('Cleaning up GPIO pins.')
        self.pwm.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Example GPIO pin.
    gpio_pin = 3
    desired_angles = [0, 45, 90, 135, 180]

    # Adjust the servos based on example angles.
    my_servo = Servo(gpio_pin)

    for desired_angle in desired_angles:
        my_servo.set_angle(desired_angle)

    # Cleanup the GPIO pins.
    del my_servo