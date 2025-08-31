# Random library import:
import random

# Arcade-related import:
import arcade
from arcade import Texture, Rect

# Settings and variables import list:
from game.collections import SORT_METHOD
from game.settings import *

# Developer session values:
from game.controllers.session import (
    DEV_ENABLE_DEBUG_AREA_RENDER,
    DEV_ENABLE_ASSERTION,
    DEV_ENABLE_ECHO,
    )

# Game status import list:
from game.status import (
    GameStatus,
    GAME_STATE, 
    TURN_STATE,
    ROUND_STATE,
    )

# Game controller import::
from game.controllers.game import GameController


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GAMESHELL BLOCK

"""


class Gameshell(arcade.Window):


    def __init__(self) -> None:

        # Calling Window parent class initialization:
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
        self.__game_controller: GameController = GameController()
        self.__setup_game_controller()

        # Update rate counter:
        self.__update_count: int = 0


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    GAMESHELL SETUP METHODS BLOCK
    
    TODO: Create a docstring

    """


    def __setup_game_controller(self) -> None:
        """
        TODO: Create a docstring.
        """

        self.__game_controller.game_init()
        self.__game_controller.game_prepare()

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    MISC METHODS BLOCK
    
    Miscellaneous private methods related to card object designed to reduce code repetition and 
    redundancy, or to simplify several for-loops when clearing cache with a function imported from
    scripts.py.

    """

    
    ...


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    NATIVE METHODS BLOCK
    
    Native arcade Window methods related to game logic, rendering, and event-handling.
    TODO: Create a docstring.

    """


    
    def on_update(self, delta_time):
        """
        This method can be implemented and is reserved for game logic. Move sprites. Perform 
        collision checks and other game logic. This method is called every frame before 
        :meth:`on_draw`.

        The ``delta_time`` can be used to make sure the game runs at the same
        speed, no matter the frame rate.

        :param float delta_time: Time interval since the last time the function was called in 
            seconds.
        """
        
        # Handling card slide (if required):
        self.__game_controller.handle_slide()

        if self.__game_controller.player_active == self.__game_controller.player_two:
            if self.__update_count > PLAY_DELAY_SECONDS:
                self.__game_controller.event_computer_turn()
                self.__update_count: int = 0
            self.__update_count += delta_time
            

    def on_draw(self):
        """
        TODO: Create a docstring.
        """

        # Clearing previous frame:
        self.clear()

        # Debug rendering:
        self.__game_controller.render()

    
    def on_mouse_press(self, 
                       cursor_coordinate_x: float, 
                       cursor_coordinate_y: float, 
                       button_pressed: int,
                       modifiers
                       ) -> None:
        """
        TODO: Create a docstring.
        """

        # Handling mouse click with game controller:
        if button_pressed == arcade.MOUSE_BUTTON_LEFT:
            self.__game_controller.handle_mouse_press(
                cursor_coordinate_x = cursor_coordinate_x,
                cursor_coordinate_y = cursor_coordinate_y,
                )

    
    def on_mouse_motion(self, 
                        cursor_coordinate_x: float, 
                        cursor_coordinate_y: float, 
                        coordinate_x_difference: float, 
                        coordinate_y_difference: float
                        ) -> None:
        """
        TODO: Create a docstring.
        """

        # Handling mouse motion with game controller:
        self.__game_controller.handle_mouse_motion(
            cursor_coordinate_x = cursor_coordinate_x,
            cursor_coordinate_y = cursor_coordinate_y,
            coordinate_x_difference = coordinate_x_difference,
            coordinate_y_difference = coordinate_y_difference
            )


    def on_key_press(self, key_pressed: int, modifiers):
        """
        TODO: Create a docstring.
        """

        if key_pressed == arcade.key.R:
            self.__game_controller: GameController = GameController()
            self.__setup_game_controller()
        elif key_pressed == arcade.key.A:
            self.__game_controller.event_draw_card(
                player_controller=self.__game_controller.player_one, debug_update = True
                )
        elif key_pressed == arcade.key.S:
            self.__game_controller.event_draw_card(
                player_controller=self.__game_controller.player_two
                )
        elif key_pressed == arcade.key.SPACE:
            print(self.__game_controller.game_status.waiting_input)
            if self.__game_controller.game_status.waiting_input:
                if self.__game_controller.game_status.end_turn_func_set is not None:
                    func_set = self.__game_controller.game_status.end_turn_func_set 
                    self.__game_controller.event_end_turn(
                        sweep_cards = func_set.sweep_cards,
                        switch_active = func_set.switch_active,
                        switch_focus = func_set.switch_focus
                        )
                    self.game_status.end_turn_func_set = None
                    self.__game_controller.game_status.waiting_input = False
                else:
                    self.__game_controller.switch_players_state_active()
                    self.__game_controller.event_analyze_turn_state()
            else:
                self.__game_controller.switch_players_state_active()
                self.__game_controller.event_analyze_turn_state()

        else:
            if key_pressed in (arcade.key.Z, arcade.key.X, arcade.key.C, arcade.key.V):
                sort_method: str = SORT_METHOD.BY_SUIT

                if key_pressed == arcade.key.Z:
                    sort_method = SORT_METHOD.BY_SUIT
                elif key_pressed == arcade.key.X:
                    sort_method = SORT_METHOD.BY_VALUE
                elif key_pressed == arcade.key.C:
                    sort_method = SORT_METHOD.BY_VALUE_C
                elif key_pressed == arcade.key.V:
                    sort_method = SORT_METHOD.BY_ADDED

                self.__game_controller.player_one.sort_hand(
                    sort_method=sort_method,
                    update_position=True
                    )
