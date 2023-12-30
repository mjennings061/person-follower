"""parameters.py

This file contains constants used by the follower module."""


from dataclasses import dataclass


@dataclass
class Parameters:
    FRAME_WIDTH: int = 640
    FRAME_HEIGHT: int = 480
