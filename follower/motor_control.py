"""motor_control.py

This file contains code for adjusting servo positions based on face detection."""

import logging
from time import sleep

# Platform-specific imports.
import platform
if platform.system() == 'Windows':
    from follower.mock_gpio import MockGPIO as GPIO
else:
    import RPi.GPIO as GPIO     # type: ignore

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
        self.pwm.ChangeDutyCycle(duty)

        # Allow the servo to move to the given angle.
        sleep(self.MOVEMENT_DELAY)

        # Stop the servo from moving to reduce jitter.
        self.pwm.ChangeDutyCycle(0)

    def __del__(self):
        """Cleans up the GPIO pins."""
        logging.info('Cleaning up GPIO pins.')
        self.pwm.stop()
        GPIO.cleanup()


class Stepper:
    """Represents a stepper motor."""

    # Constants.
    DEFAULT_PINS = [11, 13, 15, 16]
    MOVEMENT_DELAY = 0.001
    STEPS_PER_REVOLUTION = 4096
    DEFAULT_ANGLE = 90
    STEP_SEQUENCE = [
        [1, 0, 0, 1], 
        [1, 0, 0, 0], 
        [1, 1, 0, 0], 
        [0, 1, 0, 0], 
        [0, 1, 1, 0], 
        [0, 0, 1, 0], 
        [0, 0, 1, 1], 
        [0, 0, 0, 1]
    ]

    def __init__(self, pins=DEFAULT_PINS):
        """Initializes the stepper.

        Args:
            pin: The pins that the stepper is connected to on the GPIO header.
        """
        logging.info(f'Setup stepper on pins {pins}.')
        self.pins = pins

        # Setup the GPIO pins.
        GPIO.setmode(GPIO.BOARD)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

        # Assume that the stepper is at the default angle.
        self.angle = self.DEFAULT_ANGLE
        self.current_step = 0

    def move_by_degrees(self, degrees):
        """Sets the angle of the stepper.

        Args:
            angle: The angle to set the stepper to.
        """
        # Log the movement.
        logging.info(f'Moving by {degrees} degrees...')

        # Update the stepper angle.
        angle = (self.angle + degrees) % 360
        if angle < 0:
            angle += 360
        self.angle = angle

        # Calculate the number of steps to move.
        steps = round(degrees * self.STEPS_PER_REVOLUTION / 360)

        # Move the stepper.
        self._move_steps(steps)
        logging.info(f'At {self.angle} degrees')


    def _move_steps(self, steps):
        """Moves the stepper by the given number of steps.

        Args:
            steps: The number of steps to move the stepper. 
                Positive steps means clockwise, negative steps means counterclockwise.
        """
        # Number of motor states.
        n_states = len(self.STEP_SEQUENCE)

        # Move the stepper.
        for _ in range(abs(steps)):
            # Determine next index in the motor circular buffer of pin states.
            if steps >= 0:
                current_step = (self.current_step + 1) % n_states
            else:
                current_step = (self.current_step - 1) % n_states
            self.current_step = current_step

            # Get the next step.
            motor_sequence = self.STEP_SEQUENCE[self.current_step]
            for pin, state in zip(self.pins, motor_sequence):
                GPIO.output(pin, state)
            sleep(self.MOVEMENT_DELAY)

    def __del__(self):
        """Cleans up the GPIO pins."""
        logging.info('Cleaning up GPIO pins.')
        GPIO.cleanup()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Test the servo.
    logging.info('Testing the servo.')

    # Example GPIO pin.
    gpio_pin = 3
    desired_angles = [0, 45, 90, 135, 180]

    # Adjust the servos based on example angles.
    my_servo = Servo(gpio_pin)
    for desired_angle in desired_angles:
        my_servo.set_angle(desired_angle)

    # Cleanup the GPIO pins.
    del my_servo

    # Test the stepper.
    logging.info('Testing the stepper.')

    # Example GPIO pins.
    gpio_pins = [11, 13, 15, 16]
    desired_steps = [45, -90, 90, -45]

    # Adjust the stepper based on example angles.
    my_stepper = Stepper(gpio_pins)
    for desired_step in desired_steps:
        my_stepper.move_by_degrees(desired_step)
        sleep(1)