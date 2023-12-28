"""servo_control.py

This file contains code for adjusting servo positions based on face detection."""

from parameters import FRAME_WIDTH, FRAME_HEIGHT

# Constants.
PAN_SPEED = 10
TILT_SPEED = 10


def calculate_face_positions(faces):
    """Calculates the average x and y coordinates of the given faces.
    
    Args:
        faces: A list of rectangles, each of which represents a face in the frame.
        
    Returns:
        The average x coordinate of the faces.
    """
    avg_x = 0
    for (x_pixel, _, width, _) in faces:
        avg_x += x_pixel + width / 2
    avg_x /= len(faces)
    return avg_x


def adjust_servos(faces):
    """Adjusts the pan and tilt of the servos based on the given faces.
    
    Args:
        faces: A list of rectangles, each of which represents a face in the frame.
    """

    # Calculate the average x and y coordinates of the faces.
    avg_x = calculate_face_positions(faces)

    # Calculate the difference between the average xcoordinates and the center of the frame.
    # The difference is normalized to be between -1 and 1.
    x_diff = (avg_x - FRAME_WIDTH / 2) / (FRAME_WIDTH / 2)

    # TODO: Setup the raspberry pi pan servo.
    # TODO: Get the current angle of the pan servo.
    # TODO: Adjust the pan of the servos based on the difference.

    # Adjust the pan of the servos based on the difference.
    angle = angle + x_diff * PAN_SPEED


if __name__ == '__main__':
    # Example faces.
    example_faces = [
        (100, 100, 100, 100),
        (200, 200, 100, 100),
        (300, 300, 150, 150),
    ]

    # Adjust the servos based on the example faces.
    adjust_servos(example_faces)