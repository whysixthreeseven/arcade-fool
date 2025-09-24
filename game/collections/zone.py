# Dataclass import:
from dataclasses import dataclass

# Cache-related import:
from functools import cached_property

# Arcade library import:
import arcade
from arcade import Rect, Text
from arcade.types import Color

# Card-related settings import:
from game.settings import *


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ZONE DATACLASS BLOCK
"""


@dataclass(order = True, frozen = True)
class Zone_XYWH:

    # Info attribute
    name: str

    # Coordinates attribute:
    coordinate_x: int
    coordinate_y: int

    # Width and height attributes:
    width: int
    height: int

    # Background color (debug)
    color: arcade.color


    @cached_property
    def coordinate_x_left(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        coordinate_x: int = int(self.coordinate_x - self.width / 2)

        # Returning:
        return coordinate_x
    

    @cached_property
    def coordinate_x_right(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        coordinate_x: int = int(self.coordinate_x + self.width / 2)

        # Returning:
        return coordinate_x
    

    @cached_property
    def coordinate_y_bottom(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        coordinate_y: int = int(self.coordinate_y - self.height / 2)

        # Returning:
        return coordinate_y


    @cached_property
    def coordinate_y_top(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        coordinate_y: int = int(self.coordinate_y + self.height / 2)

        # Returning:
        return coordinate_y
    

    @cached_property
    def coordinate_x_boundary(self) -> range:
        """
        TODO: Create a docstring.
        """

        # Packing a range:
        coordinate_x_range: range = range(
            self.coordinate_x_left,
            self.coordinate_x_right
            )
        
        # Returning:
        return coordinate_x_range


    @cached_property
    def coordinate_y_boundary(self) -> range:
        """
        TODO: Create a docstring.
        """

        # Packing a range:
        coordinate_y_range: range = range(
            self.coordinate_y_bottom,
            self.coordinate_y_top
            )
        
        # Returning:
        return coordinate_y_range
    

    @cached_property
    def __render_rect(self) -> Rect:
        """
        TODO: Create a docstring.
        """

        # Creating a new rectangle object:
        render_rect: Rect = arcade.XYWH(
            x      = self.coordinate_x,
            y      = self.coordinate_y,
            width  = self.width,
            height = self.height,
            )
        
        # Returning:
        return render_rect
    

    @cached_property
    def __render_text(self) -> Text:
        """
        TODO: Create a docstring.
        """

        # Generating coordinates:
        coordinate_shift: int = 4
        coordinate_x: int = self.coordinate_x_left + coordinate_shift
        coordinate_y: int = self.coordinate_y_top - coordinate_shift

        # Other text variables:
        text_formatted: str = self.name.upper()
        text_color: Color = Color(15, 15, 15, 255)
        text_font_name: str = "Verdana"
        text_font_size: int = 10
        text_anchor_x: str = "left"
        text_anchor_y: str = "center"
        text_rotation: int = 0

        # Creating a Text object:
        render_text: Text = Text(
            text      = text_formatted,
            x         = coordinate_x,
            y         = coordinate_y,
            color     = text_color,
            font_name = text_font_name,
            font_size = text_font_size,
            anchor_x  = text_anchor_x,
            anchor_y  = text_anchor_y,
            rotation  = text_rotation,
            )
        
        # Returning:
        return render_text


    def render(self, render_text: bool = False) -> None:
        """
        TODO: Create a docstring.
        """

        # Rendering zone as filled rectangle:
        arcade.draw_rect_filled(
            rect       = self.__render_rect,
            color      = self.color,
            tilt_angle = 0
            )
        
        # Rendering text, if required:
        if render_text:
            self.__render_text.draw()
    

"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ZONE DATACLASS COLLECTION BLOCK
"""


ZONE_GAME_AREA_PLAY: Zone_XYWH = Zone_XYWH(
    name         = "Game area play zone",
    coordinate_x = GAME_AREA_PLAY_COORDINATE_X,
    coordinate_y = GAME_AREA_PLAY_COORDINATE_Y,
    width        = GAME_AREA_PLAY_WIDTH,
    height       = GAME_AREA_PLAY_HEIGHT,
    color        = GAME_AREA_PLAY_BG_COLOR
    )


