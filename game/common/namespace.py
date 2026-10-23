# Typing and annotations:
from typing import Literal


# RGB color variables:
RGB_Color = tuple[int, int, int]
RGBA_Color = tuple[int, int, int, int]
Location = tuple[str, int]
Coordinates = tuple[float, float]
Coordinates_Type = Literal["current", "position", "expected", "hover", "select"]


