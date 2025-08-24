# Annotation import:
from __future__ import annotations

# Cache-related modules and scripts import:
from game.scripts import clear_cached_property
from functools import cached_property
from itertools import product

# Random library import:
import random

# Settings and variables import list:
from game.variables import *
from game.settings import *

# Developer session values:
from game.controllers.session import (
    DEV_ENABLE_ASSERTION,
    DEV_ENABLE_ECHO,
    )

# Assertion functions import:
from game.scripts import (
    assert_value_is_default,
    assert_value_is_valid_type,
    assert_value_in_valid_range,
    )

# Collections import:
from game.controllers.card import CardObject


class DiscardController:

    def __init__(self):
        
        self.__discard_container: list[CardObject]

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE PROPERTIES BLOCK
    
    TODO: Create a docstring.

    """


    @cached_property
    def __cached_discard_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g.: for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "discard_container",
            "discard_count",
            )
        
        # Returning:
        return cached_property_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    DISCARD METHODS AND PROPERTIES BLOCK
    
    TODO: Create a docstring.

    """


    @cached_property
    def discard_container(self) -> list[CardObject]:
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
    

    def clear_discard(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        self.__discard_container: list[CardObject] = []

        # Clearing cache:
        for cached_property in self.__cached_discard_property_list:
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ADD/REMOVE CARD METHODS BLOCK
    
    TODO: Create a docstring.

    """


    def add_card(self, card_object: CardObject) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating card's position:
        discard_position: int = self.discard_count
        card_object.set_position_discard(
            position_index = discard_position,
            update_related = True
            )
        
        # Adding card to container:
        self.__discard_container.append(
            card_object
            )
        
        # Clearing cache:
        for cached_property in self.__cached_discard_property_list:
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )