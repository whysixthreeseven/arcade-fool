# Annotations, typing etc. import:
from __future__ import annotations

# Cache-related import:
from functools import cached_property

# Random library:
import random

# Settings variables import list:
from game.settings import (

    # Discard-related settings:
    DISCARD_COORDINATE_X,
    DISCARD_COORDINATE_Y,
    DISCARD_COORDINATE_SHIFT_MIN,
    DISCARD_COORDINATE_SHIFT_MAX,
    DISCARD_COORDINATE_SHIFT_AXIS,
    )

# Controllers import:
from game.controllers.card import Card_Object

# Scripts import:
from game.scripts.convert import (
    convert_attribute_to_repr
    )
from game.scripts.cache import (
    clear_cached_property_list
    )


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DECK CLASS OBJECT BLOCK

"""


class Discard_Controller:
    
    def __init__(self) -> None:
        
        # Core attributes:
        self.__discard_container: list[Card_Object] = []

    
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
    def __cached_discard_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "discard_container",
            "discard_count",
            "discard_value"
            )
        
        # Returning:
        return cached_property_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    DISCARD CONTAINER METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def discard_container(self) -> list[Card_Object]:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__discard_container
    

    @cached_property
    def discard_count(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        discard_count: int = len(self.discard_container)

        # Returning:
        return discard_count
    

    @cached_property
    def discard_value(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        discard_value: int = 0
        for card_object in self.discard_container:
            discard_value += card_object.type_value
        
        # Returning:
        return discard_value
    

    def create_discard(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Creating a new container:
        discard_container: list[Card_Object] = []

        # Updating attribute:
        self.__discard_container: list[Card_Object] = discard_container

        # Clearing cache:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_discard_property_list
            )
    

    def reset_discard(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        self.__discard_container: list[Card_Object] = []

        # Clearing cache:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_discard_property_list
            )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ADD CARD OBJECT METHODS BLOCK
    
    """


    def add_card(self, 
                 card_object: Card_Object, 
                 clear_cache: bool = True, 
                 force_instant: bool = False
                 ) -> None:
        """
        TODO: Create a docstring.
        """

        # Checking if card does not exist in hand container:
        if card_object not in self.discard_container:

            # Resetting card object's position and state:
            card_object.reset_state()
            card_object.reset_position()

            # Updating card object's hand position:
            position_index: int = len(self.__discard_container)   # <- Using init container
            card_object.set_position_discard(
                position_index = position_index
                )
            
            # Revealing the card:
            card_object.set_state_revealed(
                set_value = True,
                )
            
            # Adding card object to hand container:
            self.__discard_container.append(
                card_object
                )
            
            # Preparing coordinates to update:
            coordinate_x_discard: int = DISCARD_COORDINATE_X
            coordinate_y_discard: int = DISCARD_COORDINATE_Y

            # Checking if shift is required:
            coordinate_shift_required: bool = random.choice((True, False))
            if coordinate_shift_required:

                # Calculating coordinate x shift:
                coordinate_x_shift_value: int = random.randint(
                    a = DISCARD_COORDINATE_SHIFT_MIN,
                    b = DISCARD_COORDINATE_SHIFT_MAX
                    )
                coordinate_x_shift_axis = random.choice(DISCARD_COORDINATE_SHIFT_AXIS)
                coordinate_x_shift: int = coordinate_x_shift_value * coordinate_x_shift_axis

                # Calculating coordinate y shift:
                coordinate_y_shift_value: int = random.randint(
                    a = DISCARD_COORDINATE_SHIFT_MIN,
                    b = DISCARD_COORDINATE_SHIFT_MAX
                    )
                coordinate_y_shift_axis = random.choice(DISCARD_COORDINATE_SHIFT_AXIS)
                coordinate_y_shift: int = coordinate_y_shift_value * coordinate_y_shift_axis

                # Updating coordinates generated:
                coordinate_x_discard += coordinate_x_shift
                coordinate_y_discard += coordinate_y_shift

            # Packing up coordinates:
            coordinates_discard: tuple[int, int] = (
                coordinate_x_discard,
                coordinate_y_discard
                )
            
            # Updating coordinates:
            card_object.set_coordinates_default(
                set_container = coordinates_discard,
                ignore_assertion = True
                )
            
            # Clearing cache (hand):
            if clear_cache:
                clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = self.__cached_discard_property_list
                    )
    

    def add_card_list(self, card_list: list[Card_Object]) -> None:
        """
        TODO: Create a docstring.
        """

        # Adding cards to the hand container:
        for card_object in card_list:
            self.add_card(
                card_object = card_object,
                clear_cache = False,
                )
            
        # Clearing cache (hand):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_discard_property_list
            )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    RENDER METHODS BLOCK
    
    """


    def render(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Cycling through cards and calling render method:
        for card_object in reversed(self.discard_container):
            card_object.render()

