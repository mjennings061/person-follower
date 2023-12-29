"""servo_control.py

This file contains code for adjusting servo positions based on face detection."""

import logging
import RPi.GPIO as GPIO
from time import sleep


class Servo:
    """Represents a servo motor."""

    # Constants.
    DEFAULT_PIN = 11
    DEFAULT_ANGLE = 90
    MOVEMENT_DELAY = 0.5

    def __init__(self, pin=DEFAULT_PIN):
        """Initializes the servo.

        Args:
            pin: The GPIO pin that the servo is connected to.
        """
        logging.info(f'Setup servo on pin {pin}.')
        self.pin = pin

        # Setup the GPIO pin.
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)
        
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
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)

        # Allow the servo to move to the given angle.
        sleep(self.MOVEMENT_DELAY)

        # Stop the servo from moving to reduce jitter.
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)


if __name__ == '__main__':
    # Example GPIO pin.
    gpio_pin = 11
    desired_angle = 90

    # Adjust the servos based on the example faces.
    my_servo = Servo(gpio_pin)
    my_servo.set_angle(desired_angle)