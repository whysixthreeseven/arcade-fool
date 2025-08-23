# Annotation import:
from __future__ import annotations

# Cache-related modules and scripts import:
from game.collections.scripts import clear_cached_property
from functools import cached_property
from itertools import product

# Random library import:
import random

# Settings and variables import list:
from game.variables import *
from game.settings import *

# Developer session values:
from game.session import (
    DEV_ENABLE_ASSERTION,
    DEV_ENABLE_ECHO,
    )

# Assertion functions import:
from game.collections.scripts import (
    assert_value_is_default,
    assert_value_is_valid_type,
    assert_value_in_valid_range,
    )

# Collections import:
from game.collections.card import Card


class PlayerController:

    def __init__(self) -> None:

        self.__hand_container: list[Card] = []

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    MISC METHODS BLOCK
    
    Miscellaneous private methods related to player controller designed to reduce code repetition 
    and redundancy, or to simplify several for-loops when clearing cache with a function imported 
    from scripts.py.

    """


    
    def __clear_cached_property(self, target_attribute: str) -> None:
        """
        Clears cache based on the attribute name, if it exeists in class object's dictionary via
        hasattr and delattr functions. Uses script from scripts.py. "Wraps" the script's function
        to shorten the syntax, since target_object is always self.

        :param str target_attribute: Cached attribute name string name.
        """

        # Clearing cache:
        clear_cached_property(
            target_object = self,
            target_attribute = target_attribute
            )
        
    
    def __clear_cached_property_list(self, target_list: tuple[str, ...]) -> None:
        """
        Clears cache based on the attribute name from the provided tuple container of properties
        list. Cycles through the attribute names and if it exists, deletes it.

        :param tuple[str, ...] target_list: Tuple container with attribute name strings.
        """

        # CLearing cache:
        for target_attribute in target_list:
            self.__clear_cached_property(
                target_attribute = target_attribute
                )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE PROPERTIES BLOCK
    
    Private cached properties dedicated to storing and returning tuple containers with related to
    their block's cachced property lists (e.g. __cached_hand_property_list would return all the 
    cached property (attribute) string value names to clear via a different clear cache function).

    """


    @cached_property
    def __cached_hand_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache. 
        
        Cached.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g. for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "hand_container",
            "hand_count",
            "hand_value",
            "hand_position_index"
            )
        
        # Returning:
        return cached_property_list


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    HAND METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def hand_container(self) -> list[Card]:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__hand_container


    @cached_property
    def hand_count(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        hand_container_count: int = len(self.hand_container)

        # Returning:
        return hand_container_count

    
    @cached_property
    def hand_value(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        hand_value: int = 0
        if self.hand_count >= 1:
            for card_object in self.hand_container:
                hand_value += card_object.card_type_value
        
        # Returning:
        return hand_value


    @property
    def hand_position_index(self) -> dict[int, tuple[int, int]]:
        """
        TODO: Create a docstring.
        """

        ...


    def __update_hand_position(self) -> None:
        """
        TODO: Create a docstring.
        """

        ...


    def __update_hand_state(self) -> None:
        """
        TODO: Create a docstring.
        """

        ...


    def update_hand(self) -> None:
        """
        TODO: Create a docstring.
        """

        ...


    def sort_hand(self, 
                  sort_method: str,                 # Default sort method as in SESSION controller
                  ignore_trump: bool = True,        # Ignore trump value if card suit is trump suit
                  ascending_order: bool = True      # Value and card suit priority order
                  ) -> None:
        """
        TODO: Create a docstring.
        """


        # Assertion control:
        if DEV_ENABLE_ASSERTION:
            ...

        # Sorting if there are two or more cards in hand:
        if self.hand_count >= 2:

            # Sorting by suit priority (Hearts > Diamonds > Clubs > Spades):
            if sort_method == VAR_SESSION_SORT_METHOD_SUIT:
                pass

            # Sorting by value:
            elif sort_method == VAR_SESSION_SORT_METHOD_VALUE:

                # Sorting by value (ignoring trump value):
                if ignore_trump:
                    pass

                # Sorting by value (default):
                else:
                    reverse_check: bool = True if not ascending_order else False
                    hand_sorted: list[Card] = sorted(
                        self.hand_container,
                        key = lambda card_object: card_object.card_type_value,
                        reverse = reverse_check,    # Highest left (default)
                        )

            # Sorting by time added to hand:
            elif sort_method == VAR_SESSION_SORT_METHOD_ADDED:
                reverse_check: bool = True if ascending_order else False
                hand_sorted: list[Card] = sorted(
                    self.hand_container,
                    key = lambda card_object: card_object.position_added,
                    reverse = reverse_check,        # First left (default)
                    )
            
            # Updating container:
            self.__hand_container: list[Card] = hand_sorted

            # Clearing cache:
            self.__clear_cached_property_list(
                target_list = self.__cached_hand_property_list
                )





    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ADD/REMOVE CARD METHODS BLOCK

    """


    def add_card(self, card_object: Card, update_container: bool = True) -> None:
        """
        TODO: Create a docstring.
        """
        
        # Assertion control:
        if DEV_ENABLE_ASSERTION:
            ... # TODO

        # Checking if card already exists in the container:
        if card_object not in self.hand_container:

            # Updating card position:
            card_position: int = self.hand_count
            card_object.set_position_hand(
                position_index = card_position,
                update_related = True
                )
            
            # Adding card to the list:
            self.__hand_container.append(
                card_object
                )

            # Clearing cache:
            ... # TODO:

            # Updating hand container (if required):
            if update_container:
                ... # TODO

    
    def remove_card(self, card_object: Card, update_container: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:
            ... # TODO

        # Checking if card exists in the container:
        if card_object in self.hand_container:

            # Updating card position:
            card_object.reset_position()

            # Removing card from the list:
            self.__hand_container.remove(
                card_object
                )
            
            # Clearing cache:
            ...

            # Updating hand container (if required):
            if update_container:
                ... # TODO

