# Annotations, typing etc. import:
from __future__ import annotations

# Cache-related import:
from functools import cached_property
from itertools import product

# Random library import:
import random

# Related settings import:
from game.settings import (

    # Deck render coordinates:
    DECK_RENDER_COORDINATE_X,
    DECK_RENDER_COORDINATE_Y,
    DECK_RENDER_COORDINATE_SHIFT_X,
    DECK_RENDER_COORDINATE_SHIFT_Y,
    DECK_RENDER_SHIFT_THRESHOLD_DEFAULT,

    # Card texture settings:
    CARD_TEXTURE_HEIGHT_SCALED,
    )

# Variables import:
from game.variables import CARD_SUIT_TAG

# Collections import:
from game.collections.texturepack import Texture_Pack

# Controllers import:
from game.controllers.card import Card_Object

# Session controller import:
from game.session import Session_Controller

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
        
        # Deck lists:
        self.__deck_container: list[Card_Object] = []
        self.__deck_render:    list[Card_Object] = []

        # Additional attributes:
        self.__deck_trump: str = None
        self.__deck_shift: int = DECK_RENDER_SHIFT_THRESHOLD_DEFAULT

    
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
            "deck_trump_repr",
            "deck_render"
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

        :return list[Card_Object]: ...
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
                init_type = card_type,
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
    def deck_render(self) -> list[Card_Object]:
        """
        TODO: Create a docstring.

        :return list[Card_Object]: ...
        """

        # Returning:
        return self.__deck_render


    @cached_property
    def deck_container(self) -> list[Card_Object]:
        """
        TODO: Create a docstring.

        :return list[Card_Object]: ...
        """

        # Returning:
        return self.__deck_container
    

    @cached_property
    def deck_count(self) -> int:
        """
        TODO: Create a docstring.

        :return int: ...
        """

        # Calculating:
        deck_count: int = len(self.deck_container)

        # Returning:
        return deck_count
    

    @cached_property
    def deck_value(self) -> int:
        """
        TODO: Create a docstring.

        :return int: ...
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

        :return str: ...
        """

        # Returning:
        return self.__deck_trump


    @cached_property
    def deck_trump_repr(self) -> str:
        """
        TODO: Create a docstring.

        :return str: ...
        """

        # Converting to repr format:
        deck_trump_repr: str = convert_attribute_to_repr(
            attribute_value = self.deck_trump,
            attribute_tag = CARD_SUIT_TAG,
            )
        
        # Returning:
        return deck_trump_repr


    def create_deck(self, 
                    deck_shift: int, 
                    deck_lowest_value: int, 
                    ignore_assertion: bool = False
                    ) -> None:
        """
        TODO: Create a new deck.

        :param int deck_shift: ...
        :param int deck_lowest_value: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        """

        # Updating deck shift:
        self.__deck_shift: int = deck_shift

        # Creating new deck container:
        self.__prepare_deck_container(
            deck_lowest_value = deck_lowest_value,
            )
        
        # Creating new deck render:
        card_trump: Card_Object = self.deck_container[-1]
        self.__prepare_deck_render(
            card_trump = card_trump,
            )


    def update_deck(self, 
                    texture_pack_front: Texture_Pack, 
                    texture_pack_back: Texture_Pack,
                    ignore_assertion: bool = False,
                    ) -> None:
        """
        TODO: Create a docstring.

        :param Texture_pack texture_pack_front: ...
        :param Texture_pack texture_pack_back: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        """

        # Acquiring deck containers and cycling through each:
        deck_collection_list: tuple[tuple[Card_Object, ...], ...] = (
            self.deck_container,
            self.deck_render
            )
        for deck_collection in deck_collection_list:

            # Updating texture packs per card object:
            for card_object in deck_collection:
                card_object.update_texture(
                    texture_pack_front = texture_pack_front,
                    texture_pack_back = texture_pack_back,
                    )


    def __prepare_deck_container(self, deck_lowest_value: int) -> None:
        """
        TODO: Create a docstring.

        :param int deck_lowest_value: ...

        :raise AssertionError: ...
        """

        # Selecting deck:
        deck_selected: list[Card_Object] = self.deck_sealed

        # Filtering deck, if required:
        deck_filtered: list[Card_Object] = [
            card_object for card_object
            in self.deck_sealed
            if card_object.type_value_default >= deck_lowest_value
            ]
        deck_selected: list[Card_Object] = deck_filtered

        # Shuffling deck and updating attribute:
        random.shuffle(deck_selected)
        self.__deck_container: list[Card_Object] = deck_selected

        # Selecting trump card:
        card_trump: Card_Object = self.__deck_container[-1]
        card_trump_suit: str = card_trump.suit
        
        # Updating attribute:
        self.__deck_trump: str = card_trump_suit

        # Updating card objects:
        if self.deck_count > 0:
            for card_object in self.deck_container:
                if card_object.suit == card_trump_suit:
                    card_object.set_state_trump(
                        set_value = True
                        )
        
        # Clearing cache (deck):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_deck_property_list
            )
        
    
    def __prepare_deck_render(self, card_trump: Card_Object) -> None:
        """
        TODO: Create a docstring.

        :param Card_Object card_trump: ...
        """

        # Preparing coordinate shift values:
        coordinate_x_shift: int = 0
        coordinate_y_shift: int = 0
        
        # Creating a render deck container:
        deck_render: list[Card_Object] = []
        deck_render_size: int = 0
        deck_render_max_size: int = self.deck_count - 1
        while deck_render_size < deck_render_max_size:

            # Creating "fake" card:
            suit_choice: str = Card_Object.CARD_SUIT_LIST[0]
            type_choice: str = Card_Object.CARD_TYPE_LIST[0]
            card_render: Card_Object = Card_Object.create_card_object(
                init_suit = suit_choice,
                init_type = type_choice,
                texture_pack_front = card_trump.texture_pack_front,
                texture_pack_back = card_trump.texture_pack_back,
                )
            
            # Updating card object's attributes:
            position_index: int = len(deck_render)
            card_render.set_position_deck(
                position_index = position_index
                )
            card_render.set_state_revealed(
                set_value = False
                )
            
            # Adding card to the list:
            deck_render.append(
                card_render
                )
            
            # Updating size variable:
            deck_render_size: int = len(deck_render)

        # Setting coordinates in reversed order:
        card_render_count: int = 0
        for card_render in reversed(deck_render):
            card_render_count += 1

            # Checking if coordinate shift is required:      
            shift_required: bool = bool(
                card_render_count >= 1 and
                card_render_count % self.__deck_shift == 0
                )
            if shift_required:
                coordinate_x_shift += DECK_RENDER_COORDINATE_SHIFT_X
                coordinate_y_shift += DECK_RENDER_COORDINATE_SHIFT_Y

            # Calculating coordinates:
            card_coordinate_x: int = DECK_RENDER_COORDINATE_X + coordinate_x_shift
            card_coordinate_y: int = DECK_RENDER_COORDINATE_Y + coordinate_y_shift
            card_coordinates: tuple[int, int] = (
                card_coordinate_x,
                card_coordinate_y
                )

            # Updating coordinates:
            card_render.set_coordinates_default(
                set_container = card_coordinates,
                ignore_assertion = True,
                )
            card_render.set_coordinates_current(
                set_container = card_coordinates,
                ignore_assertion = True
                )

        # Creating a showcase trump card:
        card_render_trump: Card_Object = Card_Object.create_card_object(
            init_suit = card_trump.suit,
            init_type = card_trump.type_f
            )
        # Calculating coordinates:
        card_coordinate_x: int = int(DECK_RENDER_COORDINATE_X - CARD_TEXTURE_HEIGHT_SCALED / 3)
        card_coordinate_y: int = DECK_RENDER_COORDINATE_Y
        card_coordinates: tuple[int, int] = (
            card_coordinate_x,
            card_coordinate_y
            )
        
        # Updating showcase trump card's coordinates:
        card_render_trump.set_coordinates_default(
            set_container = card_coordinates,
            ignore_assertion = True,
            )
        card_render_trump.set_coordinates_current(
            set_container = card_coordinates,
            ignore_assertion = True
            )
        
        # Updating showcase trump card's attributes:
        position_index: int = len(deck_render)
        card_render_trump.set_position_deck(
            position_index = position_index
            )
        card_render_trump.set_state_revealed(
            set_value = True
            )
        card_render_trump.set_state_showcase(
            set_value = True
            )
        
        # Adding card to the list:
        deck_render.append(
            card_render_trump
            )
        
        # Updating attribute:
        self.__deck_render: list[Card_Object] = deck_render
        
        # Clearing cache:
        cached_property: str = "deck_render"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    REMOVE/DRAW CARD METHODS AND PROPERTIES BLOCK
    
    """

    
    @property
    def next_card(self) -> Card_Object | None:
        """
        TODO: Create a docstring.

        :return Card_Object: ...
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

        :return Card_Object: ...
        """

        # If card exists, removing it from the container:
        card_object: Card_Object | None = self.next_card
        if card_object is not None:
            self.remove_card(
                card_object = card_object,
                clear_cache = False
                )
            
        # Clearing cache (deck):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_deck_property_list
            )
        
        # Returning:
        return card_object
    

    def draw_card_highest_value(self) -> Card_Object | None:
        """
        TODO: Create a docstring.

        :return Card_Object: ...
        :return None: ...
        """

        # Acquiring highest value card:
        card_object: Card_Object | None = None
        if self.deck_count > 0:

            # Sorting deck container and getting highest value card:
            deck_sorted: list[Card_Object] = sorted(
                self.deck_container,
                key = lambda card_object: card_object.type_value,
                reverse = True,
                )
            card_object: Card_Object = deck_sorted[0]

            # Removing card from deck container:
            self.remove_card(
                card_object = card_object,
                clear_cache = False
                )
            
            # Clearing cache (deck):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_deck_property_list
                )

        # Returning:
        return card_object


    def remove_card(self, card_object: Card_Object, clear_cache: bool = True) -> None:
        """
        TODO: Create a docstring.

        :param Card_object card_object: ...
        :param bool clear_cache: ...

        :raise AssertionError: ...
        """

        # Removing card from the deck container:
        if card_object in self.deck_container:
            self.__deck_container.remove(
                card_object
                )

            # Deck render update (removing one card from the container):
            self.__deck_render.pop(0)

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

        # Cycling through cards in reversed order:
        card_render_count: int = 0
        for card_render in reversed(self.deck_render):
            card_render_count += 1

            # Checking if render is required:
            render_required: bool = bool(
                card_render_count > 0 and bool(
                    card_render_count % self.__deck_shift == 0 or 
                    card_render_count < self.__deck_shift or
                    card_render_count == 1
                    )
                )
            
            # Rendering:
            if render_required:
                card_render.render()

