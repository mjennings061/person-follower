"""main.py

This file is the entry point for the follower module.
"""

import cv2


def main():
    """The entry point for the follower module.

    This function will be called when the follower module is run as a script.
    """
    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Set initial brightness and gamma values
    brightness = 0
    gamma = 1

    while True:
        # Read the frame from the webcam
        ret, frame = cap.read()

        # Adjust brightness and gamma
        adjusted_frame = cv2.convertScaleAbs(frame, alpha=gamma, beta=brightness)

        # Convert the frame to grayscale
        gray = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(adjusted_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the frame with face detection
        cv2.imshow('Face Detection', adjusted_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Calculate the average brightness of the frame
        avg_brightness = cv2.mean(gray)[0]

        # Adjust brightness and gamma dynamically
        if avg_brightness < 50:
            brightness += 1
        elif avg_brightness > 100:
            brightness -= 1
        # gamma += 0.1

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
