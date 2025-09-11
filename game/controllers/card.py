# Annotations, typing etc. import:
from __future__ import annotations
from typing import Any

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

# Card-related settings import:
from game.settings import (

    # Card render settings:
    CARD_RENDER_SCALE_DEFAULT_MOD,
    CARD_RENDER_ANGLE_DEFAULT,
    CARD_RENDER_ANGLE_OPPONENT,
    CARD_RENDER_ANGLE_MIN,
    CARD_RENDER_ANGLE_MAX,
    CARD_RENDER_ANGLE_AXIS_LIST,

    # Card texture settings:
    CARD_TEXTURE_WIDTH_SCALED,
    CARD_TEXTURE_HEIGHT_SCALED,

    # Stack position index:
    TABLE_STACK_TOP_INDEX,

    # Card render angle (in deck) settings:
    DECK_RENDER_ANGLE_SHOWCASE,
    DECK_RENDER_ANGLE_ADD_MIN,
    DECK_RENDER_ANGLE_ADD_MAX,

    )

# Collections import:
from game.collections.texturepack import (

    # Texture packs:
    Texture_Pack, 
    TEXTURE_PACK_FRONT_DEFAULT,
    TEXTURE_PACK_BACK_DEFAULT,
    )

# Scripts import:
from game.scripts.convert import (
    convert_attribute_to_repr
    )
