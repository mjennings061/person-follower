# person-follower

A silly project to detect and follow people using computer vision on a Raspberry Pi. This will likely snowball into a creepy robot head that follows people around the room.

## Aims

1. Detect people in a video stream.
2. Track people in a video stream as they move.
3. Follow people in a video stream using a servo motor.
4. Infer the project onto a Raspberry Pi.

## Installation

1. Clone the repository using `git clone https://github.com/mjennings061/person-follower.git`
2. Install the dependencies using `pip install -r requirements.txt`.
3. Connect a servo motor to the Raspberry Pi on pin 3 of the GPIO header.
4. Connect a stepper motor to the Raspberry Pi on pins 11, 13, 15, and 16 of the GPIO header. Note, this uses a ULN2003A driver board. Connect the power pins to the 5V and GND pins on the GPIO header.
5. Run the program using `python -m follower.follower`.
