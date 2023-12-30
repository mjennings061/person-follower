""" mock_gpio.py

This file contains a mock class for GPIO operations when running the follower module
without a Raspberry Pi e.g. on windows."""

class MockGPIO:
    """
    A mock class for GPIO operations.

    This class provides methods to simulate GPIO operations such as setting up pins,
    setting pin states, starting PWM, and cleaning up GPIO pins.

    Attributes:
        BOARD (str): The board mode for GPIO.
        OUT (str): The output mode for GPIO.

    Methods:
        setmode(mode): Sets the GPIO mode.
        setup(pin, mode): Sets up a pin in a specific mode.
        output(pin, state): Sets the state of a pin.
        cleanup(): Cleans up GPIO pins.
        PWM(pin, frequency): Starts PWM on a pin with a specific frequency.

    Example usage:
        gpio = MockGPIO()
        gpio.setmode(MockGPIO.BOARD)
        gpio.setup(12, MockGPIO.OUT)
        gpio.output(12, True)
        gpio.cleanup()
        pwm = gpio.PWM(18, 100)
    """
    BOARD = 'BOARD'
    OUT = 'OUT'

    @staticmethod
    def setmode(mode):
        pass

    @staticmethod
    def setup(pin, mode):
        pass

    @staticmethod
    def output(pin, state):
        pass

    @staticmethod
    def cleanup():
        pass

    @staticmethod
    def PWM(pin, frequency):
        pass
        return MockPWM(pin, frequency)

class MockPWM:
    def __init__(self, pin, frequency):
        self.pin = pin
        self.frequency = frequency

    def start(self, duty_cycle):
        pass

    def ChangeDutyCycle(self, duty_cycle):
        pass

    def stop(self):
        pass