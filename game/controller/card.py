# Typing and annotations:
from __future__ import annotations
from typing import Any, Optional, Literal, LiteralString

# System management:
import os

# Random library:
import random

# Arcade library:
import arcade
from arcade import Rect, Text, Texture, XYWH

# Texture packs:
from game.utilities.texturepack import TexturePack, TEXTURE_PACK_FRONT, TEXTURE_PACK_BACK

# Settings and session instances:
from game.settings import SETTINGS
from game.session import SESSION

# Cache management:
from functools import cached_property
from game.utilities.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list
    )

# Assertion scripts:
from game.utilities.scripts.assertion import (
    assert_value_type,
    assert_value_default,
    assert_value_ge_zero,
    assert_value_not_empty,
    assert_value_in_range,
    )

# Context and other card variables:
from game.context import (
    CARD_NAME, 
    CARD_NAME_ASCII, 
    CARD_SUIT, 
    CARD_SUIT_ASCII, 
    CARD_COLOR, 
    CARD_VALUE
    )


class Card:
    
    def __init__(self) -> None:
        
        # Core attributes:
        self.__name: str = None
        self.__suit: str = None
        self.__trump: bool = None
        
        # Texture attributes:
        self.__texture_pack_front: TexturePack = None
        self.__texture_object_front: Texture = None
        self.__texture_pack_back: TexturePack = None
        self.__texture_object_back: Texture = None
        
        # Render attributes:
        self.__render_scale: float = None
        self.__render_alpha: int = None
        self.__render_tilt: int = None
        
        # Coordinates attributes:
        self.__coordinate_x_current: int = None
        self.__coordinate_y_current: int = None
        self.__coordinate_x_position: int = None
        self.__coordinate_y_position: int = None
        self.__coordinate_x_hover: int = None
        self.__coordinate_y_hover: int = None
        self.__coordinate_x_expected: int = None
        self.__coordinate_y_expected: int = None
        
        # State attributes:
        self.__state_visible: bool = None
        self.__state_revealed: bool = None
        self.__state_hovered: bool = None
        self.__state_selected: bool = None
        self.__state_playable: bool = None
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_core_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "name",
            "name_ascii",
            "suit",
            "suit_ascii",
            "color",
            "value"
            "trump"
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_texture_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "texture_pack_front",
            "texture_pack_back",
            "texture_filepath_front",
            "texture_filepath_back",
            "texture_object_front",
            "texture_object_back"
            )

        # Returning:
        return cached_property_list


    @cached_property
    def __cached_render_attributes(self) -> tuple[str, ...]:

        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "render_scale",
            "render_alpha",
            "render_tilt"
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_coordinates_attributes(self) -> tuple[str, ...]:

        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            
            # Current coordinates:
            "coordinate_x",
            "coordinate_y",
            "coordinates"
            
            # Position coordinates:
            "coordinate_x_position",
            "coordinate_y_position",
            "coordinates_position",
            
            # Hover coordinates:
            "coordinate_x_hover",
            "coordinate_y_hover",
            "coordinates_hover",
            
            # Expected coordinates:
            "coordinate_x_expected",
            "coordinate_y_expected",
            "coordinates_expected"
            )
        
        # Returning:
        return cached_property_list


    @cached_property
    def __cached_state_attributes(self) -> tuple[str, ...]:

        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "state_visible",
            "state_revealed",
            "state_hovered",
            "state_selected",
            "state_playable"
            )
        
        # Returning:
        return cached_property_list
    

    def clear_cached_core_attributes(self) -> None:

        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_core_attributes
            )
    
    
    def clear_cached_texture_attributes(self) -> None:
    
        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_texture_attributes
            )
        
    
    def clear_cached_render_attributes(self) -> None:
    
        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_render_attributes
            )
        

    def clear_cached_coordinates_attributes(self) -> None:
        
            # Clearing cached properties:
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_coordinates_attributes
                )
    
    
    def clear_cached_state_attributes(self) -> None:
        
            # Clearing cached properties:
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_state_attributes
                )
        
    
    def clear_cached_attributes(self) -> None:
        
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_core_attributes,
            self.__cached_texture_attributes,
            self.__cached_render_attributes,
            self.__cached_coordinates_attributes
            )
        
        # Looping throught the list and clearing cache:
        for cached_property_list in cached_property_list_collection:
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARD CORE CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def name(self) -> str:
        
        # Returning:
        return self.__name
    
    
    @cached_property
    def name_ascii(self) -> str:
        
        # Generating a dictionary index:
        name_ascii_index = {
            attr_name.capitalize(): getattr(CARD_NAME_ASCII, attr_name)
            for attr_name, attr_value in CARD_NAME.__dict__.items()
            if not attr_name.startswith("_") and hasattr(CARD_NAME_ASCII, attr_name)
            }
        
        # Getting correct value:
        name_ascii: str = name_ascii_index.get(
            self.name,          # Cached property (None by default)
            None                # Default return, if name not set
            )
        
        # Returning:
        return name_ascii
    
    
    def __validate_name(self, validate_value: str) -> None:
        
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = str,
            raise_error = True
            )
        
        # Asserting value is not empty:
        assert_value_not_empty(
            check_value = validate_value,
            raise_error = True
            )
        
        # Asserting value is default:
        default_list: tuple[str, ...] = tuple(
            attribute_name for attribute_name, attribute_value
            in CARD_NAME.__dict__.items()
            if not attribute_name.startswith("_")
            )
        assert_value_default(
            check_value = validate_value,
            check_default = default_list,
            raise_error = True
            )
        
    
    def set_name(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_name(
                validate_value = set_value
                )
            
        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            ...     # TODO: Implmenet duplicate setter check!
            
        # Updating attribute:
        self.__name = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "name",
                "name_ascii",
                "value"
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
 
    
    @cached_property
    def suit(self) -> str:

        # Returning:
        return self.__suit
    

    @cached_property
    def suit_ascii(self) -> str:

        # Generating a dictionary index:
        suit_ascii_index = {
            attr_name.capitalize(): getattr(CARD_SUIT_ASCII, attr_name)
            for attr_name, attr_value in CARD_SUIT.__dict__.items()
            if not attr_name.startswith("_") and hasattr(CARD_SUIT_ASCII, attr_name)
            }
        
        # Getting correct value:
        suit_ascii: str = suit_ascii_index.get(
            self.suit,          # Cached property (None by default)
            None                # Default return, if name not set
            )
        
        # Returning:
        return suit_ascii
    
    
    def __validate_suit(self, validate_value: str) -> None:

        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = str,
            raise_error = True
            )
        
        # Asserting value is not empty:
        assert_value_not_empty(
            check_value = validate_value,
            raise_error = True
            )

        # Asserting value is default:
        default_list: tuple[str, ...] = tuple(
            attribute_name for attribute_name, attribute_value
            in CARD_SUIT.__dict__.items()
            if not attribute_name.startswith("_")
            )
        assert_value_default(
            check_value = validate_value,
            check_default = default_list,
            raise_error = True
            )
        
        
    def set_suit(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_suit(
                validate_value = set_value
                )

        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            ...     # TODO: Implmenet duplicate setter check!
            
        # Updating attribute:
        self.__suit = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "suit",
                "suit_ascii",
                "color",
                "trump"
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
        
        
    @cached_property
    def color(self) -> str:
        
        # Getting correct color:
        color_index: dict[str, str] = {
            CARD_SUIT.HEARTS:   CARD_COLOR.RED,
            CARD_SUIT.DIAMONDS: CARD_COLOR.RED,
            CARD_SUIT.CLUBS:    CARD_COLOR.BLACK,
            CARD_SUIT.SPADES:   CARD_COLOR.BLACK,
            }
        color: str = color_index.get(
            self.suit,      # Cached property (None by default)
            None            # Default return, if suit not set
            )

        # Returning:
        return color


    @cached_property
    def trump(self) -> bool:
        
        # Returning:
        return self.__trump
    
    
    def __validate_trump(self, validate_value: bool) -> None:
        
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = bool,
            raise_error = True
            )


    def set_trump(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_trump(
                validate_value = set_value
                )

        # Updating attribute:
        self.__trump = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "trump",
                "value"
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
    
    def switch_trump(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.__trump = not self.__trump
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "trump",
                "value"
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
    
    
    @cached_property
    def value(self) -> int:
        
        # Generating a dictionary index:
        value_index = {
            attr_name.capitalize(): getattr(CARD_VALUE, attr_name)
            for attr_name, attr_value in CARD_NAME.__dict__.items()
            if not attr_name.startswith("_") and hasattr(CARD_VALUE, attr_name)
            }
                
        # Getting correct value:
        value: str = value_index.get(
            self.name,      # Cached property (None by default)
            None            # Default return, if name not set
            )
                
        # Calculating value:
        if value is not None and self.trump:
            value += 100
        
        # Returning:
        return value
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COORDINATES CACHED PROPERTIES AND METHODS:
        
    """
    
    
    @cached_property
    def coordinate_x(self) -> int:
        
        # Returning:
        return self.__coordinate_x_current


    @cached_property
    def coordinate_y(self) -> int:

        # Returning:
        return self.__coordinate_y_current
    
    
    @cached_property
    def coordinates(self) -> tuple[int, int]:
        
        # Making container:
        coordinates: tuple[int, int] = (
            self.coordinate_x,
            self.coordinate_y
            )

        # Returning:
        return coordinates


    def __validate_coordinate(self, validate_value: int) -> None:

        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = int,
            raise_error = True
            )
        
        # Asserting value is not negative:
        assert_value_ge_zero(
            check_value = validate_value,
            raise_error = True
            )
        
        
    def set_coordinate_x(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_x_current = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x",
                "coordinates"
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
            
    def adjust_coordinate_x(self, adjust_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assert_value_type(
                check_value = adjust_value,
                check_type = int,
                raise_error = True
                )
            
        # Updating attribute:
        coordinate_x_adjusted: int = self.coordinate_x + adjust_value
        self.set_coordinate_x(
            set_value = coordinate_x_adjusted,
            ignore_assertion = ignore_assertion,
            clear_cache = clear_cache
            )


    def set_coordinate_y(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_y_current = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_y",
                "coordinates"
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
            
    def adjust_coordinate_y(self, adjust_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assert_value_type(
                check_value = adjust_value,
                check_type = int,
                raise_error = True
                )

        # Updating attribute:
        coordinate_y_adjusted: int = self.coordinate_y + adjust_value
        self.set_coordinate_y(
            set_value = coordinate_y_adjusted,
            ignore_assertion = ignore_assertion,
            clear_cache = clear_cache
            )
            
            
    def __validate_coordiante_container(self, validate_value: tuple[int, int]) -> None:
        
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = tuple,
            raise_error = True,
            )
        
        # Asserting container item count:
        assert_eval: bool = len(validate_value) == 2
        if not assert_eval:
            container_len: int = len(validate_value)
            error_message: str = f"Invalid container item count. Expected 2, got {container_len}."
            raise AssertionError(error_message)
        
        # Asserting each item:
        for container_item in validate_value:
            self.__validate_coordinate(
                validate_value = container_item
                )
            
    
    def set_coordinates(self, set_value: tuple[int, int], ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_coordiante_container(
                validate_value = set_value
                )
            
        # Unpacking coordinates:
        coordinate_x, coordinate_y = set_value
            
        # Updating attributes:
        self.set_coordinate_y(
            set_value = coordinate_x,
            ignore_assertion = True,
            clear_cache = False,
            )
        self.set_coordinate_y(
            set_value = coordinate_y,
            ignore_assertion = True,
            clear_cache = False,
            )
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x",
                "coordinate_y",
                "coordinates"
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
        

    @cached_property
    def coordinate_x_position(self) -> int:
        
        # Returning:
        return self.__coordinate_x_position
    
    
    @cached_property
    def coordinate_y_position(self) -> int:

        # Returning:
        return self.__coordinate_y_position
    
    
    @cached_property
    def coordinates_position(self) -> tuple[int, int]:
        
        # Packing container:
        coordinates_position: tuple[int, int] = (
            self.__coordinate_x_position,
            self.__coordinate_y_position
            )

        # Returning:
        return coordinates_position
    
    
    def set_coordinate_x_position(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_x_position = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_position",
                "coordinates_position"
                )
            clear_cached_property_list(
                target_oject = self,
                target_attribute = cached_property_list
                )
            
    
    def set_coordinate_y_position(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_y_position = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_y_position",
                "coordinates_position"
                )
            clear_cached_property_list(
                target_oject = self,
                target_attribute = cached_property_list
                )
        
        
    def set_coordinates_position(self, set_value: tuple[int, int], ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_coordiante_container(
                validate_value = set_value
                )

        # Unpacking coordinates:
        coordinate_x, coordinate_y = set_value

        # Updating attributes:
        self.set_coordinate_x_position(
            set_value = coordinate_x,
            ignore_assertion = True,
            clear_cache = False,
            )
        self.set_coordinate_y_position(
            set_value = coordinate_y,
            ignore_assertion = True,
            clear_cache = False,
            )

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_position",
                "coordinate_y_position",
                "coordinates_position"
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
    
    @cached_property
    def coordinate_x_expected(self) -> int:
        
        # Returning:
        return self.__coordinate_x_expected


    @cached_property
    def coordinate_y_expected(self) -> int:

        # Returning:
        return self.__coordinate_y_expected


    @cached_property
    def coordinates_expected(self) -> tuple[int, int]:

        # Packing container:
        coordinates_expected: tuple[int, int] = (
            self.__coordinate_x_expected,
            self.__coordinate_y_expected
            )

        # Returning:
        return coordinates_expected


    def set_coordinate_x_expected(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_coordinate(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__coordinate_x_expected = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_expected",
                "coordinates_expected"
                )
            clear_cached_property(
                target_oject = self,
                target_attribute = cached_property
                )
            
    
    def set_coordinate_y_expected(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_y_expected = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_y_expected",
                "coordinates_expected"
                )
            clear_cached_property(
                target_oject = self,
                target_attribute = cached_property
                )
            
    
    def set_coordinates_expected(self, set_value: tuple[int, int], ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_coordiante_container(
                validate_value = set_value
                )

        # Unpacking coordinates:
        coordinate_x, coordinate_y = set_value
        
        # Updating attributes:
        self.set_coordinate_x_expected(
            set_value = coordinate_x,
            ignore_assertion = True,
            clear_cache = False,
            )
        self.set_coordinate_y_expected(
            set_value = coordinate_y,
            ignore_assertion = True,
            clear_cache = False,
            )

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_expected",
                "coordinate_y_expected",
                "coordinates_expected"
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
    
    
    @cached_property
    def coordinate_x_hover(self) -> int:

        # Returning:
        return self.__coordinate_x_hover
    

    @cached_property
    def coordinate_y_hover(self) -> int:

        # Returning:
        return self.__coordinate_y_hover


    @cached_property
    def coordinates_hover(self) -> tuple[int, int]:

        # Packing container:
        coordinates_hover: tuple[int, int] = (
            self.__coordinate_x_hover,
            self.__coordinate_y_hover
            )

        # Returning:
        return coordinates_hover


    def set_coordinate_x_hover(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_x_hover = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_hover",
                "coordinates_hover"
                )
            clear_cached_property(
                target_oject = self,
                target_attribute = cached_property
                )
            
    
    def set_coordinate_y_hover(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_y_hover = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_y_hover",
                "coordinates_hover"
                )
            clear_cached_property(
                target_oject = self,
                target_attribute = cached_property
                )
            
    
    def set_coordinates_hover(self, set_value: tuple[int, int], ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_coordiante_container(
                validate_value = set_value
                )

        # Unpacking coordinates:
        coordinate_x, coordinate_y = set_value
        
        # Updating attributes:
        self.set_coordinate_x_hover(
            set_value = coordinate_x,
            ignore_assertion = True,
            clear_cache = False,
            )
        self.set_coordinate_y_hover(
            set_value = coordinate_y,
            ignore_assertion = True,
            clear_cache = False,
            )

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_hover",
                "coordinate_y_hover",
                "coordinates_hover"
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        TEXTURE CACHED PROPETIES AND METHODS
    
    """
    
    
    @cached_property
    def texture_pack_front(self) -> TexturePack:
        
        # Returning:
        return self.__texture_pack_front
    
    
    @cached_property
    def texture_pack_back(self) -> TexturePack:
        
        # Returning:
        return self.__texture_pack_back
    
    
    def __validate_texture_pack(self, validate_value: TexturePack) -> None:
        
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = TexturePack,
            raise_error = True
            )
        
        # Asserting value is default:
        texture_pack = validate_value
        if texture_pack.type == "Front":
            texture_pack_list: tuple[TexturePack, ...] = tuple(
                texture_pack_object for texture_pack_name, texture_pack_object 
                in TEXTURE_PACK_FRONT.__dict__.items()
                if isinstance(texture_pack_object, TexturePack)
                )
        else:
            texture_pack_list: tuple[TexturePack, ...] = tuple(
                texture_pack_object for texture_pack_name, texture_pack_object 
                in TEXTURE_PACK_BACK.__dict__.items()
                if isinstance(texture_pack_object, TexturePack)
                )
        assert_value_default(
            check_value = texture_pack,
            check_default_list = texture_pack_list,
            raise_error = True
            )
    
    
    def set_texture_pack_front(self, texture_pack_object: TexturePack, ignore_assertion: bool = False, 
                               update_texture: bool = True, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_texture_pack(
                validate_value = texture_pack_object
                )

        # Updating attribute:
        self.__texture_pack_front = texture_pack_object

        # Updating texture:
        if update_texture:
            self.load_texture_object_front(
                clear_cache = clear_cache
                )

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "texture_pack_front",
                "texture_filepath_front"
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
    
    def set_texture_pack_back(self, texture_pack_object: TexturePack, ignore_assertion: bool = False, 
                              update_texture: bool = True, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_texture_pack(
                validate_value = texture_pack_object
                )

        # Updating attribute:
        self.__texture_pack_back = texture_pack_object

        # Updating texture:
        if update_texture:
            self.load_texture_object_back(
                clear_cache = clear_cache
                )

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "texture_pack_back",
                "texture_filepath_back"
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
    
    
    @cached_property
    def texture_filepath_front(self) -> str:
        
        # Acquiring filename:
        texture_filepath: str = self.texture_pack_front.texture_index[self.suit].get(self.name, None)
        if texture_filepath is None:
            error_message: str = f"Texture filepath for card <{self.suit_ascii}{self.name_ascii}> not provided."
            raise FileNotFoundError(error_message)

        # Returning:
        return texture_filepath
    
    
    @cached_property
    def texture_filepath_back(self) -> str:

        # Acquiring filename:
        texture_filepath: str = self.texture_pack_back.texture_index[self.suit].get(self.name, None)
        if texture_filepath is None:
            error_message: str = f"Texture filepath for card <{self.suit_ascii}{self.name_ascii}> not provided."
            raise FileNotFoundError(error_message)

        # Returning:
        return texture_filepath
    
    
    @cached_property
    def texture_object_front(self) -> Texture:
        
        # Returning:
        return self.__texture_object_front
    
    
    @cached_property
    def texture_object_back(self) -> Texture:

        # Returning:
        return self.__texture_object_back
    
    
    @cached_property
    def texture_selected(self) -> Texture:
        
        # TODO: Create logic based on card's revealed state!
        return None
    
    
    def load_texture_object_front(self, clear_cache: bool = True) -> None:
        
        # Loading texture:
        texture: Texture = arcade.load_texture(
            file_path = self.texture_filepath_front
            )
        
        # Updating attribute:
        self.__texture_object_front = texture
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "texture_object_front"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def load_texture_object_back(self, clear_cache: bool = True) -> None:

        # Loading texture:
        texture: Texture = arcade.load_texture(
            file_path = self.texture_filepath_back
            )

        # Updating attribute:
        self.__texture_object_back = texture

        # Clearing cache:
        if clear_cache:
            cached_property: str = "texture_object_back"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        RENDER CACHED PROPERTIES AND METHODS:
    
    """
    
    
    @cached_property
    def render_scale(self) -> float:
        
        # Returning:
        return self.__render_scale
    
    
    @cached_property
    def render_scale_default(self) -> float:
        
        # Returning:
        return SETTINGS.CARD_RENDER_SCALE_DEFAULT
    
    
    @cached_property
    def render_scale_step_mod_default(self) -> float:
        
        # Returning:
        return SETTINGS.CARD_RENDER_SCALE_STEP_MOD_DEFAULT
    
    
    @cached_property
    def render_scale_selected(self) -> float:

        # Returning:
        return SETTINGS.CARD_RENDER_SCALE_SELECTED
    

    @cached_property
    def render_scale_step_mod_selected(self) -> float:

        # Returning:
        return SETTINGS.CARD_RENDER_SCALE_STEP_MOD_SELECTED
    
    
    def __validate_render_scale(self, validate_value: float) -> None:
        
        # Asserting value type:
        assert_value_type(
            check_value = validate_value,
            check_type = float,
            raise_error = True
            )
        
        # Asserting value is not negative:
        assert_value_ge_zero(
            check_value = validate_value,
            raise_error = True
            )
        
        
    def set_render_scale(self, set_value: float, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_render_scale(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__render_scale = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_scale"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_render_scale_default(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.set_render_scale(
            set_value = SETTINGS.CARD_RENDER_SCALE_DEFAULT,
            ignore_assertion = False,
            clear_cache = clear_cache,
            )
        
        
    def set_render_scale_selected(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.set_render_scale(
            set_value = SETTINGS.CARD_RENDER_SCALE_SELECTED,
            ignore_assertion = False,
            clear_cache = clear_cache,
            )
        
        
    def transition_render_scale(self, target_value: float, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_render_scale(
                validate_value = target_value
                )
            
        # Updating to selected state:
        if target_value == self.render_scale_selected:
            if self.render_scale != self.render_scale_step_mod_selected:
                step_amount: float = self.__render_scale * self.render_scale_step_mod_selected
                self.adjust_render_scale(
                    adjust_value = step_amount,
                    ignore_assertion = False,
                    clear_cache = False,
                    )
                if self.__render_scale > self.render_scale_selected:
                    self.__render_scale = self.render_scale_selected
                
        # Updating to default state:
        elif target_value == self.render_scale_default:
            if self.render_scale != self.render_scale_default:
                step_amount: float = self.__render_scale * self.render_scale_step_mod_default
                self.adjust_render_scale(
                    adjust_value = step_amount,
                    ignore_assertion = False,
                    clear_cache = False,
                    )
                if self.__render_scale < self.render_scale_default:
                    self.__render_scale = self.render_scale_default

        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_scale"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def adjust_render_scale(self, adjust_value: float, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_render_scale(
                validate_value = adjust_value
                )

        # Updating attribute:
        render_scale_adjusted: float = self.render_scale + adjust_value
        self.__render_scale = render_scale_adjusted

        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_scale"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    
    
    @cached_property
    def render_alpha(self) -> int:
        
        # Returning:
        return self.__render_alpha
    
    
    @cached_property
    def render_alpha_default(self) -> int:
        
        # Returning:
        return SETTINGS.CARD_RENDER_ALPHA_DEFAULT
    
    
    @cached_property
    def render_alpha_faded(self) -> int:

        # Returning:
        return SETTINGS.CARD_RENDER_ALPHA_FADED


    def __validate_render_alpha(self, validate_value: int) -> None:

        # Asserting value type:
        assert_value_type(
            check_value = validate_value,
            check_type = int,
            raise_error = True
            )
        
        # Asserting value is not negative:
        assert_value_ge_zero(
            check_value = validate_value,
            raise_error = True
            )


    def set_render_alpha(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_render_alpha(
                validate_value = set_value
                )

        # Updating attribute:
        self.__render_alpha = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_alpha"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )


    def set_render_alpha_default(self, clear_cache: bool = True) -> None:

        # Updating attribute:
        self.set_render_alpha(
            set_value = SETTINGS.CARD_RENDER_ALPHA_DEFAULT,
            ignore_assertion = True,
            clear_cache = clear_cache,
            )
        
    
    def set_render_alpha_faded(self, clear_cache: bool = True) -> None:

        # Updating attribute:
        self.set_render_alpha(
            set_value = SETTINGS.CARD_RENDER_ALPHA_FADED,
            ignore_assertion = True,
            clear_cache = clear_cache,
            )
        
    
    def transition_render_alpha(self, target_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_render_alpha(
                validate_value = target_value
                )

        # Updating to faded state:
        if target_value == self.render_alpha_faded:
            if self.render_alpha != self.render_alpha_step_mod_faded:
                step_amount: int = self.__render_alpha * self.render_alpha_step_mod_faded
                self.adjust_render_alpha(
                    adjust_value = step_amount,
                    ignore_assertion = False,
                    clear_cache = False,
                    )
                if self.__render_alpha < self.render_alpha_faded:
                    self.__render_alpha = self.render_alpha_faded

        # Updating to default state:
        elif target_value == self.render_alpha_default:
            if self.render_alpha != self.render_alpha_step_mod_default:
                step_amount: int = self.__render_alpha * self.render_alpha_step_mod_default
                self.adjust_render_alpha(
                    adjust_value = step_amount,
                    ignore_assertion = False,
                    clear_cache = False,
                    )
                if self.__render_alpha > self.render_alpha_default:
                    self.__render_alpha = self.render_alpha_default
                    
        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_alpha"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def adjust_render_alpha(self, adjust_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assert_value_type(
                check_value = adjust_value,
                check_type = int,
                raise_error = True
                )
        
        # Updating attribute:
        render_alpha_adjusted: int = self.render_alpha + adjust_value
        self.__render_alpha = render_alpha_adjusted
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_alpha"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )

    
    @cached_property
    def render_tilt(self) -> int:
        
        # Returning:
        return self.__render_tilt
    
    
    @cached_property
    def render_tilt_default(self) -> int:
        
        # Returning:
        return SETTINGS.CARD_RENDER_TILT_DEFAULT
    
    
    @cached_property
    def render_tilt_opp(self) -> int:

        # Returning:
        return SETTINGS.CARD_RENDER_TILT_OPP
    
    
    @cached_property
    def render_tilt_random(self) -> int:
        
        # Generating a new random tilt angle:
        tilt_axis: int = random.choice(SETTINGS.CARD_RENDER_TILT_AXIS_LIST)
        tilt_angle_selected: int = random.randint(SETTINGS.CARD_RENDER_TILT_MIN, SETTINGS.CARD_RENDER_TILT_MAX)
        tilt_angle_random: int = tilt_axis * tilt_angle_selected
        
        # Returning:
        return tilt_angle_random
    
    
    @cached_property
    def render_tilt_step_in(self) -> float:
        
        # Returning:
        return SETTINGS.CARD_RENDER_TILT_STEP_IN
    
    
    @cached_property
    def render_tilt_step_out(self) -> float:

        # Returning:
        return SETTINGS.CARD_RENDER_TILT_STEP_OUT
    
    
    def __validate_render_tilt(self, validate_value: int) -> None:
        
        # Asserting value type:
        assert_value_type(
            check_value = validate_value,
            check_type = int,
            raise_error = True
            )

        # Asserting value in range:
        assert_value_in_range(
            check_value = abs(validate_value),
            check_range = (
                SETTINGS.CARD_RENDER_TILT_MIN, 
                SETTINGS.CARD_RENDER_TILT_MAX +1
                ),
            raise_error = True
            )
    
    
    def set_render_tilt(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_render_tilt(
                validate_value = set_value,
                )
            
        # Updating attribute:
        self.__render_tilt = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_tilt"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            

    def set_render_tilt_default(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.set_render_tilt(
            set_value = self.render_tilt_default,
            ignore_assertion = True,
            clear_cache = clear_cache,
            )
        
    
    def set_render_tilt_random(self, clear_cache: bool = True) -> None:
        
        # Clearing previous use cache:
        cached_property: str = "render_tilt_random"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )

        # Updating attribute:
        self.set_render_tilt(
            set_value = self.render_tilt_random,
            ignore_assertion = True,
            clear_cache = clear_cache,
            )
        
        
    def transition_render_tilt(self, target_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_render_tilt(
                validate_value = target_value,
                )
        
        if target_value == self.render_tilt_default:
            step_amount: float = self.render_tilt_step_out
        else:
            step_amount: float = self.render_tilt_step_in
            
        # Calculating new value:
        adjust_value: int = abs(self.render_tilt - int(self.render_tilt * step_amount))
        if adjust_value == 0:
            adjust_value = 1
        if self.render_tilt > target_value:
            adjust_value = -adjust_value
        
        # Updating attribute:
        self.adjust_render_tilt(
            adjust_value = adjust_value,
            ignore_assertion = False,
            clear_cache = False,
            )
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_tilt"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
        
    
    def adjust_render_tilt(self, adjust_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assert_value_type(
                check_value = adjust_value,
                check_type = int,
                raise_error = True
                )

        # Updating attribute:
        render_tilt_adjusted: int = self.render_tilt + adjust_value
        self.__render_tilt = render_tilt_adjusted

        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_tilt"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )


    @cached_property
    def render_rect(self) -> Rect:
        
        # Creating a rectnagle object:
        rect_object: Rect = XYWH(
            x = self.coordinate_x,
            y = self.coordinate_y,
            w = self.render_width,
            h = self.render_height,
            )
        
        # Returning:
        return rect_object
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        STATE CACHED PROPERTIES AND METHODS:
        
    """
    
    
    @cached_property
    def state_visible(self) -> bool:
        
        # Returning:
        return self.__state_visible
    
    
    @cached_property
    def state_revealed(self) -> bool:
        
        # Returning:
        return self.__state_revealed
    
    
    @cached_property
    def state_hovered(self) -> bool:
        
        # Returning:
        return self.__state_hovered
    
    
    @cached_property
    def state_selected(self) -> bool:
        
        # Returning:
        return self.__state_selected


    def __validate_state(self, validate_value: bool) -> None:
        
        # Asserting value type:
        assert_value_type(
            check_value = validate_value,
            check_type = bool,
            raise_error = True
            )
        
    
    def set_state_visible(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_state(
                validate_value = set_value,
                )
            
        # Updating attribute:
        self.__state_visible = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_visible"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    
    
    def switch_state_visible(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.__state_visible = not self.__state_visible

        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_visible"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )


    def set_state_revealed(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_state(
                validate_value = set_value,
                )
            
        # Updating attribute:
        self.__state_revealed = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_revealed"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )


    def switch_state_revealed(self, clear_cache: bool = True) -> None:

        # Updating attribute:
        self.__state_revealed = not self.__state_revealed

        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_revealed"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_state_hovered(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_state(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__state_hovered = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_hovered"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            

    def switch_state_hovered(self, clear_cache: bool = True) -> None:

        # Updating attribute:
        self.__state_hovered = not self.__state_hovered

        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_hovered"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_state_selected(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_state(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__state_selected = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_selected"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def switch_state_selected(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.__state_selected = not self.__state_selected

        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_selected"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_state_playable(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_state(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__state_playable = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_playable"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    
    
    def switch_state_playable(self, clear_cache: bool = True) -> None:

        # Updating attribute:
        self.__state_playable = not self.__state_playable

        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_playable"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    
    