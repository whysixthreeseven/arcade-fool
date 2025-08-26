# Annotation import:
from __future__ import annotations

# Cache-related modules and scripts import:
from game.scripts import clear_cached_property
from functools import cached_property

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


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
TABLE CONTROLLER BLOCK

"""


class TableController:


    def __init__(self) -> None:
        
        # Core attribute:
        self.__table_map: dict[int, dict[int, CardObject | None]] = {}
        self.__setup_table_map()


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    SETUP METHODS BLOCK

    """


    def __setup_table_map(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Creating nested dictionary:
        table_container: dict[int, dict[int, CardObject | None ]] = {
            position_index: {
                stack_index: None 
                for stack_index in range(TABLE_STACK_TOP_INDEX + 1)
                }
            for position_index in range(TABLE_POSITION_COUNT_MAX)
            }
        
        # Updating attribute:
        self.__table_map = table_container

        # Clearing cache:
        self.__clear_cached_property_list(
            target_list = self.__cached_table_property_list,
            )


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
    def __cached_table_property_list(self) -> tuple[str, ...]:
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
            "table_map",
            "table_container",
            "table_container_bottom",
            "table_container_top",
            "table_count",
            "table_empty_position",
            )
        
        # Returning:
        return cached_property_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    TABLE METHODS AND PROPERTIES BLOCK

    """

    
    @cached_property
    def table_map(self) -> dict[int, dict[int, CardObject | None]]:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__table_map
    

    @cached_property
    def table_container(self) -> tuple[CardObject, ...]:
        """
        TODO: Create a docstring.
        """

        # Creating empty card list:
        card_list: list[CardObject] = []

        # Scanning all positions:
        for position_index in self.table_map:
            for stack_index in self.table_map[position_index]:
                card_object: CardObject | None = self.table_map[position_index][stack_index]

                # If card object is not None, adding to list:
                if card_object is not None:
                    card_list.append(
                        card_object
                        )
        
        # Converting:
        card_list_converted: tuple[CardObject, ...] = tuple(card_list)

        # Returning:
        return card_list_converted


    @cached_property
    def table_container_bottom(self) -> tuple[CardObject, ...]:
        """
        TODO: Create a docstring.
        """

        # Creating an empty tuple container (if no cards are available)
        card_list: tuple[CardObject, ...] = tuple()

        # Gathering only bottom stacked cards:
        if self.table_count > 0 :
            card_list: tuple[CardObject, ...] = tuple(
                card_object for card_object
                in self.table_container
                if card_object.position_stack == TABLE_STACK_BOTTOM_INDEX
                )
        
        # Returning:
        return card_list
    

    @cached_property
    def table_container_top(self) -> tuple[CardObject, ...]:
        """
        TODO: Create a docstring.
        """

        # Creating an empty tuple container (if no cards are available)
        card_list: tuple[CardObject, ...] = tuple()

        # Gathering only bottom stacked cards:
        if self.table_count > 0 :
            card_list: tuple[CardObject, ...] = tuple(
                card_object for card_object
                in self.table_container
                if card_object.position_stack == TABLE_STACK_TOP_INDEX
                )
        
        # Returning:
        return card_list
    

    @cached_property
    def table_count(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Counting:
        table_count: int = len(self.table_container)

        # Returning:
        return table_count
    

    @cached_property
    def table_position_index(self) -> dict[int, dict[int, tuple[int, int]]]:
        """
        TODO: Create a docstring.

        Cached. Cannot be removed.
        """

        # Creating empty position index dictionary:
        table_position_index: dict[int, dict[int, tuple[int, int]]] = {}

        # Calculating start coordinates:
        table_coordinate_x_start = int(TABLE_COORDINATE_X - TABLE_WIDTH / 2)
        position_index_coordinate_x_start: int = int(
            table_coordinate_x_start + CARD_TEXTURE_WIDTH_SCALED / 2
            )
        
        # Cycling through position and stack indexes:
        for position_index in self.table_map:
            if position_index not in table_position_index.keys():
                table_position_index[position_index] = {}
            for stack_index in self.table_map[position_index]:

                # Generating coordinates:
                card_coordinate_x: int = int(
                    position_index_coordinate_x_start +
                    (CARD_TEXTURE_WIDTH_SCALED + TABLE_POSITION_MARGIN) * position_index
                    )
                card_coordinate_y: int = TABLE_COORDINATE_Y

                # Adjusting coordinates if stack is on top
                if stack_index == TABLE_STACK_TOP_INDEX:
                    card_coordinate_x: int = card_coordinate_x + TABLE_STACK_SHIFT_X
                    card_coordinate_y: int = TABLE_COORDINATE_Y + TABLE_STACK_SHIFT_Y
                
                # Packing up and adding to position index dictionary:
                card_coordinates: tuple[int, int] = (card_coordinate_x, card_coordinate_y)
                table_position_index[position_index][stack_index] = card_coordinates
        
        # Returning:
        return table_position_index
    

    @cached_property
    def table_empty_position(self) -> int:
        """
        TODO: Create a docstring.
        """
        
        # Cycling through available positions on table:
        table_empty_position: int = 0
        for position_index in self.table_map:
            card_object: CardObject | None = self.get_card_by_position(
                position_index   = position_index,
                stack_index      = TABLE_STACK_BOTTOM_INDEX,
                ignore_assertion = True
                )
            
            # If position is empty, stopping:
            if card_object is None:
                table_empty_position: int = position_index
                break
        
        # Returning:
        return table_empty_position


    def clear_table(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Cleaning table positions (resetting to None):
        for position_index in self.__table_map:
            for stack_index in self.__table_map[position_index]:
                self.__table_map[position_index][stack_index] = None
    
        # Clearing cache:
        self.__clear_cached_property_list(
            target_list = self.__cached_table_property_list,
            )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ADD/REMOVE CARD METHODS BLOCK

    """


    def add_card(self, 
                 card_object: CardObject, 
                 position_index: int, 
                 stack_index: int,
                 ignore_assertion: bool = False
                 ) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:
            
            # Asserting position index is valid type:
            valid_type: type = CardObject
            assert_value_is_valid_type(
                check_value = card_object,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting position index is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = position_index,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting position index in within valid range:
            valid_range: range = range(0, TABLE_POSITION_COUNT_MAX)
            assert_value_in_valid_range(
                check_value = position_index,
                valid_range = valid_range,
                raise_error = True
                )
            
            # Asserting stack index is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = stack_index,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting stack index in within valid range:
            valid_list: tuple[int, int] = (
                TABLE_STACK_BOTTOM_INDEX,
                TABLE_STACK_TOP_INDEX,
                )
            assert_value_is_default(
                check_value = stack_index,
                valid_range = valid_list,
                raise_error = True
                )

        # Adding card object ot the dictionary:
        if card_object not in self.table_container:
            self.__table_map[position_index][stack_index] = card_object

            # Updating card object's position:
            card_object.set_position_table(
                position_index = position_index,
                stack_index    = stack_index,
                update_related = True
                )
            
            # Updating card object's coordinates:
            table_position_index: dict[int, dict[int, tuple[int, int]]] = self.table_position_index
            card_coordinates: tuple[int, int] = table_position_index[position_index][stack_index]
            card_object.set_coordinates(
                set_value = card_coordinates
                )
            
    
    def remove_card(self, card_object: CardObject, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:
            
            # Asserting position index is valid type:
            valid_type: type = CardObject
            assert_value_is_valid_type(
                check_value = card_object,
                valid_type  = valid_type,
                raise_error = True,
                )

        # Checking if card exists:
        if card_object in self.table_container:

            # Acquiring position and stack indexes:
            position_index: int = card_object.position_table
            stack_index: int = card_object.position_stack

            # Removing card from dictionary:
            self.__table_map[position_index][stack_index] = None

            # Updating card positions:
            card_object.reset_position()

    
    def get_card_by_position(self, 
                             position_index: int, 
                             stack_index: int, 
                             ignore_assertion: bool = False
                             ) -> CardObject:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:
            
            # Asserting position index is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = position_index,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting position index in within valid range:
            valid_range: range = range(0, TABLE_POSITION_COUNT_MAX)
            assert_value_in_valid_range(
                check_value = position_index,
                valid_range = valid_range,
                raise_error = True
                )
            
            # Asserting stack index is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = stack_index,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting stack index in within valid range:
            valid_list: tuple[int, int] = (
                TABLE_STACK_BOTTOM_INDEX,
                TABLE_STACK_TOP_INDEX,
                )
            assert_value_is_default(
                check_value = stack_index,
                valid_range = valid_list,
                raise_error = True
                )

        # Acquiring object:
        card_object: CardObject | None = self.table_position_index[position_index][stack_index]

        # Returning:
        return card_object        
