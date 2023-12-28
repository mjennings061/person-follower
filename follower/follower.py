"""follower.py

This file is the entry point for the follower module.
"""

import cv2


def display_faces(frame, faces):
    """Draws rectangles around the detected faces in the given frame.
    
    Args:
        frame: The frame to draw the rectangles on.
        faces: A list of rectangles, each of which represents a face in the frame.
    """
    # Draw rectangles around the detected faces.
    COLOUR = (0, 255, 0)
    THICKNESS = 2
    for (x_pixel, y_pixel, width, height) in faces:
        cv2.rectangle(
            frame, 
            (x_pixel, y_pixel), 
            (x_pixel + width, y_pixel + height), 
            COLOUR, 
            THICKNESS
        )

    # Display the frame with face detection
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
    # Load the pre-trained face detection model.
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the webcam.
    cap = cv2.VideoCapture(0)

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

        # Break the loop if 'q' is pressed.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window.
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run_follower()
