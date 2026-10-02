# Controllers:
from game.controller.game import Game

# External libraries:
import arcade

# Settings, session and context:
from game.settings import SETTINGS
from game.session import SESSION
from game import context


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    GAMESHELL CLASS INSTANCE CONSTRUCTOR
    
"""


class Gameshell(arcade.Window):
    
    def __init__(self) -> None:
        
        # Initializing window using SETTINGS variables:
        super().__init__(
            width = SETTINGS.WINDOW_WIDTH,
            height = SETTINGS.WINDOW_HEIGHT,
            title = SETTINGS.WINDOW_TITLE,
            fullscreen = SETTINGS.WINDOW_FULLSCREEN,
            resizable = SETTINGS.WINDOW_RESIZABLE,
            update_rate = SETTINGS.WINDOW_UPDATE_RATE,
            antialiasing = SETTINGS.WINDOW_ANTIALIASING,
            )
        
        # Game controller:
        self.__game_controller: Game = Game()
        self.__game_controller.setup()
        self.__game_controller.game_start()
        
    
    @property
    def __gc(self) -> Game:
        return self.__game_controller
    
    
    def on_draw(self) -> None:
        
        # Cleaning up previous frame:
        self.clear()
        
        # Rendering surface and card containers in order:
        self.__gc.display_surface()
        self.__gc.display_cards()
        
        # Rendering hints, if available:
        if SESSION.ENABLE_HINT:
            self.__gc.display_hints()
            
            
    def on_mouse_motion(self, coordinate_x, coordinate_y, shift_x, shift_y):
        
        # Packing cursor coordinates:
        cursor_coordinates: context.Coordinates = (
            int(coordinate_x), 
            int(coordinate_y)
            )
        
        # Handling event:
        if self.__gc.user_mouse_enabled:
            self.__gc.handle_mouse_motion(
                cursor_coordinates = cursor_coordinates,
                ignore_assertion = False
                )
            

    def on_mouse_press(self, coordinate_x, coordinate_y, button, modifiers):
        ...     # TODO: Check documentation and implement!
        
    
    def on_mouse_leave(self, coordinate_x, coordinate_y):
        ...     # TODO: Check documentation and implement!
        

    def on_mouse_enter(self, coordinate_x, coordinate_y):
        ...     # TODO: Check documentation and implement!
    
        
    def on_key_press(self, key_pressed, modifiers):
        
        # Handling event:
        if self.__gc.user_keyboard_enabled:
            self.__gc.handle_key_press(
                key_pressed = key_pressed,
                ignore_assertion = False,
                )
    
    
    def on_update(self, delta_time):
        
        # Handling card slide:
        self.__gc.handle_slide(
            force_instant = False
            )
        
        self.__gc.update_event_pipe(
            autoremove = True,
            clear_cache = True,
            )
        
        

            