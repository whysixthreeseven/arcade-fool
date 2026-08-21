# Typing and annotations:
from __future__ import annotations
from typing import Any, Optional, Literal, LiteralString

# System management:
import os

# Arcade library:
import arcade
from arcade import Rect, Text, Texture, XYWH

# Cache management:
from functools import cached_property
from game.utilities.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list
    )

# Settings and session instances:
from game.settings import SETTINGS
from game.session import SESSION

# Card-related variables:
from game.context import (
    CARD_NAME, 
    CARD_NAME_ASCII, 
    CARD_SUIT, 
    CARD_SUIT_ASCII, 
    CARD_COLOR, 
    CARD_VALUE
    )

# Assertion scripts:
from game.utilities.scripts.assertion import (
    assert_value_type,
    assert_value_default,
    )


class Card:
    
    def __init__(self) -> None:
        
        # Core attributes:
        self.__name: str = None
        self.__suit: str = None
        self.__trump: bool = None
        
        # Texture attributes:
        self.__texture_front_pack: TexturePack = None
        self.__texture_front_object: Texture = None
        self.__texture_back_pack: TexturePack = None
        self.__texture_back_object: Texture = None
        
        # Render attributes:
        self.__render_scale: float = 1.00
        self.__render_alpha: int = 255
        self.__render_tilt: int = 0
        
        
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
    

    def clear_cached_core_attributes(self) -> None:

        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_core_attributes
            )
        
    
    def clear_cached_attributes(self) -> None:
        
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_core_attributes,
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
        TEXTURE PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def texture_front_pack(self) -> str:
        
        # Returning:
        return self.__texture_front_pack
    
    
    
    
    
    @cached_property
    def texture_front_filename(self) -> str:
        
        dir_card_name: str = "card"
        dir_front_name: str = "front"
        dir_card_path: str = os.path.join(
            SETTINGS.DIR_TEXTURES_PATH, 
            dir_card_name,
            dir_front_name
            )