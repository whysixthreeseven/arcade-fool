# Cache-related modules and scripts import:
from game.scripts import clear_cached_property
from functools import cached_property

# Dataclass import:
from dataclasses import dataclass

# Settings and variables import list:
from game.settings import *


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
AREA DATACLASS BLOCK

"""


@dataclass
class Area:

    # Area attributes:
    area_name: str
    area_coordinate_x_center: int
    area_coordinate_y_center: int
    area_width: int
    area_height: int


    @cached_property
    def area_coordinate_x_left(self) -> int:
        coordinate_x: int = int(self.area_coordinate_x_center - self.area_width / 2)
        return coordinate_x
    

    @cached_property
    def area_coordinate_x_right(self) -> int:
        coordinate_x: int = int(self.area_coordinate_x_center + self.area_width / 2)
        return coordinate_x
    

    @cached_property
    def area_coordinate_y_bottom(self) -> int:
        coordinate_x: int = int(self.area_coordinate_y_center - self.area_height / 2)
        return coordinate_x
    

    @cached_property
    def area_coordinate_y_top(self) -> int:
        coordinate_y: int = int(self.area_coordinate_y_center + self.area_height / 2)
        return coordinate_y


    @cached_property
    def boundary_horizontal(self) -> range:
        boundary_range: range = range(
            self.area_coordinate_x_left,
            self.area_coordinate_x_right
            )
        return boundary_range
    

    @cached_property
    def boundary_vertical(self) -> range:
        boundary_range: range = range(
            self.area_coordinate_y_bottom,
            self.area_coordinate_y_top
            )
        return boundary_range


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
AREA CONTAINERS BLOCK

"""


AREA_PLAYER_ONE_HAND: Area = Area(
    area_name = "Player One hand area",
    area_coordinate_x_center = CARD_COORDINATE_X_HAND_PLAYER,
    area_coordinate_y_center = CARD_COORDINATE_Y_HAND_PLAYER,
    area_width = AREA_PLAYER_ONE_HAND_WIDTH,
    area_height = AREA_PLAYER_ONE_HAND_HEIGHT
    )


AREA_PLAYER_TWO_HAND: Area = Area(
    area_name = "Player Two hand area",
    area_coordinate_x_center = CARD_COORDINATE_X_HAND_OPPONENT,
    area_coordinate_y_center = CARD_COORDINATE_Y_HAND_OPPONENT,
    area_width = AREA_PLAYER_TWO_HAND_WIDTH,
    area_height = AREA_PLAYER_TWO_HAND_HEIGHT
    )


AREA_TABLE: Area = Area(
    area_name = "Table area",
    area_coordinate_x_center = TABLE_COORDINATE_X,
    area_coordinate_y_center = TABLE_COORDINATE_Y,
    area_width = GAME_WINDOW_WIDTH,
    area_height = TABLE_HEIGHT
    )


AREA_INDICATOR_PLAYER_ONE: Area = Area(
    area_name = "Player One indicator area",
    area_coordinate_x_center = TABLE_COORDINATE_X,
    area_coordinate_y_center = AREA_PLAYER_ONE_INDICATOR_COORDINATE_Y,
    area_width = AREA_PLAYER_ONE_INDICATOR_WIDTH,
    area_height = AREA_PLYAER_ONE_INDICATOR_HEIGHT,
    )


AREA_INDICATOR_PLAYER_TWO: Area = Area(
    area_name = "Player Two indicator area",
    area_coordinate_x_center = TABLE_COORDINATE_X,
    area_coordinate_y_center = AREA_PLAYER_TWO_INDICATOR_COORDINATE_Y,
    area_width = AREA_PLAYER_TWO_INDICATOR_WIDTH,
    area_height = AREA_PLAYER_TWO_INDICATOR_HEIGHT,
    )
