# Annotations, typing etc. import:
from __future__ import annotations

# Cache-related import:
from functools import cached_property

# # Related settings import:
# from game.settings import (
#     ...
#     )

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


    def add_card(self, card_object: Card_Object, clear_cache: bool = True) -> None:
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
            target_attribute_list = self.__cached_hand_property_list
            )

