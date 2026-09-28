# Arcade library
import arcade

# Settings and session instance:
from game.settings import SETTINGS
from game.session import SESSION

# Context and namespace variables:
from game.context import (
    Coordinates, 
    Location, 
    RGB_Color
    )

# Controllers and other instances:
from game.controller.surface import Surface
from game.controller.hand import Hand
from game.controller.deck import Deck
from game.controller.card import Card

# Area instances:
from game.utilities.area import (
    Area, 
    AREA_TABLE,
    AREA_DECK,
    AREA_DISCARD,
    AREA_PLAYER,
    AREA_OPPONENT,
    )
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

        # Controller attributes:
        self.__surface_controller: Surface = Surface()
        self.__game_controller: object = None               # TODO: Implement!
        self.__ui_controller: object = None                 # TODO: Implement!
        
        # Test attributes:
        self.__deck = Deck()
        self.__deck.generate(None, SETTINGS.DECK_SIZE_MIN)
        self.__hand = Hand()
        self.__hand.set_owner(
            set_value = context.PLAYER_TYPE.HUMAN,
            ignore_assertion = True,
            clear_cache = True
            )
        self.__hand_opp = Hand()
        self.__hand_opp.set_owner(
            set_value = context.PLAYER_TYPE.COMPUTER,
            ignore_assertion = True,
            clear_cache = True
            )
        
        # Boundary attributes:
        self.__hit_area: Area | None = None
        self.__hit_card_list: list[Card] = []
        
        # Cursor coordinates:
        self.__cursor_coordinate_x: int = 0
        self.__cursor_coordinate_y: int = 0
        
    
    def on_draw(self) -> None:
        
        # Cleaning up previous frame:
        self.clear()
        
        # Rendering area in debug mode:
        if SESSION.ENABLE_DEBUG:
            self.__surface_controller.display_debug()
            
        self.__deck.display()
        self.__hand.display()
        self.__hand_opp.display()

        if self.__hit_card_list:
            self.__deck.display_info(
                display_coordinates = (
                    self.__cursor_coordinate_x,
                    self.__cursor_coordinate_y,
                    ),
                ignore_assertion = True,
                )
            
            
    def on_mouse_motion(self, coordinate_x, coordinate_y, shift_x, shift_y):
        
        # Packing coordinates:
        coordinates: Coordinates = (
            int(coordinate_x), 
            int(coordinate_y)
            )

        # Updating area hit:
        hit_area: Area | None = self.__surface_controller.locate_area(coordinates)
        if self.__hit_area != hit_area:
            self.__hit_area = hit_area
        
        # Updating card hit:
        hit_card: Card | None = None
        if hit_area is None:
            pass
        else:
            if hit_area == AREA_DECK:
                card_hit_list: list[Card] = []
                for card_object in self.__deck.cards:
                    card_object_hit: bool = card_object.hit_boundary(
                        hit_coordinates = coordinates,
                        ignore_assertion = True
                        )
                    if card_object_hit:
                        if card_object not in card_hit_list:
                            card_hit_list.append(
                                card_object
                                )
                self.__hit_card_list = card_hit_list
                self.__cursor_coordinate_x = coordinate_x
                self.__cursor_coordinate_y = coordinate_y
            

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
        
        # Drawing card for player:
        if key_released == arcade.key.D:
            if self.__deck.cards_count > 0:
                card = self.__deck.draw_card()
                self.__hand.add_card(
                    card_object = card,
                    ignore_assertion = False,
                    clear_cache = True,
                    )
                self.__hand.update_coordinates(
                    clear_cache = True
                    )
                
        # Drawing card for opponent:
        if key_released == arcade.key.F:
            if self.__deck.cards_count > 0:
                card = self.__deck.draw_card()
                self.__hand_opp.add_card(
                    card_object = card,
                    ignore_assertion = False,
                    clear_cache = True,
                    )
                self.__hand_opp.update_coordinates(
                    clear_cache = True
                    )
        
        # Resetting game state:
        if key_released == arcade.key.R:
            self.__deck = Deck()
            self.__deck.generate(None, SETTINGS.DECK_SIZE_MIN)
            self.__hand = Hand()
            self.__hand_opp.set_owner(
                set_value = context.PLAYER_TYPE.HUMAN,
                ignore_assertion = True,
                clear_cache = True
                )
            self.__hand_opp = Hand()
            self.__hand_opp.set_owner(
                set_value = context.PLAYER_TYPE.COMPUTER,
                ignore_assertion = True,
                clear_cache = True
                )
            
        # Sorting player's hand:
        if key_released == arcade.key.Z:
            self.__hand.sort(
                sort_seq = context.HAND_SORT_SEQ.ADDED, 
                sort_reverse = False, 
                update_coordinates = True, 
                ignore_assertion = True, 
                clear_cache = True
                )
        if key_released == arcade.key.X:
            self.__hand.sort(
                sort_seq = context.HAND_SORT_SEQ.VALUE, 
                sort_reverse = False, 
                update_coordinates = True, 
                ignore_assertion = True, 
                clear_cache = True
                )
        if key_released == arcade.key.C:
            self.__hand.sort(
                sort_seq = context.HAND_SORT_SEQ.SUIT, 
                sort_reverse = False, 
                update_coordinates = True, 
                ignore_assertion = True, 
                clear_cache = True
                )
        if key_released == arcade.key.V:
            self.__hand.sort(
                sort_seq = context.HAND_SORT_SEQ.COLOR, 
                sort_reverse = False, 
                update_coordinates = True, 
                ignore_assertion = True, 
                clear_cache = True
                )
        
        # Randomly shuffling opponent's hand:
        if key_released == arcade.key.B:
            self.__hand_opp.sort_random(
                update_coordinates = True, 
                clear_cache = True
                )
            
    
    def on_update(self, delta_time):
        for hand_container in (self.__hand.cards, self.__hand_opp.cards):
            for card_object in hand_container:
                card_object.update_coordinates_state(
                    clear_cache = True
                    )
                co = card_object
                card_object.slide(
                    slide_speed_modifier = 1.50,
                    clear_cache = True
                    )
            
        
