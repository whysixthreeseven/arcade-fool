# Typing and annotations:
from typing import Literal


# RGB color variables:
RGB = tuple[int, int, int]
RGBA = tuple[int, int, int, int]
Location = tuple[str, int]
Coordinates = tuple[float, float]
CoordinatesType = Literal["current", "position", "expected", "hover", "select"]
StateType = Literal["hovered", "selected", "playable", "controlled", "ready", "showcase"]


