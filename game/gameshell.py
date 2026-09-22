# Arcade library
import arcade

# Settings and session instance:
from game.settings import SETTINGS
from game.session import SESSION

# Context and namespace variables:
from game.context import Coordinates, Location, RGB_Color

# Controllers and other instances:
from game.controller.surface import Surface
from game.controller.deck import Deck


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

        # Controller attributes:
        self.__surface_controller: Surface = Surface()
        self.__game_controller: object = None               # TODO: Implement!
        self.__ui_controller: object = None                 # TODO: Implement!
        
        # Test attributes:
        self.__deck = Deck()
        self.__deck.generate(None, SETTINGS.DECK_SIZE_MIN)
        
    
    def on_draw(self) -> None:
        
        # Cleaning up previous frame:
        self.clear()
        
        # Rendering area in debug mode:
        if SESSION.ENABLE_DEBUG:
            self.__surface_controller.display_debug()
            
        for card in self.__deck.cards:
            card.display()
            
            
    def on_mouse_motion(self, coordinate_x, coordinate_y, shift_x, shift_y):
        ...     # TODO: Implement
            

    def on_mouse_press(self, coordinate_x, coordinate_y, button, modifiers):
        print(self.__surface_controller.locate_area((int(coordinate_x), int(coordinate_y))))
        
    
    def on_mouse_release(self, coordinate_x, coordinate_y, button, modifiers):
        ...     # TODO: Check documentation and implement!
        
        
    def on_mouse_leave(self, coordinate_x, coordinate_y):
        ...     # TODO: Check documentation and implement!
        

    def on_mouse_enter(self, coordinate_x, coordinate_y):
        ...     # TODO: Check documentation and implement!
    
        
    def on_key_press(self, key_pressed, modifiers):
        ...     # TODO: Check documentation and implement!
    
    
    def on_key_release(self, key_released, modifiers):
        ...     # TODO: Check documentation and implement!
    
    
    def on_update(self, delta_time):
        return super().on_update(delta_time)
        ...     # TODO: Implement
        
