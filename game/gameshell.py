# Controllers:
from game.controller.player import PlayerController
from game.controller.discard import DiscardController
from game.controller.table import TableController
from game.controller.deck import DeckController
from game.controller.hand import HandController
from game.controller.card import CardController as Card
from game.controller.surface import SurfaceController
from game.controller.game import Game

# External libraries:
import random
import arcade
import time

# Settings, session and context:
from game.settings import SETTINGS
from game.session import SESSION
from game import context

# Cache management:
from functools import cached_property
from game.utilities.scripts import cache

# Various utilities:
from game.utilities import area, texturepack
from game.utilities.scripts import assertion, validate


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
        
    
    @property
    def gc(self) -> Game:
        return self.__game_controller
    
    
    def on_draw(self) -> None:
        
        # Cleaning up previous frame:
        self.clear()
        
        # Rendering area in debug mode:
        if SESSION.ENABLE_DEBUG:
            self.gc.surface.display_debug()
            
        # Rendering card containers in order:
        self.gc.deck.display()
        self.gc.discard.display()
        self.gc.table.display()
        self.gc.player_computer.hand.display()
        self.gc.player_human.hand.display()
            
            
            
    def on_mouse_motion(self, coordinate_x, coordinate_y, shift_x, shift_y):
        
        # Packing cursor coordinates:
        cursor_coordinates: context.Coordinates = (coordinate_x, coordinate_y)
        
        # Updating current cursor coordinates:
        self.gc.set_cursor_coordinates(
            set_value = cursor_coordinates,
            ignore_assertion = True,
            )
        print(self.gc.cursor_coordinates)
                    
            

    def on_mouse_press(self, coordinate_x, coordinate_y, button, modifiers):
        ...     # TODO: Check documentation and implement!
        
    
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
        ...     # TODO: Check documentation and implement!
                
            
            
        
