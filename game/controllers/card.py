# Annotations, typing etc. import:
from __future__ import annotations
from typing import Any, Optional

# System management import:
import os

# Cache-related import:
from functools import cached_property

# Random library import:
import random

# Arcade library import:
import arcade
from arcade import Rect, Text, Texture

# Card-related variables import:
from game.variables import (

    # Suit variables:
    CARD_SUIT_TAG,
    CARD_SUIT_NOT_SET,
    CARD_SUIT_HEARTS,
    CARD_SUIT_DIAMONDS,
    CARD_SUIT_CLUBS,
    CARD_SUIT_SPADES,

    # Suit color variables:
    CARD_SUIT_COLOR_TAG,
    CARD_SUIT_COLOR_NOT_SET,
    CARD_SUIT_COLOR_RED,
    CARD_SUIT_COLOR_BLACK,

    # Suit ASCII variables:
    CARD_SUIT_NOT_SET_ASCII,
    CARD_SUIT_HEARTS_ASCII,
    CARD_SUIT_DIAMONDS_ASCII,
    CARD_SUIT_CLUBS_ASCII,
    CARD_SUIT_SPADES_ASCII,

    # Type variables:
    CARD_TYPE_TAG,
    CARD_TYPE_NOT_SET,
    CARD_TYPE_TWO,
    CARD_TYPE_THREE,
    CARD_TYPE_FOUR,
    CARD_TYPE_FIVE,
    CARD_TYPE_SIX,
    CARD_TYPE_SEVEN,
    CARD_TYPE_EIGHT,
    CARD_TYPE_NINE,
    CARD_TYPE_TEN,
    CARD_TYPE_JACK,
    CARD_TYPE_QUEEN,
    CARD_TYPE_KING,
    CARD_TYPE_ACE,

    # Location variables:
    CARD_LOCATION_TAG,
    CARD_LOCATION_NOT_SET,
    CARD_LOCATION_HAND,
    CARD_LOCATION_DECK,
    CARD_LOCATION_DISCARD,
    CARD_LOCATION_TABLE,
    )

# Card- and texture-related directory variables import:
from game.directory import (
    DIR_TEXTURES_CARD_FRONT_PATH,
    DIR_TEXTURES_CARD_BACK_PATH,
    )

# Related settings import:
from game.settings import (

    # Card-related settings:
    CARD_RENDER_SCALE_DEFAULT_MOD,
    CARD_RENDER_ANGLE_DEFAULT,
    CARD_RENDER_ANGLE_OPPONENT,
    CARD_RENDER_ANGLE_MIN,
    CARD_RENDER_ANGLE_MAX,
    CARD_RENDER_ANGLE_AXIS_LIST,
    CARD_TEXTURE_WIDTH_SCALED,
    CARD_TEXTURE_HEIGHT_SCALED,
    CARD_SLIDE_SPEED_DEFAULT,
    CARD_SLIDE_SPEED_THROTTLE,
    CARD_SLIDE_SPEED_MODIFIER_DEFAULT,
    CARD_SLIDE_SPEED_MODIFIER_SLOW,
    CARD_SLIDE_SPEED_MODIFIER_FAST,

    # Table positions and stack index:
    TABLE_STACK_TOP_INDEX,
    TABLE_STACK_BOTTOM_INDEX,
    TABLE_STACK_RANGE,
    TABLE_POSITION_MIN,
    TABLE_POSITION_MAX,
    TABLE_POSITION_RANGE,
    ZONE_TABLE_COORDINATE_Y,

    # Deck-related settings:
    DECK_RENDER_ANGLE_SHOWCASE,
    DECK_RENDER_ANGLE_ADD_MIN,
    DECK_RENDER_ANGLE_ADD_MAX,
    DECK_SIZE_MAX,

    )

# Session-related import:
from game.session import (
    SESSION_ENABLE_ASSERTION,
    SESSION_ENABLE_ECHO,
    )

# Collections import:
from game.collections.texturepack import (

    # Texture packs:
    Texture_Pack, 
    TEXTURE_PACK_FRONT_LIGHT_DEFAULT,
    TEXTURE_PACK_BACK_LIGHT_DEFAULT,
    )

# Scripts import:
from game.scripts.convert import (
    convert_attribute_to_repr,
    convert_value_to_integer,
    )
from game.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list
    )
from game.scripts.assertion import (
    assert_value_is_default,
    assert_value_is_positive,
    assert_value_is_valid_type,
    assert_value_in_valid_range,
    assert_container_is_valid_size,
    )


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CARD OBJECT CLASS BLOCK

