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
from game.controller.table import Table

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
        self.__deck.setup(
            trump_suit = None, 
            )
        self.__hand = Hand()
        self.__hand.setup(
            set_owner = context.PLAYER_TYPE.HUMAN,
            ignore_assertion = True,
            )
        self.__hand_opp = Hand()
        self.__hand_opp.setup(
            set_owner = context.PLAYER_TYPE.COMPUTER,
            ignore_assertion = True,
            )
        self.__table = Table()
        self.__table.setup()
        
        # Boundary attributes:
        self.__hit_area: Area | None = None
        self.__hit_card_list: list[Card] = []
        self.__card_hover: Card | None = None
        
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
            if hit_area != AREA_PLAYER and self.__card_hover is not None:
                self.__card_hover.set_state_hovered(False, True, True)
                self.__card_hover = None
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
            elif hit_area == AREA_PLAYER:
                hover_temp = []
                for card_object in self.__hand.cards:
                    card_object_hit: bool = card_object.hit_boundary(
                        hit_coordinates = coordinates,
                        ignore_assertion = True
                        )
                    if card_object_hit:
                        hover_temp.append(
                            card_object
                            )
                if hover_temp:
                    self.__hit_card_list = hover_temp
                    self.__hit_card_list.sort(
                        key = lambda card: card.hit_boundary_value(
                            hit_coordinates = coordinates,
                            ignore_assertion = True
                            ),
                        reverse = False,
                        )
                    if self.__card_hover is not None and self.__card_hover != self.__hit_card_list[0]:
                        self.__card_hover.set_state_hovered(False, True, True)
                    self.__card_hover = self.__hit_card_list[0]
                    self.__card_hover.set_state_hovered(True, True, True)
                else:
                    self.__hit_card_list = []
                    if self.__card_hover is not None:
                        self.__card_hover.set_state_hovered(False, True, True)
                    
                    
            

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
            for controller in (self.__deck, self.__hand, self.__hand_opp, self.__table):
                controller.reset()
            
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
                    slide_speed_modifier = 2.00,
                    clear_cache = True
                    )
        if self.__hit_area == AREA_PLAYER:
            if self.__card_hover is not None:
                if self.__card_hover.coordinates_expected == self.__card_hover.coordinates_hover:
                    mod = 2
                else:
                    mod = 0.85
                self.__card_hover.slide(
                    slide_speed_modifier = mod,
                    clear_cache = True
                    )
                
            
            
        
