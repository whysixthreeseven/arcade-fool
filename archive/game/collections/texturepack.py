# Typing and annotations import:
from __future__ import annotations
from typing import Literal, Optional, Any
from enum import Enum

# Random library import:
import random

# Dataclass import:
from dataclasses import dataclass

# Cache module:
from functools import cached_property

# Arcade import:
from arcade import Texture
import arcade

# Texture pack variables:
from game.variables import (

    # Texture pack type variables:
    TEXTURE_PACK_TYPE_TAG,
    TEXTURE_PACK_TYPE_FRONT,
    TEXTURE_PACK_TYPE_BACK,

    # Texture pack mode variables:
    TEXTURE_PACK_MODE_TAG,
    TEXTURE_PACK_MODE_LIGHT,
    TEXTURE_PACK_MODE_DARK,

    # Texture pack (front) variables:
    TEXTURE_PACK_FRONT_STYLE_LIGHT,
    TEXTURE_PACK_FRONT_STYLE_DARK,
    TEXTURE_PACK_FRONT_STYLE_SEPIA,
    TEXTURE_PACK_FRONT_COLOR_MONO,
    TEXTURE_PACK_FRONT_COLOR_DUO,
    TEXTURE_PACK_FRONT_COLOR_QUAD,

    # Texture pack (back) variables:
    TEXTURE_PACK_BACK_STYLE_PLAIN,
    TEXTURE_PACK_BACK_STYLE_SUN,
    TEXTURE_PACK_BACK_STYLE_MOUNTAINS,
    TEXTURE_PACK_BACK_STYLE_CROSS,
    TEXTURE_PACK_BACK_COLOR_NAVY,
    TEXTURE_PACK_BACK_COLOR_BLUE,
    TEXTURE_PACK_BACK_COLOR_GREEN,
    TEXTURE_PACK_BACK_COLOR_PURPLE,
    TEXTURE_PACK_BACK_COLOR_RED,
    TEXTURE_PACK_BACK_COLOR_WHITE,
    TEXTURE_PACK_BACK_COLOR_ORANGE,
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
TEXTURE PACK DATACLASSES BLOCK

"""


class Texture_Pack:

    # Texture pack (front) collection:
    TEXTURE_PACK_FRONT_COLLECTION: tuple[tuple[str, str, int], ...] = (

        # Texture style                  # Texture color                # Index
        (TEXTURE_PACK_FRONT_STYLE_DARK,  TEXTURE_PACK_FRONT_COLOR_DUO,  1       ),
        (TEXTURE_PACK_FRONT_STYLE_DARK,  TEXTURE_PACK_FRONT_COLOR_MONO, 1       ),

        (TEXTURE_PACK_FRONT_STYLE_LIGHT, TEXTURE_PACK_FRONT_COLOR_DUO,  1       ),
        (TEXTURE_PACK_FRONT_STYLE_LIGHT, TEXTURE_PACK_FRONT_COLOR_DUO,  2       ),
        (TEXTURE_PACK_FRONT_STYLE_LIGHT, TEXTURE_PACK_FRONT_COLOR_MONO, 1       ),
        (TEXTURE_PACK_FRONT_STYLE_LIGHT, TEXTURE_PACK_FRONT_COLOR_QUAD, 1       ),
        (TEXTURE_PACK_FRONT_STYLE_LIGHT, TEXTURE_PACK_FRONT_COLOR_QUAD, 2       ),
        (TEXTURE_PACK_FRONT_STYLE_LIGHT, TEXTURE_PACK_FRONT_COLOR_QUAD, 3       ),

        (TEXTURE_PACK_FRONT_STYLE_SEPIA, TEXTURE_PACK_FRONT_COLOR_DUO,  1       ),
        (TEXTURE_PACK_FRONT_STYLE_SEPIA, TEXTURE_PACK_FRONT_COLOR_MONO, 1       ),
        )

    # Texture pack (back) collection:
    TEXTURE_PACK_BACK_COLLECTION: tuple[tuple[str, str], ...] = (

        # Texture color                  # Texture style
        (TEXTURE_PACK_BACK_COLOR_BLUE,   TEXTURE_PACK_BACK_STYLE_MOUNTAINS),
        (TEXTURE_PACK_BACK_COLOR_BLUE,   TEXTURE_PACK_BACK_STYLE_CROSS    ),
        (TEXTURE_PACK_BACK_COLOR_BLUE,   TEXTURE_PACK_BACK_STYLE_PLAIN    ),
        (TEXTURE_PACK_BACK_COLOR_BLUE,   TEXTURE_PACK_BACK_STYLE_SUN      ),

        (TEXTURE_PACK_BACK_COLOR_GREEN,  TEXTURE_PACK_BACK_STYLE_MOUNTAINS),
        (TEXTURE_PACK_BACK_COLOR_GREEN,  TEXTURE_PACK_BACK_STYLE_CROSS    ),
        (TEXTURE_PACK_BACK_COLOR_GREEN,  TEXTURE_PACK_BACK_STYLE_PLAIN    ),
        (TEXTURE_PACK_BACK_COLOR_GREEN,  TEXTURE_PACK_BACK_STYLE_SUN      ),

        (TEXTURE_PACK_BACK_COLOR_NAVY,   TEXTURE_PACK_BACK_STYLE_MOUNTAINS),
        (TEXTURE_PACK_BACK_COLOR_NAVY,   TEXTURE_PACK_BACK_STYLE_CROSS    ),
        (TEXTURE_PACK_BACK_COLOR_NAVY,   TEXTURE_PACK_BACK_STYLE_PLAIN    ),
        (TEXTURE_PACK_BACK_COLOR_NAVY,   TEXTURE_PACK_BACK_STYLE_SUN      ),

        (TEXTURE_PACK_BACK_COLOR_ORANGE, TEXTURE_PACK_BACK_STYLE_MOUNTAINS),
        (TEXTURE_PACK_BACK_COLOR_ORANGE, TEXTURE_PACK_BACK_STYLE_CROSS    ),
        (TEXTURE_PACK_BACK_COLOR_ORANGE, TEXTURE_PACK_BACK_STYLE_PLAIN    ),
        (TEXTURE_PACK_BACK_COLOR_ORANGE, TEXTURE_PACK_BACK_STYLE_SUN      ),

        (TEXTURE_PACK_BACK_COLOR_PURPLE, TEXTURE_PACK_BACK_STYLE_MOUNTAINS),
        (TEXTURE_PACK_BACK_COLOR_PURPLE, TEXTURE_PACK_BACK_STYLE_CROSS    ),
        (TEXTURE_PACK_BACK_COLOR_PURPLE, TEXTURE_PACK_BACK_STYLE_PLAIN    ),
        (TEXTURE_PACK_BACK_COLOR_PURPLE, TEXTURE_PACK_BACK_STYLE_SUN      ),

        (TEXTURE_PACK_BACK_COLOR_RED,    TEXTURE_PACK_BACK_STYLE_MOUNTAINS),
        (TEXTURE_PACK_BACK_COLOR_RED,    TEXTURE_PACK_BACK_STYLE_CROSS    ),
        (TEXTURE_PACK_BACK_COLOR_RED,    TEXTURE_PACK_BACK_STYLE_PLAIN    ),
        (TEXTURE_PACK_BACK_COLOR_RED,    TEXTURE_PACK_BACK_STYLE_SUN      ),

        (TEXTURE_PACK_BACK_COLOR_WHITE,  TEXTURE_PACK_BACK_STYLE_MOUNTAINS),
        (TEXTURE_PACK_BACK_COLOR_WHITE,  TEXTURE_PACK_BACK_STYLE_CROSS    ),
        (TEXTURE_PACK_BACK_COLOR_WHITE,  TEXTURE_PACK_BACK_STYLE_PLAIN    ),
        (TEXTURE_PACK_BACK_COLOR_WHITE,  TEXTURE_PACK_BACK_STYLE_SUN      ),

        )
    
    # Default texture pack by mode (light or dark) index:
    TEXTURE_PACK_DEFAULT_INDEX: dict[str, dict[str, tuple[Any, ...]]] = {
        TEXTURE_PACK_MODE_LIGHT: {
            TEXTURE_PACK_TYPE_FRONT: (
                TEXTURE_PACK_FRONT_STYLE_LIGHT, 
                TEXTURE_PACK_FRONT_COLOR_DUO,  
                1
                ),
            TEXTURE_PACK_TYPE_BACK: (
                TEXTURE_PACK_BACK_COLOR_WHITE,
                TEXTURE_PACK_BACK_STYLE_PLAIN
                )
            },
        TEXTURE_PACK_MODE_DARK: {
            TEXTURE_PACK_TYPE_FRONT: (
                TEXTURE_PACK_FRONT_STYLE_DARK,
                TEXTURE_PACK_FRONT_COLOR_DUO,
                1
                ),
            TEXTURE_PACK_TYPE_BACK: (
                TEXTURE_PACK_BACK_COLOR_NAVY,
                TEXTURE_PACK_BACK_STYLE_PLAIN
                ),
            }
        }

    def __init__(self, init_style: str, init_color: str, init_index: Optional[int] = None):

        # Core attributes:
        self.pack_style: str = init_style
        self.pack_color: str = init_color
        self.pack_index: int | None = init_index      # <- None, if back texture pack;


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PACK CACHED PROPERTIES BLOCK

    """


    @cached_property
    def pack_num(self) -> int:
        """
        TODO: Create a docstring:
        """
        
        # Preparing return variable:
        pack_num: None | int = None

        # Searching for front pack position number:
        if self.pack_index is not None:
            pack_collection_front: tuple = Texture_Pack.TEXTURE_PACK_FRONT_COLLECTION
            for pack_position, pack_collection in enumerate(pack_collection_front):
                pack_found: bool = bool(
                    self.pack_color in pack_collection and
                    self.pack_style in pack_collection and
                    self.pack_index in pack_collection
                    )
                if pack_found:
                    pack_num: int = pack_position
                    break
        
        # Searching for back pack position:
        else:
            pack_collection_back: tuple = Texture_Pack.TEXTURE_PACK_BACK_COLLECTION
            for pack_position, pack_collection in enumerate(pack_collection_back):
                pack_found: bool = bool(
                    self.pack_color in pack_collection and
                    self.pack_style in pack_collection
                    )
                if pack_found:
                    pack_num: int = pack_position
                    break
        
        # Returning:
        return pack_num
    

    @cached_property
    def pack_type(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Selecting correct pack type variable:
        if self.pack_index is not None:
            pack_type: str = TEXTURE_PACK_TYPE_FRONT
        else:
            pack_type: str = TEXTURE_PACK_TYPE_BACK

        # Returning:
        return pack_type


    @cached_property
    def pack_type_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Formatted value:
        pack_type_repr: str = convert_attribute_to_repr(
            attribute_value = self.pack_type,
            attribute_tag = TEXTURE_PACK_TYPE_TAG
            )
        
        # Returning:
        return pack_type_repr
    

    @property
    def pack_container(self) -> tuple:
        """
        TODO: Create a docstring.
        """

        # Generating pack:
        if self.pack_type == TEXTURE_PACK_TYPE_FRONT:
            pack_container: tuple[str, str, int] = (
                self.pack_style,
                self.pack_color,
                self.pack_index
                )
        else:
            pack_container: tuple[str, str] = (
                self.pack_color,
                self.pack_style
                )
            
        # Returning:
        return pack_container
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PACK SET METHODS BLOCK

    """
    

    def set_pack(self, 
                 pack_container: tuple, 
                 pack_type: Optional[str] = None, 
                 clear_cache: bool = True
                 ) -> None:
        """
        TODO: Create a doctring.
        """

        # Getting pack type:
        pack_type_selected: str | None = pack_type
        if pack_type_selected is None:
            pack_type_selected: str = self.pack_type

        # Unpacking texture pack front:
        if pack_type_selected == TEXTURE_PACK_TYPE_FRONT:
            pack_style, pack_color, pack_index = pack_container
            self.pack_style: str = pack_style
            self.pack_color: str = pack_color
            self.pack_index: str = pack_index

        # Unpacking texture pack back:
        elif pack_type_selected == TEXTURE_PACK_TYPE_BACK:
            pack_color, pack_style = pack_container
            self.pack_style: str = pack_style
            self.pack_color: str = pack_color

        # Raising error, if pack type is not recognized:
        else:
            error_message: str = f"Texture pack type {pack_type_selected=} is not recognized."
            raise ValueError(error_message)
        
        # Clearing cache (property):
        if clear_cache:
            cached_property: str = "pack_num"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_pack_default(self, pack_mode: str) -> None:
        """
        TODO: Create a docstring.
        """

        # Aquiring correct texture pack
        pack_index: dict[str, dict[str, tuple[Any, ...]]] = Texture_Pack.TEXTURE_PACK_DEFAULT_INDEX
        pack_container: tuple[Any, ...] = pack_index[pack_mode][self.pack_type]

        # Setting a new pack:
        self.set_pack(
            pack_type = self.pack_type,
            pack_container = pack_container,
            clear_cache = True
            )


    def set_pack_random(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Selecting a random pack based on current type:
        if self.pack_type == TEXTURE_PACK_TYPE_FRONT:
            pack_random: tuple[str, str, int] = random.choice(
                Texture_Pack.TEXTURE_PACK_FRONT_COLLECTION
                )
        else:
            pack_random: tuple[str, str, int] = random.choice(
                Texture_Pack.TEXTURE_PACK_BACK_COLLECTION
                )

        # Setting a new pack:
        self.set_pack(
            pack_type = self.pack_type,
            pack_container = pack_random,
            clear_cache = True
            )
        
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PACK SWITCH METHODS BLOCK

    """


    def __switch_pack(self, switch_axis: int = 1) -> None:

        # Aquiring texture pack:
        if self.pack_type == TEXTURE_PACK_TYPE_FRONT:
            pack_collection = Texture_Pack.TEXTURE_PACK_FRONT_COLLECTION
        else:
            pack_collection = Texture_Pack.TEXTURE_PACK_BACK_COLLECTION

        # Checking indexes:
        pack_num_max: int = len(pack_collection)
        pack_num_current: int = self.pack_num
        pack_num_switch: int = pack_num_current + switch_axis

        # Getting back to zero if switch index overflows max size:
        if pack_num_switch >= pack_num_max:
            pack_num_switch: int = 0

        # Selecting pack:
        pack_switch: Texture_Pack = pack_collection[pack_num_switch]

        # Setting new pack:
        self.set_pack(
            pack_type = self.pack_type,
            pack_container = pack_switch,
            clear_cache = True
            )


    def switch_pack_next(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Switching packs:
        self.__switch_pack(
            switch_axis = 1
            )
        
    
    def switch_pack_previous(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Switching packs:
        self.__switch_pack(
            switch_axis = 1
            )
        

"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DEFAULT TEXTURE PACK COLLECTIONS BLOCK

"""


TEXTURE_PACK_FRONT_LIGHT_DEFAULT = Texture_Pack(
    init_style = TEXTURE_PACK_FRONT_STYLE_LIGHT,
    init_color = TEXTURE_PACK_FRONT_COLOR_DUO,
    init_index = 1,
    )


TEXTURE_PACK_FRONT_DARK_DEFAULT = Texture_Pack(
    init_style = TEXTURE_PACK_FRONT_STYLE_DARK,
    init_color = TEXTURE_PACK_FRONT_COLOR_DUO,
    init_index = 1,
    )


TEXTURE_PACK_BACK_LIGHT_DEFAULT = Texture_Pack(
    init_style = TEXTURE_PACK_BACK_STYLE_PLAIN,
    init_color = TEXTURE_PACK_BACK_COLOR_WHITE,
    )


TEXTURE_PACK_BACK_DARK_DEFAULT = Texture_Pack(
    init_style = TEXTURE_PACK_BACK_STYLE_PLAIN,
    init_color = TEXTURE_PACK_BACK_COLOR_NAVY,
    )