"""


class Card_Object:

    # Card suit_list:
    CARD_SUIT_LIST: tuple[str, ...] = (
        CARD_SUIT_HEARTS,
        CARD_SUIT_DIAMONDS,
        CARD_SUIT_CLUBS,
        CARD_SUIT_SPADES,
        )

    # Card suit index:
    CARD_SUIT_COLOR_INDEX: dict[str, str] = {
        CARD_SUIT_NOT_SET:  CARD_SUIT_COLOR_NOT_SET,
        CARD_SUIT_HEARTS:   CARD_SUIT_COLOR_RED,
        CARD_SUIT_DIAMONDS: CARD_SUIT_COLOR_RED,
        CARD_SUIT_CLUBS:    CARD_SUIT_COLOR_BLACK,
        CARD_SUIT_SPADES:   CARD_SUIT_COLOR_BLACK,
        }
    
    # Card suit ASCII index:
    CARD_SUIT_ASCII_INDEX: dict[str, str] = {
        CARD_SUIT_NOT_SET:  CARD_SUIT_NOT_SET_ASCII,
        CARD_SUIT_HEARTS:   CARD_SUIT_HEARTS_ASCII,
        CARD_SUIT_DIAMONDS: CARD_SUIT_DIAMONDS_ASCII,
        CARD_SUIT_CLUBS:    CARD_SUIT_CLUBS_ASCII,
        CARD_SUIT_SPADES:   CARD_SUIT_SPADES_ASCII,
        }
    
    # Card type list:
    CARD_TYPE_LIST: tuple[str, ...] = (
        CARD_TYPE_TWO,
        CARD_TYPE_THREE,
        CARD_TYPE_FOUR,
        CARD_TYPE_FIVE,
        CARD_TYPE_SIX,
        CARD_TYPE_SEVEN,
        CARD_TYPE_EIGHT,
        CARD_TYPE_NINE,
        CARD_TYPE_TEN,
        CARD_TYPE_JACK,
        CARD_TYPE_QUEEN,
        CARD_TYPE_KING,
        CARD_TYPE_ACE,
        )

    # Card value default index:
    CARD_TYPE_VALUE_INDEX: dict[str, int] = {
        CARD_TYPE_NOT_SET: 0,
        CARD_TYPE_TWO:     2,
        CARD_TYPE_THREE:   3,
        CARD_TYPE_FOUR:    4,
        CARD_TYPE_FIVE:    5,
        CARD_TYPE_SIX:     6,
        CARD_TYPE_SEVEN:   7,
        CARD_TYPE_EIGHT:   8,
        CARD_TYPE_NINE:    9,
        CARD_TYPE_TEN:     10,
        CARD_TYPE_JACK:    11,
        CARD_TYPE_QUEEN:   12,
        CARD_TYPE_KING:    13,
        CARD_TYPE_ACE:     14,
        }
    
    # Card trump modifier:
    CARD_TRUMP_VALUE_MODIFIER: int = 100


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    INITIALIZER AND CORE ATTRIBUTES BLOCK
    
    """


    def __init__(self):
        
        # Core attributes:
        self.__type: str = CARD_TYPE_NOT_SET
        self.__suit: str = CARD_SUIT_NOT_SET

        # State attributes:
        self.__state_selected: bool = False
        self.__state_hovered:  bool = False
        self.__state_trump:    bool = False
        self.__state_revealed: bool = False
        self.__state_opponent: bool = False
        self.__state_playable: bool = False
        self.__state_showcase: bool = False
        self.__state_arrived:  bool = False
        
        # Position attributes:
        self.__position_hand:    int | None = None
        self.__position_added:   int | None = None
        self.__position_deck:    int | None = None
        self.__position_discard: int | None = None
        self.__position_table:   int | None = None
        self.__position_index:   int | None = None

        # Texture-related attributes:
        self.__texture_pack_front:   Texture_Pack = None
        self.__texture_pack_back:    Texture_Pack = None
        self.__texture_front_object: Texture = None
        self.__texture_back_object:  Texture = None

        # Coordinates attributes:
        self.__coordinate_x_current: int = 0
        self.__coordinate_y_current: int = 0
        self.__coordinate_x_default: int = 0
        self.__coordinate_y_default: int = 0
        self.__coordinate_x_slide:   int = 0
        self.__coordinate_y_slide:   int = 0

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    OVERWRITTEN MAGIC METHODS BLOCK
    
    """

    
    def __str__(self):
        """
        TODO: Create a docstring.
        """

        # Generating new string value:
        echo_string: str = f"{self.suit_ascii}{self.type_ascii}"

        # Returning:
        return echo_string
    

    def __repr__(self):
        """
        TODO: Create a docstring.
        """

        # Generating new string value:
        echo_string: str = f"{self.suit_ascii}{self.type_ascii}"

        # Returning:
        return echo_string
    

    def __gt__(self, card_object: Card_Object) -> bool:
        """
        TODO: Create a docstring
        """

        # Checking if suits are compatible:
        eval_result: bool = False
        eval_available: bool = bool(
            (self.suit == card_object.suit or self.state_trump) and
            self.state_ready and card_object.state_ready
            )

        # Comparing values:
        if eval_available:
            if self.type_value > card_object.type_value:
                eval_result: bool = True

        # Returning:
        return eval_result
    

    def __lt__(self, card_object: Card_Object) -> bool:
        """
        TODO: Create a docstring
        """

        # Checking if suits are compatible:
        eval_result: bool = False
        eval_available: bool = bool(
            self.suit == card_object.suit and
            self.state_ready and card_object.state_ready
            )

        # Comparing values:
        if eval_available:
            if self.type_value < card_object.type_value:
                eval_result: bool = True

        # Returning:
        return eval_result
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CLASS STATIC METHODS BLOCK
    
    """


    @staticmethod
    def create_card_object(init_type: str, 
                           init_suit: str, 
                           texture_pack_front: Optional[Texture_Pack] = None,
                           texture_pack_back: Optional[Texture_Pack] = None,
                           ) -> Card_Object:
        """
        TODO: Create a docstring.
        """

        # Creating card object:
        card_object: Card_Object = Card_Object()

        # Setting core attributes:
        card_object.set_type(
            set_value = init_type
            )
        card_object.set_suit(
            set_value = init_suit
            )
        
        # Selecting texture packs:
        texture_pack_front_selected: Texture_Pack = TEXTURE_PACK_FRONT_LIGHT_DEFAULT
        if texture_pack_front is not None:
            texture_pack_front_selected: Texture_Pack = texture_pack_front
        texture_pack_back_selected: Texture_Pack = TEXTURE_PACK_BACK_LIGHT_DEFAULT
        if texture_pack_back is not None:
            texture_pack_back_selected: Texture_Pack = texture_pack_back

        # Setting texture packs accordingly:
        card_object.set_texture_pack_front(
            texture_pack = texture_pack_front_selected
            )
        card_object.set_texture_pack_back(
            texture_pack = texture_pack_back_selected
            )
        
        # Returning:
        return card_object


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def __cached_suit_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "suit",
            "suit_repr",
            "suit_color",
            "suit_color_repr",
            "suit_ascii",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_type_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "type_f",
            "type_repr",
            "type_value_default",
            "type_value",
            "type_ascii",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_state_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "state_ready",
            "state_selected",
            "state_hovered",
            "state_trump",
            "state_revealed",
            "state_playable",
            "state_arrived",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_position_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "position_hand",
            "position_added",
            "position_deck",
            "position_discard",
            "position_table",
            "position_index",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_location_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "location",
            "location_repr"
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_texture_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "texture_front_object",
            "texture_back_object",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_coordinates_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "coordinate_x_current",
            "coordinate_y_current",
            "coordinate_x_default",
            "coordinate_y_default",
            "coordinate_x_slide",
            "coordinate_y_slide",
            )
        
        # Returning:
        return cached_property_list


    @cached_property
    def __cached_render_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "render_texture_object",
            "render_scale_value",
            "render_angle_value",
            "render_width_value",
            "render_height_value",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_boundary_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "boundary_x_left",
            "boundary_x_right",
            "boundary_x_range",
            "boundary_y_bottom",
            "boundary_y_top",
            "boundary_y_range"
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_boundary_x_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "boundary_x_left",
            "boundary_x_right",
            "boundary_x_range",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_boundary_y_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "boundary_y_bottom",
            "boundary_y_top",
            "boundary_y_range"
            )
        
        # Returning:
        return cached_property_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CARD SUIT METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def suit(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__suit
    

    @cached_property
    def suit_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Formatting:
        suit_repr: str = convert_attribute_to_repr(
            attribute_value = self.suit,
            attribute_tag = CARD_SUIT_TAG 
            )

        # Returning:
        return suit_repr
    

    @cached_property
    def suit_color(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Acquiring default value:
        suit_color: str = Card_Object.CARD_SUIT_COLOR_INDEX[self.suit]

        # Returning:
        return suit_color
    

    @cached_property
    def suit_color_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Formatting:
        suit_color_repr: str = convert_attribute_to_repr(
            attribute_value = self.suit_color,
            attribute_tag = CARD_SUIT_COLOR_TAG
            )
        
        # Returning:
        return suit_color_repr
    

    @cached_property
    def suit_ascii(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Aquiring ASCII symbol:
        suit_ascii: str = Card_Object.CARD_SUIT_ASCII_INDEX[self.suit]

        # Returning:
        return suit_ascii


    def set_suit(self, set_value: str, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param str set_value: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (str, )
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value is default:
            default_value_list: tuple[Any, ...] = Card_Object.CARD_SUIT_LIST
            assert_value_is_default(
                check_value = set_value,
                check_list = default_value_list,
                raise_error = True,
                )

        # Updating attribute:
        if self.suit != set_value:
            self.__suit: str = set_value

            # Clearing cache (suit):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_suit_property_list
                )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CARD TYPE METHODS AND PROPERTIES BLOCK
    
    """

    
    @cached_property
    def type_f(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__type
    

    @cached_property
    def type_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Formatting:
        type_repr: str = convert_attribute_to_repr(
            attribute_value = self.type_f,
            attribute_tag = CARD_TYPE_TAG 
            )

        # Returning:
        return type_repr
    

    @cached_property
    def type_value_default(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Acquiring default value:
        type_value_default: int = Card_Object.CARD_TYPE_VALUE_INDEX[self.type_f]

        # Returning:
        return type_value_default
    

    @cached_property
    def type_value(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating value:
        type_value: int = self.type_value_default
        if self.state_trump:
            type_value: int = type_value + Card_Object.CARD_TRUMP_VALUE_MODIFIER

        # Returning:
        return type_value
    

    @cached_property
    def type_ascii(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Selecting first character based on numerical or literal type:
        if self.type_value_default <= 10:
            type_ascii: str = str(self.type_value_default)
        else:
            type_ascii: str = self.type_repr[0]

        # Returning:
        return type_ascii


    def set_type(self, set_value: str, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param str set_value: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (str, )
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value is default:
            default_value_list: tuple[Any, ...] = Card_Object.CARD_TYPE_LIST
            assert_value_is_default(
                check_value = set_value,
                check_list = default_value_list,
                raise_error = True,
                )

        # Updating attribute:
        if self.type_f != set_value:
            self.__type: str = set_value

            # Clearing cache (type):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_type_property_list
                )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    STATE METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def state_ready(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Checking attributes values:
        state_ready: bool = (
            self.type_f != CARD_TYPE_NOT_SET and
            self.suit != CARD_SUIT_NOT_SET
            )
        
        # Returning:
        return state_ready
    

    @cached_property
    def state_selected(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__state_selected
    

    @cached_property
    def state_hovered(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__state_hovered
    

    @cached_property
    def state_trump(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__state_trump
    

    @cached_property
    def state_revealed(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__state_revealed


    @cached_property
    def state_opponent(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__state_opponent
    

    @cached_property
    def state_playable(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__state_playable
    

    @cached_property
    def state_showcase(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__state_showcase
    

    @cached_property
    def state_moving(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Comparing current coordinates with the expected/default coordinates:
        state_moving: bool = bool(
            self.coordinate_x_current not in (
                self.coordinate_x_default,
                self.coordinate_x_slide
                ) or
            self.coordinate_y_current not in (
                self.coordinate_y_default,
                self.coordinate_y_slide
                )
            )
        
        # Returning:
        return state_moving
    

    @cached_property
    def state_arrived(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__state_arrived
    

    def set_state_selected(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param bool set_value: ...
        :param bool ignore_assertion: ...

        :raise AssertionError:
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (bool, )
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )

        # Updating attribute:
        if self.state_selected != set_value:
            self.__state_selected: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_selected"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
            # Clearing cache (render):
            cached_property: str = "render_angle_value"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    

    def set_state_hovered(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param bool set_value: ...
        :param bool ignore_assertion: ...

        :raise AssertionError:
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (bool, )
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )

        # Updating attribute:
        if self.state_hovered != set_value:
            self.__state_hovered: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_hovered"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
            # Clearing cache (boundary):
            if self.location in (CARD_LOCATION_HAND, CARD_LOCATION_TABLE):

                # Clearing cache:
                clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = self.__cached_boundary_property_list
                    )
    

    def set_state_trump(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param bool set_value: ...
        :param bool ignore_assertion: ...

        :raise AssertionError:
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (bool, )
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )

        # Updating attribute:
        if self.state_trump != set_value:
            self.__state_trump: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_trump"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    

    def set_state_revealed(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param bool set_value: ...
        :param bool ignore_assertion: ...

        :raise AssertionError:
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (bool, )
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )

        # Updating attribute:
        if self.state_revealed != set_value:
            self.__state_revealed: bool = set_value

            # Clearing cache (render, texture):
            cached_property_collection: tuple[tuple, ...] = (
                self.__cached_render_property_list,
                self.__cached_texture_property_list,
                )
            for cached_property_list in cached_property_collection:
                clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = cached_property_list
                    )
            
            # Clearing cache (property)
            cached_property: str = "state_revealed"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            

    def set_state_opponent(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param bool set_value: ...
        :param bool ignore_assertion: ...

        :raise AssertionError:
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (bool, )
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )

        # Updating attribute:
        if self.state_opponent != set_value:
            self.__state_opponent: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_opponent"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    

    def set_state_playable(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param bool set_value: ...
        :param bool ignore_assertion: ...

        :raise AssertionError:
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (bool, )
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )

        # Updating attribute:
        if self.state_playable != set_value:
            self.__state_playable: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_playable"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_state_showcase(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param bool set_value: ...
        :param bool ignore_assertion: ...

        :raise AssertionError:
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (bool, )
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )

        # Updating attribute:
        if self.state_showcase != set_value:
            self.__state_showcase: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_showcase"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_state_arrived(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param bool set_value: ...
        :param bool ignore_assertion: ...

        :raise AssertionError:
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (bool, )
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )

        # Updating attribute:
        if self.state_arrived != set_value:
            self.__state_arrived: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_arrived"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
        
    
    def reset_state(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Resetting attributes:
        self.__state_selected: bool = False
        self.__state_hovered:  bool = False
        self.__state_trump:    bool = False
        self.__state_revealed: bool = False
        self.__state_opponent: bool = False
        self.__state_playable: bool = False
        self.__state_showcase: bool = False
        self.__state_arrived:  bool = False

        # Clearing cache (state):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_state_property_list,
            )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    POSITION METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def position_hand(self) -> int | None:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__position_hand
    

    @cached_property
    def position_added(self) -> int | None:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__position_added
    

    @cached_property
    def position_deck(self) -> int | None:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__position_deck
    

    @cached_property
    def position_discard(self) -> int | None:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__position_discard
    

    @cached_property
    def position_table(self) -> int | None:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__position_table
    

    @cached_property
    def position_index(self) -> int | None:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__position_index
    

    def set_position_hand(self, position_index: int, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param int | float position_index: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        :raise ValueError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (int, float)
            assert_value_is_valid_type(
                check_value = position_index,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value in valid range:
            default_range: range = range(0, DECK_SIZE_MAX)
            assert_value_in_valid_range(
                check_value = position_index,
                check_range = default_range,
                raise_error = True
                )
        
        # Attempting to convert:
        convert_required: bool = isinstance(position_index, float)
        position_index_f: float | int = position_index
        if convert_required:
            position_index_f: int = convert_value_to_integer(
                convert_value = position_index
                )

        # Updating attribute:
        if self.position_hand != position_index_f:
            self.__position_hand: int = position_index_f

            # Updating related attributes:
            self.__position_deck:    int | None = None
            self.__position_discard: int | None = None
            self.__position_table:   int | None = None
            self.__position_index:   int | None = None

            # Clearing cache (position):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_position_property_list,
                )
            
            # Clearing cache (location):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_location_property_list,
                )
            

    def set_position_added(self, position_index: int, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param int | float position_index: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        :raise ValueError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (int, float)
            assert_value_is_valid_type(
                check_value = position_index,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value in valid range:
            default_range: range = range(0, DECK_SIZE_MAX)
            assert_value_in_valid_range(
                check_value = position_index,
                check_range = default_range,
                raise_error = True
                )
        
        # Attempting to convert:
        convert_required: bool = isinstance(position_index, float)
        position_index_f: float | int = position_index
        if convert_required:
            position_index_f: int = convert_value_to_integer(
                convert_value = position_index
                )

        # Updating attribute:
        if self.position_added != position_index_f:
            self.__position_added: int = position_index_f

            # Updating related attributes:
            self.__position_deck:    int | None = None
            self.__position_discard: int | None = None
            self.__position_table:   int | None = None
            self.__position_index:   int | None = None

            # Clearing cache (position):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_position_property_list,
                )
            
            # Clearing cache (location):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_location_property_list,
                )
    

    def set_position_deck(self, position_index: int, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param int | float position_index: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        :raise ValueError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (int, float)
            assert_value_is_valid_type(
                check_value = position_index,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value is positive:
            assert_value_is_positive(
                check_value = position_index,
                raise_error = True,
                )

        # Attempting to convert:
        convert_required: bool = isinstance(position_index, float)
        position_index_f: float | int = position_index
        if convert_required:
            position_index_f: int = convert_value_to_integer(
                convert_value = position_index
                )

        # Updating attribute:
        if self.position_deck != position_index_f:
            self.__position_deck: int = position_index_f

            # Updating related attributes:
            self.__position_hand:    int | None = None
            self.__position_added:   int | None = None
            self.__position_discard: int | None = None
            self.__position_table:   int | None = None
            self.__position_index:   int | None = None

            # Clearing cache (position):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_position_property_list,
                )
            
            # Clearing cache (location):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_location_property_list,
                )
    

    def set_position_discard(self, position_index: int, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param int | float position_index: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        :raise ValueError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (int, float)
            assert_value_is_valid_type(
                check_value = position_index,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value in valid range:
            default_range: range = range(0, DECK_SIZE_MAX)
            assert_value_in_valid_range(
                check_value = position_index,
                check_range = default_range,
                raise_error = True
                )
        
        # Attempting to convert:
        convert_required: bool = isinstance(position_index, float)
        position_index_f: float | int = position_index
        if convert_required:
            position_index_f: int = convert_value_to_integer(
                convert_value = position_index
                )

        # Updating attribute:
        if self.position_discard != position_index_f:
            self.__position_discard: int = position_index_f

            # Updating related attributes:
            self.__position_hand:    int | None = None
            self.__position_added:   int | None = None
            self.__position_deck:    int | None = None
            self.__position_table:   int | None = None
            self.__position_index:   int | None = None

            # Clearing cache (position):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_position_property_list,
                )
            
            # Clearing cache (location):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_location_property_list,
                )
        

    def set_position_table(self, 
                           position_index: int,                 # <- 0 (left) to 5 (right)
                           stack_index: int,                    # <- 0 (bottom) to 1 (top)
                           ignore_assertion: bool = False       # <- True if debugging
                           ) -> None:
        """
        TODO: Create a docstring.

        :param int | float position_index: ...
        :param int | float stack_index: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        :raise ValueError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid (position):
            default_type_list: tuple[type, ...] = (int, float)
            assert_value_is_valid_type(
                check_value = position_index,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value in valid range (position):
            default_range: range = TABLE_POSITION_RANGE
            assert_value_in_valid_range(
                check_value = position_index,
                check_range = default_range,
                raise_error = True
                )
            
            # Asserting value type is valid (stack):
            default_type_list: tuple[type, ...] = (int, float)
            assert_value_is_valid_type(
                check_value = stack_index,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value in valid range (stack):
            default_range: range = TABLE_STACK_RANGE
            assert_value_in_valid_range(
                check_value = stack_index,
                check_range = default_range,
                raise_error = True
                )
        
        # Attempting to convert (position index):
        convert_required: bool = isinstance(position_index, float)
        position_index_f: float | int = position_index
        if convert_required:
            position_index_f: int = convert_value_to_integer(
                convert_value = position_index
                )
        
        # Attempting to convert (stack index):
        convert_required: bool = isinstance(stack_index, float)
        stack_index_f: float | int = stack_index
        if convert_required:
            stack_index_f: int = convert_value_to_integer(
                convert_value = stack_index
                )
        

        # Updating attributes:
        if self.position_table != position_index_f and self.position_index != stack_index_f:
            self.__position_table: int = position_index_f
            self.__position_index: int = stack_index_f

            # Updating related attributes:
            self.__position_hand:    int | None = None
            self.__position_added:   int | None = None
            self.__position_deck:    int | None = None
            self.__position_discard: int | None = None

            # Clearing cache (position):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_position_property_list,
                )
            
            # Clearing cache (location):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_location_property_list,
                )


    def reset_position(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Resetting positions to None:
        self.__position_hand:    int | None = None
        self.__position_added:   int | None = None
        self.__position_deck:    int | None = None
        self.__position_discard: int | None = None
        self.__position_table:   int | None = None
        self.__position_index:   int | None = None

        # Clearing cache:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_position_property_list,
            )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    LOCATION PROPERTIES BLOCK
    
    """


    @cached_property
    def location(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Generating card position to location index:
        card_location_index: dict[str, int | None] = {
            CARD_LOCATION_DECK:    self.position_deck,
            CARD_LOCATION_DISCARD: self.position_discard,
            CARD_LOCATION_HAND:    self.position_hand,
            CARD_LOCATION_TABLE:   self.position_table
            }
        
        # Locating card location based on position value:
        card_location_selected: str = CARD_LOCATION_NOT_SET
        for card_location, position_index in card_location_index.items():
            if position_index is not None:
                card_location_selected: str = card_location
                break
        
        # Returning:
        return card_location_selected


    @cached_property
    def location_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Formatting:
        location_repr: str = convert_attribute_to_repr(
            attribute_value = self.location,
            attribute_tag = CARD_LOCATION_TAG
            )

        # Returning:
        return location_repr
    
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    TEXTURE METHODS AND PROPERTIES BLOCK
    
    """


    @property
    def texture_pack_front(self) -> Texture_Pack:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__texture_pack_front
    

    @property
    def texture_pack_back(self) -> Texture_Pack:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__texture_pack_back
    

    @property
    def texture_front_filename(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Generating filename:
        texture_front_filename: str = "{card_suit}_{card_type}.png".format(
            card_suit = self.suit_repr.lower(),
            card_type = str(
                self.type_repr.lower() if self.type_value_default > 10 else
                str(self.type_value_default)
                ),
            )

        # Returning:
        return texture_front_filename
    

    @property
    def texture_front_filepath(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Connecting texture pack folder with textures folder:
        dir_texture_pack_color_name: str = "{texture_pack_color}_{texture_pack_index}".format(
            texture_pack_color = self.__texture_pack_front.pack_color.lower(),
            texture_pack_index = str(self.__texture_pack_front.pack_index),
            )
        dir_texture_pack_style: str = self.__texture_pack_front.pack_style.lower()
        dir_texture_pack_path: str = os.path.join(
            DIR_TEXTURES_CARD_FRONT_PATH,
            dir_texture_pack_style,
            dir_texture_pack_color_name,
            )
        
        # Generating texture front filepath:
        texture_front_filename: str = self.texture_front_filename
        texture_front_filepath: str = os.path.join(
            dir_texture_pack_path,
            texture_front_filename,
            )
            
        # Returning:
        return texture_front_filepath
    

    @cached_property
    def texture_front_object(self) -> Texture:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__texture_front_object
    

    @property
    def texture_back_filename(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Generating filename:
        texture_back_filename: str = "{pack_style}.png".format(
            pack_style = self.texture_pack_back.pack_style.lower()
            )

        # Returning:
        return texture_back_filename
    

    @property
    def texture_back_filepath(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Connecting texture pack folder with textures folder:
        dir_texture_pack_color_name: str = self.__texture_pack_back.pack_color.lower()
        dir_texture_pack_path: str = os.path.join(
            DIR_TEXTURES_CARD_BACK_PATH,
            dir_texture_pack_color_name
            )
        
        # Generating texture back filepath:
        texture_back_filename: str = self.texture_back_filename
        texture_back_filepath: str = os.path.join(
            dir_texture_pack_path,
            texture_back_filename,
            )
            
        # Returning:
        return texture_back_filepath
    

    @cached_property
    def texture_back_object(self) -> Texture:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__texture_back_object
    

    def set_texture_pack_front(self, texture_pack: Texture_Pack, clear_cache: bool = True) -> None:
        """
        TODO: Create a docstring.

        :param Texture_Pack texture_pack: ...
        :param bool clear_cache: ...

        :raise AssertionError: ...
        """

        # Assertion control:
        if SESSION_ENABLE_ASSERTION:

            # Asserting value is valid type (texture pack):
            default_type: object = Texture_Pack
            assert_value_is_valid_type(
                check_value = texture_pack,
                check_type = default_type,
                raise_error = True,
                )
            
            # Asserting value is valid type (flag):
            default_type: type = bool
            assert_value_is_valid_type(
                check_value = clear_cache,
                check_type = default_type,
                raise_error = True,
                )

        # Updating texture:
        self.__texture_pack_front: Texture_Pack = texture_pack
        
        # Loading texture object:
        texture_object: Texture = arcade.load_texture(
            file_path = self.texture_front_filepath
            )
        
        # Updating attribute:
        self.__texture_front_object: Texture = texture_object

        # Clearing cache (texture):
        if clear_cache:
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_texture_property_list,
                )
            
    
    def set_texture_pack_back(self, texture_pack: Texture_Pack, clear_cache: bool = True) -> None:
        """
        TODO: Create a docstring.

        :param Texture_Pack texture_pack: ...
        :param bool clear_cache: ...

        :raise AssertionError: ...
        """

        # Assertion control:
        if SESSION_ENABLE_ASSERTION:

            # Asserting value is valid type (texture pack):
            default_type: object = Texture_Pack
            assert_value_is_valid_type(
                check_value = texture_pack,
                check_type = default_type,
                raise_error = True,
                )
            
            # Asserting value is valid type (flag):
            default_type: type = bool
            assert_value_is_valid_type(
                check_value = clear_cache,
                check_type = default_type,
                raise_error = True,
                )

        # Updating texture:
        self.__texture_pack_back: Texture_Pack = texture_pack

        # Loading texture object:
        texture_object: Texture = arcade.load_texture(
            file_path = self.texture_back_filepath
            )
        
        # Updating attribute:
        self.__texture_back_object: Texture = texture_object

        # Clearing cache (texture):
        if clear_cache:
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_texture_property_list,
                )
            
    
    def update_texture(self, 
                       texture_pack_front: Texture_Pack, 
                       texture_pack_back: Texture_Pack,
                       ) -> None:
        """
        TODO: Create a docstring.

        :param Texture_Pack texture_pack_front:
        :param Texture_Pack texture_pack_back:
        """

        # Updating texture packs:
        self.set_texture_pack_front(
            texture_pack = texture_pack_front,
            clear_cache = False,
            )
        self.set_texture_pack_back(
            texture_pack = texture_pack_back,
            clear_cache = False,
            )
        
        # Clearing cache (texture):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_texture_property_list,
            )
        
        # Clearing cache (render):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_render_property_list
            )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    COORDINATES METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def coordinate_x_current(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__coordinate_x_current
    

    @cached_property
    def coordinate_y_current(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__coordinate_y_current
    

    @cached_property
    def coordinate_x_default(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__coordinate_x_default
    

    @cached_property
    def coordinate_y_default(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__coordinate_y_default
    

    @cached_property
    def coordinate_x_slide(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__coordinate_x_slide
    

    @cached_property
    def coordinate_y_slide(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__coordinate_y_slide
    

    def set_coordinate_x_current(self, 
                                 set_value: int, 
                                 clear_cache: bool = True, 
                                 ignore_assertion: bool = False
                                 ) -> None:
        """
        TODO: Create a docstring.

        :param int | float set_value: ...
        :param bool clear_cache: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        :raise ValueError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (int, float)
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value is positive:
            assert_value_is_positive(
                check_value = set_value,
                raise_error = True,
                )
        
        # Attempting to convert:
        convert_required: bool = isinstance(set_value, float)
        set_value_f: float | int = set_value
        if convert_required:
            set_value_f: int = convert_value_to_integer(
                convert_value = set_value
                )

        # Updating attribute:
        if self.coordinate_x_current != set_value_f:
            self.__coordinate_x_current: int = set_value_f

            # Clearing cache:
            if clear_cache:

                # Clearing cache (property)
                cached_property: str = "coordinate_x_current"
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )
                
                # Clearing cache (boundary x):
                clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = self.__cached_boundary_x_property_list
                    )


    def set_coordinate_y_current(self, 
                                 set_value: int, 
                                 clear_cache: bool = True, 
                                 ignore_assertion: bool = False
                                 ) -> None:
        """
        TODO: Create a docstring.

        :param int | float set_value: ...
        :param bool clear_cache: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        :raise ValueError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (int, float)
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value is positive:
            assert_value_is_positive(
                check_value = set_value,
                raise_error = True,
                )
        
        # Attempting to convert:
        convert_required: bool = isinstance(set_value, float)
        set_value_f: float | int = set_value
        if convert_required:
            set_value_f: int = convert_value_to_integer(
                convert_value = set_value
                )

        # Updating attribute:
        if self.coordinate_y_current != set_value_f:
            self.__coordinate_y_current: int = set_value_f

            # Clearing cache:
            if clear_cache:

                # Clearing cache (property)
                cached_property: str = "coordinate_x_current"
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )
                
                # Clearing cache (boundary y):
                clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = self.__cached_boundary_y_property_list
                    )
    

    def set_coordinate_x_default(self, 
                                 set_value: int, 
                                 clear_cache: bool = True, 
                                 ignore_assertion: bool = False
                                 ) -> None:
        """
        TODO: Create a docstring.

        :param int | float set_value: ...
        :param bool clear_cache: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        :raise ValueError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (int, float)
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value is positive:
            assert_value_is_positive(
                check_value = set_value,
                raise_error = True,
                )
        
        # Attempting to convert:
        convert_required: bool = isinstance(set_value, float)
        set_value_f: float | int = set_value
        if convert_required:
            set_value_f: int = convert_value_to_integer(
                convert_value = set_value
                )

        # Updating attribute:
        if self.coordinate_x_default != set_value_f:
            self.__coordinate_x_default: int = set_value_f

            # Clearing cache:
            if clear_cache:
                
                # Clearing cache (property)
                cached_property: str = "coordinate_x_default"
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )
    

    def set_coordinate_y_default(self, 
                                 set_value: int, 
                                 clear_cache: bool = True, 
                                 ignore_assertion: bool = False
                                 ) -> None:
        """
        TODO: Create a docstring.

        :param int | float set_value: ...
        :param bool clear_cache: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        :raise ValueError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (int, float)
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value is positive:
            assert_value_is_positive(
                check_value = set_value,
                raise_error = True,
                )
        
        # Attempting to convert:
        convert_required: bool = isinstance(set_value, float)
        set_value_f: float | int = set_value
        if convert_required:
            set_value_f: int = convert_value_to_integer(
                convert_value = set_value
                )

        # Updating attribute:
        if self.coordinate_y_default != set_value_f:
            self.__coordinate_y_default: int = set_value_f

            # Clearing cache:
            if clear_cache:
                
                # Clearing cache (coordinate property)
                cached_property: str = "coordinate_y_default"
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )
                
                # Clearing cache (boundary property)
                cached_property: str = "boundary_y_bottom"
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )
    

    def set_coordinate_x_slide(self, 
                               set_value: int, 
                               clear_cache: bool = True, 
                               ignore_assertion: bool = False
                               ) -> None:
        """
        TODO: Create a docstring.

        :param int | float set_value: ...
        :param bool clear_cache: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        :raise ValueError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (int, float)
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value is positive:
            assert_value_is_positive(
                check_value = set_value,
                raise_error = True,
                )
        
        # Attempting to convert:
        convert_required: bool = isinstance(set_value, float)
        set_value_f: float | int = set_value
        if convert_required:
            set_value_f: int = convert_value_to_integer(
                convert_value = set_value
                )

        # Updating attribute:
        if self.coordinate_x_slide != set_value_f:
            self.__coordinate_x_slide: int = set_value_f

            # Clearing cache:
            if clear_cache:
                cached_property: str = "coordinate_x_slide"
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )
    

    def set_coordinate_y_slide(self, 
                               set_value: int, 
                               clear_cache: bool = True, 
                               ignore_assertion: bool = False
                               ) -> None:
        """
        TODO: Create a docstring.

        :param int | float set_value: ...
        :param bool clear_cache: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        :raise ValueError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (int, float)
            assert_value_is_valid_type(
                check_value = set_value,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value is positive:
            assert_value_is_positive(
                check_value = set_value,
                raise_error = True,
                )
        
        # Attempting to convert:
        convert_required: bool = isinstance(set_value, float)
        set_value_f: float | int = set_value
        if convert_required:
            set_value_f: int = convert_value_to_integer(
                convert_value = set_value
                )

        # Updating attribute:
        if self.coordinate_y_slide != set_value_f:
            self.__coordinate_y_slide: int = set_value_f

            # Clearing cache:
            if clear_cache:
                cached_property: str = "coordinate_y_slide"
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )
                
    
    def set_coordinates_current(self, 
                                set_container: tuple[int, int], 
                                ignore_assertion: bool = False
                                ) -> None:
        """
        TODO: Create a docstring.

        :param tuple[int, int] set_container: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (tuple[int, int], list[int, int])
            assert_value_is_valid_type(
                check_value = set_container,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value (container) is valid size:
            default_size: int = 2
            assert_container_is_valid_size(
                check_container = set_container,
                check_size = default_size,
                raise_error = True
                )

        # Unpacking:
        set_coordinate_x, set_coordinate_y = set_container
        
        # Updating attributes:
        attribute_updated: bool = False
        if self.coordinate_x_current != set_coordinate_x:
            attribute_updated: bool = True
            self.set_coordinate_x_current(
                set_value = set_coordinate_x,
                clear_cache = False,
                ignore_assertion = ignore_assertion
                )
        if self.coordinate_y_current != set_coordinate_y:
            attribute_updated: bool = True
            self.set_coordinate_y_current(
                set_value = set_coordinate_y,
                clear_cache = False,
                ignore_assertion = ignore_assertion
                )

        # Post-update block:        
        if attribute_updated:

            # Clearing cache (property):
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_current",
                "coordinate_y_current",
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
            # Clearing cache (boundary):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_boundary_property_list
                )
            
            # Checking if the card arrived:
            if not self.state_arrived:
                card_arrived: bool = bool(
                    self.coordinate_x_current == self.coordinate_x_default and
                    self.coordinate_y_current == self.coordinate_y_default
                    )
                if card_arrived:
                    self.set_state_arrived(
                        set_value = True,
                        ignore_assertion = True,
                        )

    
    def set_coordinates_default(self, 
                                set_container: tuple[int, int], 
                                ignore_assertion: bool = False
                                ) -> None:
        """
        TODO: Create a docstring.

        :param tuple[int, int] set_container: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (tuple[int, int], list[int, int])
            assert_value_is_valid_type(
                check_value = set_container,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value (container) is valid size:
            default_size: int = 2
            assert_container_is_valid_size(
                check_container = set_container,
                check_size = default_size,
                raise_error = True
                )

        # Unpacking:
        set_coordinate_x, set_coordinate_y = set_container
        
        # Updating attributes:
        attribute_updated: bool = False
        if self.coordinate_x_default != set_coordinate_x:
            attribute_updated: bool = True
            self.set_coordinate_x_default(
                set_value = set_coordinate_x,
                clear_cache = False,
                ignore_assertion = ignore_assertion
                )
        if self.coordinate_y_default != set_coordinate_y:
            attribute_updated: bool = True
            self.set_coordinate_y_default(
                set_value = set_coordinate_y,
                clear_cache = False,
                ignore_assertion = ignore_assertion
                )
        
        # Clearing cache (property):
        if attribute_updated:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_default",
                "coordinate_y_default",
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
            # Updating state arrived:
            self.set_state_arrived(
                set_value = False,
                ignore_assertion = True,
                )


    def set_coordinates_slide(self, 
                              set_container: tuple[int, int], 
                              ignore_assertion: bool = False
                              ) -> None:
        """
        TODO: Create a docstring.

        :param tuple[int, int] set_container: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        """

        # Assertion control (if enabled):
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value type is valid:
            default_type_list: tuple[type, ...] = (tuple, )
            assert_value_is_valid_type(
                check_value = set_container,
                check_type = default_type_list,
                raise_error = True
                )
            
            # Asserting value (container) is valid size:
            default_size: int = 2
            assert_container_is_valid_size(
                check_container = set_container,
                check_size = default_size,
                raise_error = True
                )

        # Unpacking:
        set_coordinate_x, set_coordinate_y = set_container
        
        # Updating attributes:
        attribute_updated: bool = False
        if self.coordinate_x_slide != set_coordinate_x:
            attribute_updated: bool = True
            self.set_coordinate_x_slide(
                set_value = set_coordinate_x,
                clear_cache = False,
                ignore_assertion = ignore_assertion
                )
        if self.coordinate_y_slide != set_coordinate_y:
            attribute_updated: bool = True
            self.set_coordinate_y_slide(
                set_value = set_coordinate_y,
                clear_cache = False,
                ignore_assertion = ignore_assertion
                )
        
        # Clearing cache (property):
        if attribute_updated:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_slide",
                "coordinate_y_slide",
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    BOUNDARY METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def boundary_x_left(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating boundary coordinate (showcase):
        if self.state_showcase:
            boundary_coordinate: int = int(
                self.coordinate_x_current -
                self.render_height_value / 2
                )

        # Calculating boundary coordinate (default):
        else:
            boundary_coordinate: int = int(
                self.coordinate_x_current -
                self.render_width_value / 2
                )
            
        # Returning:
        return boundary_coordinate
    

    @cached_property
    def boundary_x_right(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating boundary coordinate (showcase):
        if self.state_showcase:
            boundary_coordinate: int = int(
                self.coordinate_x_current +
                self.render_height_value / 2
                )

        # Calculating boundary coordinate (default):
        else:
            boundary_coordinate: int = int(
                self.coordinate_x_current +
                self.render_width_value / 2
                )
        
        # Returning:
        return boundary_coordinate
    

    @cached_property
    def boundary_y_bottom(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating boundary coordinate (showcase):
        if self.state_showcase:
            boundary_coordinate: int = int(
                self.coordinate_y_current - 
                self.render_width_value / 2
                )

        # Calculating boundary coordinate (default):
        else:

            # Generating player's boundary:
            if self.coordinate_y_default < ZONE_TABLE_COORDINATE_Y:
                coordinate_y_center: int = self.coordinate_y_current
                if self.location == CARD_LOCATION_HAND and self.state_hovered:
                    coordinate_y_center: int = self.coordinate_y_default

            # Generating opponent's boundary:
            else:
                coordinate_y_center: int = self.coordinate_y_current
                if self.location == CARD_LOCATION_HAND and self.state_hovered:
                    coordinate_y_center: int = self.coordinate_y_slide

            # Calculating boundary coordinate:
            boundary_coordinate: int = int(
                coordinate_y_center - 
                self.render_height_value / 2
                )
        
        # Returning:
        return boundary_coordinate
    

    @cached_property
    def boundary_y_top(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating boundary coordinate (showcase):
        if self.state_showcase:
            boundary_coordinate: int = int(
                self.coordinate_y_current +
                self.render_width_value / 2
                )

        # Calculating boundary coordinate (default):
        else:

            # Generating player's boundary:
            if self.coordinate_y_default < ZONE_TABLE_COORDINATE_Y:
                coordinate_y_center: int = self.coordinate_y_current
                if self.location == CARD_LOCATION_HAND and self.state_hovered:
                    coordinate_y_center: int = self.coordinate_y_slide
            
            # Generating opponent's boundary:
            else:
                coordinate_y_center: int = self.coordinate_y_current
                if self.location == CARD_LOCATION_HAND and self.state_hovered:
                    coordinate_y_center: int = self.coordinate_y_default

            # Calculating boundary coordinate:
            boundary_coordinate: int = int(
                coordinate_y_center +
                self.render_height_value / 2
                )
        
        # Returning:
        return boundary_coordinate
    

    @cached_property
    def boundary_x_range(self) -> range:
        """
        TODO: Create a docstring.
        """

        # Generating range:
        boundary_range: range = range(
            self.boundary_x_left,
            self.boundary_x_right
            )
        
        # Returning:
        return boundary_range
    

    @cached_property
    def boundary_y_range(self) -> range:
        """
        TODO: Create a docstring.
        """

        # Generating range:
        boundary_range: range = range(
            self.boundary_y_bottom,
            self.boundary_y_top
            )
        
        # Returning:
        return boundary_range
    

    def reset_boundary(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Clearing cache (boundary):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_boundary_property_list
            )
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    RENDER METHODS AND PROPERTIES BLOCK
    
    """
    

    @cached_property
    def render_texture_object(self) -> Texture:
        """
        TODO: Create a docstring.
        """

        # Default (not revealed) texture:
        texture_object: Texture = self.texture_back_object

        # Checking if front texture is forced:
        force_front: bool = bool(
            self.location == CARD_LOCATION_HAND and self.state_revealed or
            self.location == CARD_LOCATION_DECK and self.state_showcase or
            self.location == CARD_LOCATION_DISCARD
            )
        if force_front:
            texture_object: Texture = self.texture_front_object

        # Returning:
        return texture_object
    

    @cached_property
    def render_scale_value(self) -> float:
        """
        TODO: Create a docstring.
        """

        render_scale_required: bool = bool(
            self.location == CARD_LOCATION_HAND and self.state_selected
            )
        
        # Choosing correct scale value:
        render_scale_selected: int = CARD_RENDER_SCALE_DEFAULT_MOD
        if render_scale_required:
            render_scale_selected: int = CARD_RENDER_SCALE_DEFAULT_MOD
            
        # Returning:
        return render_scale_selected
    

    @property
    def render_angle_value_random(self) -> int:
        """
        TODO: Create a docstring.
        """
        
        # Calculating a random angle:
        render_angle_value: int = random.randrange(
            start = CARD_RENDER_ANGLE_MIN,
            stop = CARD_RENDER_ANGLE_MAX
            )
        render_angle_axis: int = random.choice(
            seq = CARD_RENDER_ANGLE_AXIS_LIST
            )
        render_angle_random: int = render_angle_value * render_angle_axis    

        # Returning:
        return render_angle_random


    @cached_property
    def render_angle_value(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Choosing default angle:
        render_angle_selected: int = CARD_RENDER_ANGLE_DEFAULT

        # Checking angle based on location (table) and stack position:
        if self.location == CARD_LOCATION_TABLE:
            if self.position_index == TABLE_STACK_TOP_INDEX:
                render_angle_selected: int = self.render_angle_value_random
        
        # Checking angle based on location (hand) and state:
        elif self.location == CARD_LOCATION_HAND:
            if self.state_opponent:
                if self.state_revealed:
                    render_angle_selected: int = CARD_RENDER_ANGLE_OPPONENT
            else:
                if self.state_selected:
                    render_angle_selected: int = self.render_angle_value_random
        
        # Checking angle based on location (deck) and state:
        elif self.location == CARD_LOCATION_DECK:
            if self.state_showcase:
                render_angle_selected: int = DECK_RENDER_ANGLE_SHOWCASE
            else:
                render_angle_selected: int = CARD_RENDER_ANGLE_DEFAULT

        # Returning:
        return render_angle_selected


    @cached_property
    def render_width_value(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        render_width_value: int = int(CARD_TEXTURE_WIDTH_SCALED * self.render_scale_value)
    
        # Returning:
        return render_width_value
    

    @cached_property
    def render_height_value(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        render_height_value: int = int(CARD_TEXTURE_HEIGHT_SCALED * self.render_scale_value)
    
        # Returning:
        return render_height_value


    @property
    def render_rect_object(self) -> Rect:
        """
        TODO: Create a docstring.
        """

        # Creating render rectangle object:
        render_rect: Rect = arcade.XYWH(
            x = self.coordinate_x_current,
            y = self.coordinate_y_current,
            width = self.render_width_value,
            height = self.render_height_value
            )
        
        # Returning:
        return render_rect
        
    
    def render(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Rendering:
        arcade.draw_texture_rect(
            texture = self.render_texture_object,
            rect = self.render_rect_object,
            angle = self.render_angle_value,
            pixelated = True,
            )
        

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    SLIDE METHODS AND PROPERTIES BLOCK
    
    """


    def __calculate_coordinate_next(self, 
                                    slide_speed: int, 
                                    current_coordinate: int, 
                                    target_coordinate: int
                                    ) -> int:
        """
        TODO: Create a docstring.

        :param int slide_speed: ...
        :param int current_coordinate: ...
        :param int target_coordinate: ...
        """

        # Finding coordinate x slide axis:
        slide_axis: int = -1
        if current_coordinate < target_coordinate:
            slide_axis: int = +1

        # Calculating coordinate:
        coordinate_next: int = int(current_coordinate + slide_speed * slide_axis)
        coordinate_forced: bool = bool(
            (coordinate_next > target_coordinate and slide_axis == + 1) or
            (coordinate_next < target_coordinate and slide_axis == - 1)
            )
        
        # Forcing next coordinate to be target if it overlaps:
        if coordinate_forced:
            coordinate_next: int = target_coordinate

        # Returning:
        return coordinate_next


    def __slide_to_coordinates(self, 
                               target_coordinates: tuple[int, int], 
                               speed_modifier: Optional[float] = None,
                               force_instant: bool = False
                               ) -> None:
        """
        TODO: Create a docstring.

        :param tuple[int, int] target_coordinates: ...
        :param Optional[float] speed_modifier: ...
        :param bool force_instant: ...
        """

        # Looping over target coordinates:
        set_coordinates: list[int] = []
        for target_coordinate in target_coordinates:

            # Forcing next coordinate to be target coordinate:
            if force_instant:
                coordinate_next: int = target_coordinate

            # Calculating next coordinate x to slide to
            else:

                # Selecting speed modifier and calculating speed:
                slide_speed_modifier: float = CARD_SLIDE_SPEED_DEFAULT
                if speed_modifier is not None:
                    slide_speed_modifier: float = speed_modifier
                slide_speed: int = int(
                    CARD_SLIDE_SPEED_DEFAULT * 
                    CARD_SLIDE_SPEED_THROTTLE * 
                    slide_speed_modifier
                    )

                # Getting coordinate current:
                coordinates_current: int = (self.coordinate_x_current, self.coordinate_y_current)
                coordinate_index: int = target_coordinates.index(target_coordinate)
                coordinate_current: int = coordinates_current[coordinate_index]

                # Getting next coordinate:
                coordinate_next: int = self.__calculate_coordinate_next(
                    slide_speed = slide_speed,
                    current_coordinate = coordinate_current,
                    target_coordinate = target_coordinate,
                    )
                
                # Adding coordinate to the list:
                set_coordinates.append(
                    coordinate_next
                    )
        
        # Converting and updating coordinates:
        set_coordinates_conv: tuple[int, ...] = tuple(set_coordinates)
        self.set_coordinates_current(
            set_container = set_coordinates_conv,
            ignore_assertion = True,
            )


    def __slide_to_default(self, speed_modifier: Optional[float], force_instant: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param Optional[float] speed_modifier: ...
        :param bool force_instant: ...
        """

        # Preparing coordinates container:
        coordinates_default: tuple[int, int] = (
            self.coordinate_x_default,
            self.coordinate_y_default
            )
        
        # Calling slide method:
        self.__slide_to_coordinates(
            target_coordinates = coordinates_default,
            speed_modifier = speed_modifier,
            force_instant = force_instant,
            )
        
    
    def __slide_to_expected(self, speed_modifier: Optional[float], force_instant: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param Optional[float] speed_modifier: ...
        :param bool force_instant: ...
        """

        # Preparing coordinates container:
        coordinates_expected: tuple[int, int] = (
            self.coordinate_x_slide,
            self.coordinate_y_slide
            )
        
        # Calling slide method:
        self.__slide_to_coordinates(
            target_coordinates = coordinates_expected,
            speed_modifier = speed_modifier,
            force_instant = force_instant,
            )
        
    
    def slide(self, force_instant: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param bool force_instant: ...
        """

        # First slide logic:
        if not self.state_arrived:
            self.__slide_to_default(
                speed_modifier = CARD_SLIDE_SPEED_MODIFIER_FAST,
                force_instant = force_instant,
                )
        
        # Default logic:
        else:

            # Sliding card in place:
            if self.state_hovered:
                self.__slide_to_expected(
                    speed_modifier = CARD_SLIDE_SPEED_MODIFIER_DEFAULT,
                    force_instant = force_instant
                    )
            else:
                self.__slide_to_default(
                    speed_modifier = CARD_SLIDE_SPEED_MODIFIER_SLOW,
                    force_instant = force_instant,
                    )

