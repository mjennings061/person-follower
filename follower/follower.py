"""follower.py

This file is the entry point for the follower module.
"""

import cv2
import logging
from parameters import FRAME_WIDTH, FRAME_HEIGHT
from motor_control import Servo, Stepper
from time import sleep

# # TODO: Delete this when the servo code works as expected on the RPi.
# class Servo:
#     # Dummy class for now.
#     def __init__(self, pin=11):
#         self.pin = pin
#         self.set_angle()

#     def set_angle(self, angle=90):
#         logging.info(f'Moving to {angle} degrees.')
#         self.angle = angle
#         sleep(0.5)


# # TODO: Delete this when the stepper code works as expected on the RPi.
# class Stepper:
#     # Dummy class for now.
#     def __init__(self, pins=[11, 13, 15, 16]):
#         self.pins = pins
#         self.angle = 90

#     def move_by_degrees(self, degrees):
#         logging.info(f'Moving by {degrees} degrees...')
#         self.angle += degrees
#         sleep(0.01 * abs(degrees) * 2048 / 360)
#         logging.info(f'At {self.angle} degrees')


def update_motor_angle(motor, avg_x):
    """Updates the servo angle based on the average x coordinate of the faces.
    
    Args:
        motor: The motor to update. Must be an instance of Servo or Stepper.
        avg_x: The average x coordinate of the faces.
    """

    # Constants.
    MAX_ANGLE = 180
    MIN_ANGLE = 0
    GAIN = 0.05

    # Calculate the error.
    error = avg_x - FRAME_WIDTH / 2
    logging.info(f'Error: {error}')

    # Calculate the new angle.
    angle = round(motor.angle + error * GAIN)

    # Limit the angle to the range [MIN_ANGLE, MAX_ANGLE].
    angle = max(angle, MIN_ANGLE)
    angle = min(angle, MAX_ANGLE)

    # Set the new angle.
    if isinstance(motor, Servo):
        motor.set_angle(angle)
    elif isinstance(motor, Stepper):
        # Calculate the degrees to rotate the stepper motor.
        degrees = angle - motor.angle
        motor.move_by_degrees(degrees)


def calculate_average_face_pos(faces):
        """Calculates the average x coordinate of the given faces.
        
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


def display_faces(frame, faces):
    """Draws rectangles around the detected faces in the given frame.
    
    Args:
        frame: The frame to draw the rectangles on.
        faces: A list of rectangles, each of which represents a face in the frame.
    """

    # Constants.
    COLOUR = (0, 255, 0)
    THICKNESS = 2
    TEXT_COLOUR = (0, 0, 255)
    TEXT_SIZE = 1
    TEXT_THICKNESS = 2

    # Show each face in the frame.
    for (x_pixel, y_pixel, width, height) in faces:
        # Draw rectangles around the detected faces.
        cv2.rectangle(
            frame, 
            (x_pixel, y_pixel), 
            (x_pixel + width, y_pixel + height), 
            COLOUR, 
            THICKNESS
        )

        # Display the X and Y coordinates of the face.
        x_position = round(x_pixel + width / 2)
        y_position = round(y_pixel + height / 2)
        display_text = f'({x_position}, {y_position})'
        cv2.putText(
            frame, 
            display_text, 
            (x_pixel, y_pixel), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            TEXT_SIZE, 
            TEXT_COLOUR, 
            TEXT_THICKNESS
        )

    # Display the frame with face detection.
    cv2.imshow('Face Detection', frame)


def adjust_brightness(frame):
    """Adjusts the brightness of the given frame.
    
    Args:
        frame: The frame to adjust the brightness of.
        
    Returns:
        The adjusted frame.
    """
    # Set target brightness value.
    TARGET_BRIGHTNESS = 100

    # Calculate the average brightness of the frame.
    avg_brightness = cv2.mean(frame)[0]
    brightness = TARGET_BRIGHTNESS - avg_brightness

    # Adjust brightness and gamma of the frame.
    adjusted_frame = cv2.convertScaleAbs(frame, alpha=1, beta=brightness)
    return adjusted_frame


def detect_faces(frame, face_cascade):
    """Detects faces in the given frame using the given face detection model.
    
    Args:
        frame: The frame to detect faces in.
        face_cascade: The face detection model to use.
        
    Returns:
        A list of rectangles, each of which represents a face in the frame.
    """
    # Convert the frame to grayscale.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection.
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces


def run_follower():
    """The entry point for the follower module.

    This function will be called when the follower module is run as a script.
    """

    # Setup the servo.
    motor = Stepper()

    # Load the pre-trained face detection model.
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    # Open the webcam.
    cap = cv2.VideoCapture(0)

    # Set resolution.
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    while True:
        # Read the frame from the webcam.
        ret, frame = cap.read()

        # Break the loop if the frame is not read correctly.
        if not ret:
            break

        # Adjust the brightness of the frame.
        adjusted_frame = adjust_brightness(frame)

        # Detect faces.
        faces = detect_faces(adjusted_frame, face_cascade)

        # Display the frame with face detection.
        display_faces(adjusted_frame, faces)
        
        if len(faces) > 0:
            # Calculate the average x coordinate of the faces.
            avg_x = calculate_average_face_pos(faces)

            # Adjust the motor position based on the average x coordinate of the faces.
            # Use a proportional controller to update the motor angle.
            update_motor_angle(motor, avg_x)

        # Break the loop if 'q' is pressed.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window.
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_follower()
