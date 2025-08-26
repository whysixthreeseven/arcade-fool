# Cache-related modules and scripts import:
from game.scripts import clear_cached_property
from functools import cached_property

# Dataclass import:
from dataclasses import dataclass

# Settings and variables import list:
from game.variables import *
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
    area_name = "Player One Hand Area",
    area_coordinate_x_center = CARD_COORDINATE_X_HAND_PLAYER,
    area_coordinate_y_center = CARD_COORDINATE_Y_HAND_PLAYER,
    area_width = GAME_WINDOW_WIDTH,
    area_height = int(
        CARD_TEXTURE_HEIGHT_SCALED * 2.00   # Fine-tuned modifier
        ),
    )


AREA_PLAYER_TWO_HAND: Area = Area(
    area_name = "Player Two Hand Area",
    area_coordinate_x_center = CARD_COORDINATE_X_HAND_OPPONENT,
    area_coordinate_y_center = CARD_COORDINATE_Y_HAND_OPPONENT,
    area_width = GAME_WINDOW_WIDTH,
    area_height = int(
        CARD_TEXTURE_HEIGHT_SCALED * 2.00   # Fine-tuned modifier
        ),
    )


AREA_TABLE: Area = Area(
    area_name = "Table Area",
    area_coordinate_x_center = TABLE_COORDINATE_X,
    area_coordinate_y_center = TABLE_COORDINATE_Y,
    area_width = GAME_WINDOW_WIDTH,
    area_height = TABLE_HEIGHT
    )