ZONE_GAME_AREA_SIDE: Zone_XYWH = Zone_XYWH(
    name         = "Game area side zone",
    coordinate_x = GAME_AREA_SIDE_COORDINATE_X,
    coordinate_y = GAME_AREA_SIDE_COORDINATE_Y,
    width        = GAME_AREA_SIDE_WIDTH,
    height       = GAME_AREA_SIDE_HEIGHT,
    color        = GAME_AREA_SIDE_BG_COLOR,
    )


ZONE_PLAYER_ONE: Zone_XYWH = Zone_XYWH(
    name         = "Player one zone",
    coordinate_x = ZONE_PLAYER_ONE_COORDINATE_X,
    coordinate_y = ZONE_PLAYER_ONE_COORDINATE_Y,
    width        = ZONE_PLAYER_ONE_WIDTH,
    height       = ZONE_PLAYER_ONE_HEIGHT,
    color        = ZONE_PLAYER_ONE_BG_COLOR,
    )


ZONE_PLAYER_TWO: Zone_XYWH = Zone_XYWH(
    name         = "Player two zone",
    coordinate_x = ZONE_PLAYER_TWO_COORDINATE_X,
    coordinate_y = ZONE_PLAYER_TWO_COORDINATE_Y,
    width        = ZONE_PLAYER_TWO_WIDTH,
    height       = ZONE_PLAYER_TWO_HEIGHT,
    color        = ZONE_PLAYER_TWO_BG_COLOR,
    )


ZONE_TABLE: Zone_XYWH = Zone_XYWH(
    name         = "Table zone",
    coordinate_x = ZONE_TABLE_COORDINATE_X,
    coordinate_y = ZONE_TABLE_COORDINATE_Y,
    width        = ZONE_TABLE_WIDTH,
    height       = ZONE_TABLE_HEIGHT,
    color        = ZONE_TABLE_BG_COLOR
    )


ZONE_INDICATOR_PLAYER_ONE: Zone_XYWH = Zone_XYWH(
    name         = "Indicator player one zone",
    coordinate_x = ZONE_INDICATOR_PLAYER_ONE_COORDINATE_X,
    coordinate_y = ZONE_INDICATOR_PLAYER_ONE_COORDINATE_Y,
    width        = ZONE_INDICATOR_PLAYER_ONE_WIDTH,
    height       = ZONE_INDICATOR_PLAYER_ONE_HEIGHT,
    color        = ZONE_INDICATOR_PLAYER_ONE_COLOR,
    )


ZONE_INDICATOR_PLAYER_TWO: Zone_XYWH = Zone_XYWH(
    name         = "Indicator player two zone",
    coordinate_x = ZONE_INDICATOR_PLAYER_TWO_COORDINATE_X,
    coordinate_y = ZONE_INDICATOR_PLAYER_TWO_COORDINATE_Y,
    width        = ZONE_INDICATOR_PLAYER_TWO_WIDTH,
    height       = ZONE_INDICATOR_PLAYER_TWO_HEIGHT,
    color        = ZONE_INDICATOR_PLAYER_TWO_COLOR,
    )


ZONE_DECK: Zone_XYWH = Zone_XYWH(
    name         = "Deck zone",
    coordinate_x = ZONE_DECK_COORDINATE_X,
    coordinate_y = ZONE_DECK_COORDINATE_Y,
    width        = ZONE_DECK_WIDTH,
    height       = ZONE_DECK_HEIGHT,
    color        = ZONE_DECK_BG_COLOR
    )


ZONE_DISCARD: Zone_XYWH = Zone_XYWH(
    name         = "Discard zone",
    coordinate_x = ZONE_DISCARD_COORDINATE_X,
    coordinate_y = ZONE_DISCARD_COORDINATE_Y,
    width        = ZONE_DISCARD_WIDTH,
    height       = ZONE_DISCARD_HEIGHT,
    color        = ZONE_DISCARD_BG_COLOR
    )

