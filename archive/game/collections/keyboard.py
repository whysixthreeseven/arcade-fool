# Dataclass import:
from dataclasses import dataclass

# Cache tools:
from functools import cached_property

# Arcade library import:
import arcade


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
KEYBOARD MAPPING CLASS OBJECT BLOCK

"""


@dataclass
class Keyboard_Mapping:

    # DEBUG Game logic key mapping:
    KEY_DEBUG_DRAW_CARD_PLAYER:   int = arcade.key.KEY_1
    KEY_DEBUG_DRAW_CARD_OPPONENT: int = arcade.key.KEY_2
    KEY_DEBUG_RESTART_GAME:       int = arcade.key.R

    # DEBUG Texture pack key mapping:
    KEY_DEBUG_SWITCH_TEXTURE_PACK_FRONT:      int = arcade.key.T
    KEY_DEBUG_SWITCH_TEXTURE_PACK_BACK:       int = arcade.key.Y
    KEY_DEBUG_SET_TEXTURE_PACK_DEFAULT_LIGHT: int = arcade.key.U
    KEY_DEBUG_SET_TEXTURE_PACK_DEFAULT_DARK:  int = arcade.key.I

    # DEBUG Hand sorting key mapping:
    KEY_DEBUG_SORT_HAND_BY_VALUE:         int = arcade.key.Z
    KEY_DEBUG_SORT_HAND_BY_VALUE_DEFAULT: int = arcade.key.X
    KEY_DEBUG_SORT_HAND_BY_TIME_ADDED:    int = arcade.key.C
    KEY_DEBUG_SORT_HAND_BY_SUIT:          int = arcade.key.V

    # DEBUG Sweep key mapping：
    KEY_DEBUG_SWEEP_TO_HAND_PLAYER:   int = arcade.key.NUM_1
    KEY_DEBUG_SWEEP_TO_HAND_OPPONENT: int = arcade.key.NUM_2
    KEY_DEBUG_SWEEP_TO_DISCARD:       int = arcade.key.NUM_0

    # Action key mapping:
    KEY_BACK:        int = arcade.key.ESCAPE    # <- Escape to menu, back to previous menu, exit game
    KEY_CONFIRM:     int = arcade.key.SPACE     # <- Confirm play, confirm prompt, selection
    KEY_SORT:        int = arcade.key.S

    # Selection key mapping:
    KEY_ARROW_LEFT:  int = arcade.key.LEFT
    KEY_ARROW_RIGHT: int = arcade.key.RIGHT
    KEY_ARROW_UP:    int = arcade.key.UP
    KEY_ARROW_DOWN:  int = arcade.key.DOWN


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def __cached_key_list_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.

        :return tuple[str, ...]: ...
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "key_list",
            "key_user_list",
            "key_debug_list",
            )
        
        # Returning:
        return cached_property_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ALL KEY LISTS PROPERTIES BLOCK
    
    """


    @cached_property
    def key_list(self) -> tuple[int, ...]:
        """
        TODO: Create a docstring.
        """

        # Acquiring all recognized keys:
        key_list: tuple[int, ...] = tuple(
            key_stored for key_stored in self.__dict__.values()
            if key_stored is not None
            )
        
        # Returning:
        return key_list
    
    
    @cached_property
    def key_user_list(self) -> tuple[int, ...]:
        """
        TODO: Create a docstring.
        """

        # Acquiring all recognized keys:
        key_list: tuple[int, ...] = tuple(
            key_stored for attribute_name, key_stored in self.__dict__.items()
            if key_stored in self.key_list and "DEBUG" not in attribute_name
            )
        
        # Returning:
        return key_list
    

    @cached_property
    def key_debug_list(self) -> tuple[int, ...]:
        """
        TODO: Create a docstring.
        """

        # Acquiring all recognized keys:
        key_list: tuple[int, ...] = tuple(
            key_stored for attribute_name, key_stored in self.__dict__.items()
            if key_stored in self.key_list and "DEBUG" in attribute_name
            )
        
        # Returning:
        return key_list
    

    @cached_property
    def key_debug_texture_list(self) -> tuple[int, ...]:
        """
        TODO: Create a docstring.
        """

        # Collecting key list:
        key_list: tuple[int, ...] = (
            self.KEY_DEBUG_SWITCH_TEXTURE_PACK_FRONT,
            self.KEY_DEBUG_SWITCH_TEXTURE_PACK_BACK,
            self.KEY_DEBUG_SET_TEXTURE_PACK_DEFAULT_LIGHT,
            self.KEY_DEBUG_SET_TEXTURE_PACK_DEFAULT_DARK,
            )
        
        # Returning:
        return key_list


    @cached_property
    def key_debug_sort_list(self) -> tuple[int, ...]:
        """
        TODO: Create a docstring.
        """

        # Collecting key list:
        key_list: tuple[int, ...] = (
            self.KEY_DEBUG_SORT_HAND_BY_VALUE,
            self.KEY_DEBUG_SORT_HAND_BY_VALUE_DEFAULT,
            self.KEY_DEBUG_SORT_HAND_BY_TIME_ADDED,
            self.KEY_DEBUG_SORT_HAND_BY_SUIT,
            )
        
        # Returning:
        return key_list
    

    @cached_property
    def key_debug_draw_list(self) -> tuple[int, ...]:
        """
        TODO: Create a docstring.
        """

        # Collecting key list:
        key_list: tuple[int, ...] = (
            self.KEY_DEBUG_DRAW_CARD_PLAYER,
            self.KEY_DEBUG_DRAW_CARD_OPPONENT,
            )
        
        # Returning:
        return key_list
    

    @cached_property
    def key_debug_sweep_list(self) -> tuple[int, ...]:
        """
        TODO: Create a docstring.
        """

        # Collecting key list:
        key_list: tuple[int, ...] = (
            self.KEY_DEBUG_SWEEP_TO_HAND_PLAYER,
            self.KEY_DEBUG_SWEEP_TO_HAND_OPPONENT,
            self.KEY_DEBUG_SWEEP_TO_DISCARD,
            )
        
        # Returning:
        return key_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    NORMAL KEY LISTS PROPERTIES BLOCK
    
    """

    ...

