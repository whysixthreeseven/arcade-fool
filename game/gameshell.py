# Typing import:
from typing import Any

# Cache tools:
from functools import cached_property

# Arcade library import:
import arcade
from arcade import Rect, Text, Texture

# Gameshell-related settings import:
from game.settings import (

    # Game window settings:
    GAME_WINDOW_WIDTH,
    GAME_WINDOW_HEIGHT,
    GAME_WINDOW_FULLSCREEN,
    GAME_WINDOW_RESIZABLE,
    GAME_WINDOW_UPDATE_RATE,
    GAME_WINDOW_ANTIALIASING,
    GAME_WINDOW_TITLE,

    # Deck size:
    DECK_LOWEST_VALUE_DEFAULT,
    )

# Gameshell-related settings import:
from game.variables import *

# Zones import:
from game.collections.zone import (

    # Zone class object:
    Zone_XYWH,

    # Debugging zones:
    ZONE_GAME_AREA_PLAY,
    ZONE_GAME_AREA_SIDE,
    ZONE_PLAYER_ONE,
    ZONE_PLAYER_TWO,
    ZONE_TABLE,
    )

# Collections import:
from game.collections.keyboard import Keyboard_Mapping

# Controllers import:
from game.controllers.game import Game_Controller
from game.controllers.player import Player_Controller

# Session variables import:
from game.session import SESSION_ENABLE_DEBUG

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
GAMESHELL CLASS OBJECT BLOCK

"""


class Gameshell(arcade.Window):

    def __init__(self) -> None:

        # Initializing window with predefined settings:
        super().__init__(
            width        = GAME_WINDOW_WIDTH,
            height       = GAME_WINDOW_HEIGHT,
            title        = GAME_WINDOW_TITLE,
            fullscreen   = GAME_WINDOW_FULLSCREEN,
            resizable    = GAME_WINDOW_RESIZABLE,
            update_rate  = GAME_WINDOW_UPDATE_RATE,
            antialiasing = GAME_WINDOW_ANTIALIASING
            )
        
        # Game controller:
        self.__game_controller: Game_Controller = None
        self.__initialize_game_controller()


        self.__zones: tuple[Zone_XYWH, ...] = (
            ZONE_GAME_AREA_PLAY,
            ZONE_GAME_AREA_SIDE,
            ZONE_PLAYER_ONE,
            ZONE_PLAYER_TWO,
            ZONE_TABLE,
            )
        
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE METHODS AND PROPERTIES BLOCK
    
    """


    ...


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    GAME METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def game(self) -> Game_Controller:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__game_controller
    

    def __initialize_game_controller(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Creating game controller:
        self.__game_controller: Game_Controller = Game_Controller()

        # Creating session and starting a default game:
        self.__game_controller.create_session()
        self.__game_controller.create_game_default()

        # Clearing cache:
        cached_property: str = "game"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
        
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    NATIVE METHODS BLOCK
    
    """

    
    def on_update(self, delta_time: float) -> None:
        """
        TODO: Create a docstring.
        """

        # Nothing to do, yet.
        pass


    def on_draw(self):
        """
        TODO: Create a docstring.
        """

        # Clearing previous frame:
        self.clear()

        # Debugging, rendering game zones:
        for zone in self.__zones:
            zone.render()

        # Rendering containers:
        self.game.deck.render()
        # self.game.discard.render()        # <- TODO: Implement
        # self.game.table.render()

        # Rendering player controller's hand containers:
        self.game.player_one.hand.render()
        self.game.player_two.hand.render()

    
    def on_key_press(self, key_pressed: Any, key_modifiers):
        """
        TODO: Create a docstring.
        """

        # Asserting key is registered and recognized:
        if key_pressed in self.game.keyboard.key_list:

            # Checking if key pressed was a debug command:
            if key_pressed in self.game.keyboard.key_debug_list:

                # Warning debug mode was not enabled:
                if not SESSION_ENABLE_DEBUG:
                    warning_message: str = "Unable to execute command. Enable debug mode in session."
                    print(warning_message)

                # Executing debug command:
                else:
                    self.game.handle_debug_key_pressed(
                        key_pressed = key_pressed
                        )
            
            # Otherwise, handling key pressed:
            else:
                
                # Executing command:
                self.game.handle_key_pressed(
                    key_pressed = key_pressed
                    )
                

    def on_mouse_motion(self, 
                        motion_coordinate_x: Any, 
                        motion_coordinate_y: Any, 
                        motion_coordinate_dx: Any, 
                        motion_coordinate_dy: Any
                        ) -> None:
        """
        TODO: Create a docstring.

        :param int | float motion_coordinate_x: ...
        :param int | float motion_coordinate_y: ...
        :param int | float motion_coordinate_dx: ...
        :param int | float motion_coordinate_dy: ...
        """

        # Packing up:
        motion_coordinates: tuple[int, int] = (
            motion_coordinate_x,
            motion_coordinate_y
            )

        # Handling mouse motion:
        self.game.handle_mouse_motion(
            motion_coordinates = motion_coordinates
            )