from game.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list
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
        self.__texture_front_object: Texture      = None
        self.__texture_back_object:  Texture      = None

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
        echo_string: str = ""

        # Returning:
        return echo_string
    

    def __repr__(self):
        """
        TODO: Create a docstring.
        """

        # Generating new string value:
        echo_string: str = ""

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
    def create_card_object(init_type: str, init_suit: str) -> Card_Object:
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
        
        # Updating texture pack:
        card_object.set_texture_pack_front(
            texture_pack = TEXTURE_PACK_FRONT_DEFAULT,
            )
        card_object.set_texture_pack_back(
            texture_pack = TEXTURE_PACK_BACK_DEFAULT
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
            "type_value"
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
            "__texture_pack_front",
            "__texture_pack_back",
            "__texture_front_object",
            "__texture_back_object",
            "__texture_width",
            "__texture_height",
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
            "__render_texture_object",
            "__render_scale_value",
            "__render_angle_value",
            "__render_width_value",
            "__render_height_value",
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


    def set_suit(self, set_value: str) -> None:
        """
        TODO: Create a docstring.
        """

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


    def set_type(self, set_value: str) -> None:
        """
        TODO: Create a docstring.
        """

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
            self.type_f != CARD_TYPE_NOT_SET,
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
    

    def set_state_selected(self, set_value: bool) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.state_selected != set_value:
            self.__state_selected: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_selected"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    

    def set_state_hovered(self, set_value: bool) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.state_hovered != set_value:
            self.__state_hovered: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_hovered"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    

    def set_state_trump(self, set_value: bool) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.state_trump != set_value:
            self.__state_trump: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_trump"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    

    def set_state_revealed(self, set_value: bool) -> None:
        """
        TODO: Create a docstring.
        """

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
            

    def set_state_opponent(self, set_value: bool) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.state_opponent != set_value:
            self.__state_opponent: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_opponent"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    

    def set_state_playable(self, set_value: bool) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.state_playable != set_value:
            self.__state_playable: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_playable"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_state_showcase(self, set_value: bool) -> None:
        """
        TODO
        """

        # Updating attribute:
        if self.state_showcase != set_value:
            self.__state_showcase: bool = set_value

            # Clearing cache (property):
            cached_property: str = "state_showcase"
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
    

    def set_position_hand(self, position_index: int) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.position_hand != position_index:
            self.__position_hand: int = position_index

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
            

    def set_position_added(self, position_index: int) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.position_added != position_index:
            self.__position_added: int = position_index

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
    

    def set_position_deck(self, position_index: int) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.position_deck != position_index:
            self.__position_deck: int = position_index

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
    

    def set_position_discard(self, position_index: int) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.position_discard != position_index:
            self.__position_discard: int = position_index

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
        

    def set_position_table(self, position_index: int, stack_index: int) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attributes:
        if self.position_table != position_index and self.position_index != stack_index:
            self.__position_table: int = position_index
            self.__position_index: int = stack_index

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


    @cached_property
    def __texture_pack_front(self) -> Texture_Pack:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__texture_pack_front
    

    @cached_property
    def __texture_pack_back(self) -> Texture_Pack:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__texture_pack_back
    

    @cached_property
    def __texture_width(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Acquriing texture width:
        texture_width: int = self.__texture_front_object.width

        # Returning:
        return texture_width
    

    @cached_property
    def __texture_height(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Acquriing texture width:
        texture_height: int = self.__texture_front_object.height

        # Returning:
        return texture_height


    @property
    def __texture_front_filename(self) -> str:
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
    def __texture_front_filepath(self) -> str:
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
        texture_front_filename: str = self.__texture_front_filename
        texture_front_filepath: str = os.path.join(
            dir_texture_pack_path,
            texture_front_filename,
            )
            
        # Returning:
        return texture_front_filepath
    

    @cached_property
    def __texture_front_object(self) -> Texture:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__texture_front_object
    

    @property
    def __texture_back_filename(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Generating filename:
        texture_back_filename: str = "{pack_style}.png".format(
            pack_style = self.__texture_pack_back.pack_style.lower()
            )

        # Returning:
        return texture_back_filename
    

    @property
    def __texture_back_filepath(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Connecting texture pack folder with textures folder:
        dir_texture_pack_color_name: str = self.__texture_pack_back.pack_color
        dir_texture_pack_path: str = os.path.join(
            DIR_TEXTURES_CARD_BACK_PATH,
            dir_texture_pack_color_name
            )
        
        # Generating texture back filepath:
        texture_back_filename: str = self.__texture_back_filename
        texture_back_filepath: str = os.path.join(
            dir_texture_pack_path,
            texture_back_filename,
            )
            
        # Returning:
        return texture_back_filepath
    

    @cached_property
    def __texture_back_object(self) -> Texture:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__texture_back_object
    

    def __load_texture_front(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Loading texture object:
        texture_object: Texture = arcade.load_texture(
            file_path = self.__texture_front_filepath
            )
        
        # Updating attribute:
        self.__texture_front_object: Texture = texture_object


    def __load_texture_back(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Loading texture object:
        texture_object: Texture = arcade.load_texture(
            file_path = self.__texture_back_filepath
            )
        
        # Updating attribute:
        self.__texture_back_object: Texture = texture_object


    def set_texture_pack_front(self, texture_pack: Texture_Pack) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating texture:
        if self.__texture_pack_front != texture_pack:
            self.__texture_pack_front: Texture_Pack = texture_pack

            # Clearing cache (texture):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_texture_property_list,
                )
            
            # Updating texture objects:
            self.__load_texture_front()
            
    
    def set_texture_pack_back(self, texture_pack: Texture_Pack) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating texture:
        if self.__texture_pack_back != texture_pack:
            self.__texture_pack_back: Texture_Pack = texture_pack

            # Clearing cache (texture):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_texture_property_list,
                )
            
            # Updating texture objects:
            self.__load_texture_back()


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
        """

        # Updating attribute:
        if self.coordinate_x_current != set_value:
            self.__coordinate_x_current: int = set_value

            # Clearing cache:
            if clear_cache:
                cached_property: str = "coordinate_x_current"
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )
    

    def set_coordinate_y_current(self, 
                                 set_value: int, 
                                 clear_cache: bool = True, 
                                 ignore_assertion: bool = False
                                 ) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.coordinate_y_current != set_value:
            self.__coordinate_y_current: int = set_value

            # Clearing cache:
            if clear_cache:
                cached_property: str = "coordinate_y_current"
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )
    

    def set_coordinate_x_default(self, 
                                 set_value: int, 
                                 clear_cache: bool = True, 
                                 ignore_assertion: bool = False
                                 ) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.coordinate_x_default != set_value:
            self.__coordinate_x_default: int = set_value

            # Clearing cache:
            if clear_cache:
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
        """

        # Updating attribute:
        if self.coordinate_y_default != set_value:
            self.__coordinate_y_default: int = set_value

            # Clearing cache:
            if clear_cache:
                cached_property: str = "coordinate_y_default"
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
        """

        # Updating attribute:
        if self.coordinate_x_slide != set_value:
            self.__coordinate_x_slide: int = set_value

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
        """

        # Updating attribute:
        if self.coordinate_y_slide != set_value:
            self.__coordinate_y_slide: int = set_value

            # Clearing cache:
            if clear_cache:
                cached_property: str = "coordinate_y_slide"
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )
                
    
    def set_coordinates_current(self, 
                                set_value: tuple[int, int], 
                                ignore_assertion: bool = False
                                ) -> None:
        """
        TODO: Create a docstring.
        """

        # Unpacking:
        set_coordinate_x, set_coordinate_y = set_value
        
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
        
        # Clearing cache (property):
        if attribute_updated:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_current",
                "coordinate_y_current",
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )

    
    def set_coordinates_default(self, 
                                set_value: tuple[int, int], 
                                ignore_assertion: bool = False
                                ) -> None:
        """
        TODO: Create a docstring.
        """

        # Unpacking:
        set_coordinate_x, set_coordinate_y = set_value
        
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
            self.set_coordinate_x_default(
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


    def set_coordinates_slide(self, 
                              set_value: tuple[int, int], 
                              ignore_assertion: bool = False
                              ) -> None:
        """
        TODO: Create a docstring.
        """

        # Unpacking:
        set_coordinate_x, set_coordinate_y = set_value
        
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
            self.set_coordinate_x_slide(
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
    RENDER METHODS AND PROPERTIES BLOCK
    
    """
    

    @cached_property
    def __render_texture_object(self) -> Texture:
        """
        TODO: Create a docstring.
        """

        # Default (not revealed) texture:
        texture_object: Texture = self.__texture_back_object

        # Checking if front texture is forced:
        force_front: bool = bool(
            self.location == CARD_LOCATION_HAND and self.state_revealed or
            self.location == CARD_LOCATION_DISCARD or
            self.location == CARD_LOCATION_DECK and self.state_showcase
            )
        if force_front:
            texture_object: Texture = self.__texture_front_object

        # Returning:
        return texture_object
    

    @cached_property
    def __render_scale_value(self) -> float:
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
    def __render_angle_random(self) -> int:
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
    def __render_angle_value(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Choosing default angle:
        render_angle_selected: int = CARD_RENDER_ANGLE_DEFAULT

        # Checking angle based on location (table) and stack position:
        if self.location == CARD_LOCATION_TABLE:
            if self.position_index == TABLE_STACK_TOP_INDEX:
                render_angle_selected: int = self.__render_angle_random
        
        # Checking angle based on location (hand) and state:
        elif self.location == CARD_LOCATION_HAND:
            if self.state_opponent:
                if self.state_revealed:
                    render_angle_selected: int = 180    # TODO: Implement
            else:
                if self.state_selected:
                    render_angle_selected: int = self.__render_angle_random
        
        # Checking angle based on location (deck) and state:
        elif self.location == CARD_LOCATION_DECK:
            if self.state_showcase:
                render_angle_selected: int = DECK_RENDER_ANGLE_SHOWCASE
                # render_angle_add: int = random.randint(
                #     a = DECK_RENDER_ANGLE_ADD_MIN,
                #     b = DECK_RENDER_ANGLE_ADD_MAX,
                #     )
                # render_angle_axis: int = random.choice(CARD_RENDER_ANGLE_AXIS_LIST)
                # render_angle_selected: int = int(
                #     DECK_RENDER_ANGLE_SHOWCASE + 
                #     render_angle_add * render_angle_axis
                #     )

            # Flipping card over for opponent's hand:
            else:
                render_angle_selected: int = CARD_RENDER_ANGLE_OPPONENT

        # Returning:
        return render_angle_selected


    @cached_property
    def __render_width_value(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        render_width_value: int = int(CARD_TEXTURE_WIDTH_SCALED * self.__render_scale_value)
    
        # Returning:
        return render_width_value
    

    @cached_property
    def __render_height_value(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        render_height_value: int = int(CARD_TEXTURE_HEIGHT_SCALED * self.__render_scale_value)
    
        # Returning:
        return render_height_value


    @property
    def __render_rect_object(self) -> Rect:
        """
        TODO: Create a docstring.
        """

        # Creating render rectangle object:
        render_rect: Rect = arcade.XYWH(
            x      = self.coordinate_x_current,
            y      = self.coordinate_y_current,
            width  = self.__render_width_value,
            height = self.__render_height_value
            )
        
        # Returning:
        return render_rect
        
    
    def render(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Rendering:
        arcade.draw_texture_rect(
            texture   = self.__render_texture_object,
            rect      = self.__render_rect_object,
            angle     = self.__render_angle_value,
            pixelated = True,
            )
        
    