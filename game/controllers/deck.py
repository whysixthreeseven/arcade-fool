# Annotations, typing etc. import:
from __future__ import annotations

# Cache-related import:
from functools import cached_property
from itertools import product

# Random library import:
import random

# Arcade library import:
import arcade
from arcade import Rect, Text, Texture

# Variables, settings, and directories import:
from game.settings import (
    DECK_RENDER_SHIFT_THRESHOLD,
    DECK_RENDER_COORDINATE_SHIFT_X,
    DECK_RENDER_COORDINATE_SHIFT_Y
    )

# Controllers import:
from game.controllers.card import Card_Object

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
DECK OBJECT CLASS BLOCK
"""


class Deck_Controller:

    def __init__(self) -> None:
        
        # Core attributes:
        self.__deck_container: list[Card_Object] = []
        self.__deck_trump: str = None

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    OVERWRITTEN MAGIC METHODS BLOCK
    
    """

    
    def __str__(self):
        """
        TODO: Create a docstring.
        """

        # Generating new string value:
        echo_string: str = ""

        # Returning:
        return echo_string
    

    def __repr__(self):
        """
        TODO: Create a docstring.
        """

        # Generating new string value:
        echo_string: str = ""

        # Returning:
        return echo_string


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def __cached_deck_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "deck_container",
            "deck_count",
            "deck_value",
            "deck_trump",
            )
        
        # Returning:
        return cached_property_list

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    DECK OBJECT CLASS BLOCK
    """


    @cached_property
    def deck_sealed(self) -> list[Card_Object]:
        """
        TODO: Create a docstring.

        Cached. Cannot be cleared.
        """
        
        # Creating card combinations list:
        card_object_combination_list: tuple[str, str] = product(
            Card_Object.CARD_SUIT_LIST,
            Card_Object.CARD_TYPE_LIST
            )
        
        # Creating card objects and forming a list:
        card_object_list: list[Card_Object] = []
        for card_suit, card_type in card_object_combination_list:
            card_object: Card_Object = Card_Object.create_card_object(
                init_suit = card_suit,
                init_type = card_type
                )
            
            # Updating card object's attributes:
            position_index: int = len(card_object_list)
            card_object.set_position_deck(
                position_index = position_index
                )
            card_object.set_state_revealed(
                set_value = False
                )
            
            # Adding card object to the list:
            card_object_list.append(
                card_object
                )
            
        # Reversing the list:
        card_object_list_reversed: list[Card_Object] = list(reversed(card_object_list))
        
        # Returning:
        return card_object_list_reversed


    @cached_property
    def deck_container(self) -> list[Card_Object]:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__deck_container
    

    @cached_property
    def deck_count(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        deck_count: int = len(self.deck_container)

        # Returning:
        return deck_count
    

    @cached_property
    def deck_value(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating deck value:
        deck_value: int = 0 
        if self.deck_count > 0:
            for card_object in self.deck_container:
                deck_value += card_object.type_value

        # Returning:
        return deck_value
    

    @cached_property
    def deck_trump(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__deck_trump
    

    def create_deck(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        self.__deck_container: list[Card_Object] = self.deck_sealed

        # Shuffling deck:
        random.shuffle(self.__deck_container)
        
        # Setting a random trump suit value:
        self.set_deck_trump(
            set_value = None,           # <- None sets random
            clear_cache = False
            )
        
        # Clearing cache:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_deck_property_list
            )
        
    
    def set_deck_trump(self, set_value: str | None, clear_cache: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Selecting parameter as suit value:
        deck_trump_selected: str | None = set_value

        # Getting a random suit value:
        if deck_trump_selected is None:
            deck_trump_selected: str = random.choice(
                seq = Card_Object.CARD_SUIT_LIST
                )
        
        # Updating attribute:
        if self.deck_trump != deck_trump_selected:
            self.__deck_trump: str = deck_trump_selected

            # Updating card objects:
            if self.deck_count > 0:
                for card_object in self.deck_container:
                    if card_object.suit == deck_trump_selected:
                        card_object.set_state_trump(
                            set_value = True
                            )

            # Clearing cache (deck):
            if clear_cache:
                clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = self.__cached_deck_property_list
                    )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    REMOVE/DRAW CARD METHODS AND PROPERTIES BLOCK
    
    """

    
    @property
    def next_card(self) -> Card_Object | None:
        """
        TODO: Create a docstring.
        """

        # Getting the next (top) card from the deck:
        card_object: Card_Object | None = None
        if self.deck_count > 0:
            card_object: Card_Object = self.deck_container[0]

        # Returning:
        return card_object
    

    def draw_card(self) -> Card_Object | None:
        """
        TODO: Create a docstring.
        """

        # If card exists, removing it from the container:
        card_object: Card_Object | None = self.next_card
        if card_object is not None:
            self.remove_card(
                card_object = card_object,
                clear_cache = False
                )
            
        # Clearing cache:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_deck_property_list
            )
        
        # Returning:
        return card_object
    

    def remove_card(self, card_object: Card_Object, clear_cache: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Removing card from the deck container:
        if card_object in self.deck_container:
            self.__deck_container.remove(
                card_object
                )
            
            # Resetting card object's position:
            card_object.reset_position()

            # Clearing cache (deck):
            if clear_cache:
                clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = self.__cached_deck_property_list
                    )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    RENDER METHODS AND PROPERTIES BLOCK
    
    """


    def render(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Shift variables:
        coordinate_x_shift: int = 0
        coordinate_y_shift: int = 0

        # Counting cards while cycling through the deck:
        card_count: int = 0
        if self.deck_count > 0:
            for card_object in self.deck_container:
                card_count += 1

                # Checking if rendering and/or shift is required::
                render_required: bool = bool(
                    card_count == 0 or
                    card_count // DECK_RENDER_SHIFT_THRESHOLD == 0
                    )
                shift_required: bool = bool(
                    card_count > 0 and
                    card_count // DECK_RENDER_SHIFT_THRESHOLD == 0
                    )
                
                # Shifting coordinates:
                if shift_required:
                    coordinate_x_shift += DECK_RENDER_COORDINATE_SHIFT_X
                    coordinate_y_shift += DECK_RENDER_COORDINATE_SHIFT_Y

                # Rendering:
                if render_required:
                    card_object.render()
    
    