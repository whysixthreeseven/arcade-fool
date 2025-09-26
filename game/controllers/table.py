# Typing library import:
from typing import Any, Optional

# Random library:
import random

# Cache-related import:
from functools import cached_property

# Controllers import:
from game.controllers.card import Card_Object

# Settings import:
from game.settings import (
    
    # Related settings:
    TABLE_POSITION_MIN,
    TABLE_POSITION_MAX,
    TABLE_POSITION_RANGE,
    TABLE_STACK_BOTTOM_INDEX,
    TABLE_STACK_TOP_INDEX,
    TABLE_STACK_RANGE,
    TABLE_COORDINATE_CENTER_X,
    TABLE_COORDINATE_CENTER_Y,
    TABLE_COORDINATE_SHIFT_X,
    TABLE_COORDINATE_SHIFT_Y,
    TABLE_POSITION_GAP,

    # Card-related settings:
    CARD_TEXTURE_WIDTH_SCALED
    )

# Session global variables import:
from game.session import (
    SESSION_ENABLE_ASSERTION,
    SESSION_ENABLE_ECHO,
    )

# Scripts import:
from game.scripts.convert import (
    convert_attribute_to_repr
    )
from game.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list
    )


class Table_Controller:
    
    def __init__(self) -> None:

        # Core attributes:
        self.__table_map: dict[dict[int, Card_Object | None]] = {}


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def __cached_table_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "table_map",
            "table_container",
            "table_container_count",
            "table_container_top",
            "table_container_top_count",
            "table_container_bottom",
            "table_container_bottom_count",
            )
        
        # Returning:
        return cached_property_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    TABLE MAP METHODS AND PROPERTIES BLOCK
    
    """
    

    @cached_property
    def table_map(self) -> dict[dict[int, Card_Object | None]]:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__table_map
    

    @cached_property
    def table_container_top(self) -> list[Card_Object]:
        """
        TODO: Create a docstring.
        """

        # Collecting card objects:
        table_container: list[Card_Object] = []

        # Looping through position and stack index:
        for position_index in self.table_map:
            stack_index: str = TABLE_STACK_TOP_INDEX
            card_object: Card_Object | None = self.table_map[position_index][stack_index]

            # Adding to the container:
            if card_object is not None:
                table_container.append(
                    card_object
                    )
        
        # Returning:
        return table_container
    

    @cached_property
    def table_container_top_count(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        card_count: int = len(self.table_container_top)

        # Returning:
        return card_count
    

    @cached_property
    def table_container_bottom(self) -> list[Card_Object]:
        """
        TODO: Create a docstring.
        """

        # Collecting card objects:
        table_container: list[Card_Object] = []

        # Looping through position and stack index:
        for position_index in self.table_map:
            stack_index: str = TABLE_STACK_BOTTOM_INDEX
            card_object: Card_Object | None = self.table_map[position_index][stack_index]

            # Adding to the container:
            if card_object is not None:
                table_container.append(
                    card_object
                    )
        
        # Returning:
        return table_container
    

    @cached_property
    def table_container_bottom_count(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        card_count: int = len(self.table_container_bottom)

        # Returning:
        return card_count
    

    @cached_property
    def table_container(self) -> list[Card_Object]:
        """
        TODO: Create a docstring.
        """

        # Creating containers:
        table_container_all: list[Card_Object] = []
        table_container_list: tuple[list[Card_Object], ...] = (
            self.table_container_top,
            self.table_container_bottom,
            )
        
        # Collecting cards:
        for table_container in table_container_list:
            for card_object in table_container:
                table_container_all.append(
                    card_object
                    )
        
        # Returning:
        return table_container_all
    

    @cached_property
    def table_container_count(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Counting card objects:
        table_container_count: int = int(
            self.table_container_top_count + 
            self.table_container_bottom_count
            )
        
        # Returning:
        return table_container_count
    

    @cached_property
    def table_position_index(self) -> dict[int, dict[int, tuple[int, int]]]:
        """
        TODO: Create a docstring.

        Cached. Cannot be cleared.

        :return dict[int, dict[int, tuple[int, int]]]: ...
        """

        # Creating position index dictionary:
        table_position_index: dict = {
            position_index: {
                TABLE_STACK_BOTTOM_INDEX: None,
                TABLE_STACK_TOP_INDEX: None
                }
            for position_index in TABLE_POSITION_RANGE
            }

        # Calculating table initial variables:
        table_width: int = int(
            CARD_TEXTURE_WIDTH_SCALED * 6 +
            TABLE_POSITION_GAP * 5
            )
        table_coordinate_x_start: int = int(
            TABLE_COORDINATE_CENTER_X -
            table_width / 2
            )
        
        # Calculating starting coordinates:
        position_coordinate_x_gap: int = CARD_TEXTURE_WIDTH_SCALED + TABLE_POSITION_GAP
        position_coordinate_x: int = int(table_coordinate_x_start + CARD_TEXTURE_WIDTH_SCALED / 8)
        position_coordinate_y: int = TABLE_COORDINATE_CENTER_Y
        
        # Generating position index dictionary:
        for position_index in TABLE_POSITION_RANGE:
            for stack_index in (TABLE_STACK_BOTTOM_INDEX, TABLE_STACK_TOP_INDEX):

                # Shifting coordinates for top stack:
                if stack_index == TABLE_STACK_TOP_INDEX:
                    position_coordinate_x += TABLE_COORDINATE_SHIFT_X
                    position_coordinate_y += TABLE_COORDINATE_SHIFT_Y
                
                # Packing up:
                position_coordinates: tuple[int, int] = (
                    position_coordinate_x,
                    position_coordinate_y
                    )
                
                # Adding to the dictionary:
                table_position_index[position_index][stack_index] = position_coordinates
            
            # Adding gap:
            position_coordinate_x += position_coordinate_x_gap
        
        # Returning:
        return table_position_index
    

    def create_table(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Creating a new table map dictionary:
        table_map: dict[int, dict[int, Card_Object | None]] = {
            position_index: {
                TABLE_STACK_BOTTOM_INDEX: None,
                TABLE_STACK_TOP_INDEX: None
                }
            for position_index in TABLE_POSITION_RANGE
            }
        
        # Updating attribute:
        self.__table_map: dict[int, dict[int, Card_Object | None]] = table_map

        # Clearing cache (table):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_table_property_list
            )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ADD/REMOVE CARD METHODS AND PROPERTIES BLOCK
    
    """


    def add_card(self, 
                 card_object: Card_Object,
                 position_index: int, 
                 stack_index: int, 
                 reset_coordinates: bool = False,   # <- Insntaly moves card to new coordinates
                 ignore_assertion: bool = False     # <- Enable in debug mode, please
                 ) -> None:
        """
        TODO: Create a docstring.

        :param Card_Object card_object: ...
        :param int position_index: ...
        :param int stack_index: ...
        :param bool reset_coordinates: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        """

        # Assertion control:
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:
            ...

        # Adding card to table map:
        self.__table_map[position_index][stack_index] = card_object

        # Updating card object's position:
        card_object.set_position_table(
            position_index = position_index,
            stack_index = stack_index,
            ignore_assertion = ignore_assertion
            )
        
        # Acquiring coordinates containers:
        coordinates_map: dict[int, dict[int, tuple[int, int]]] = self.table_position_index
        coordinates_default: tuple[int, int] = coordinates_map[position_index][stack_index]
        coordinate_x_default, coordinate_y_default = coordinates_default
        coordinates_slide: tuple[int, int] = (
            coordinate_x_default + TABLE_COORDINATE_SHIFT_X,
            coordinate_y_default + TABLE_COORDINATE_SHIFT_Y
            )

        # Updating coordinates:
        card_object.set_coordinates_default(
            set_container = coordinates_default,
            ignore_assertion = ignore_assertion
            )
        card_object.set_coordinates_slide(
            set_container = coordinates_slide,
            ignore_assertion = ignore_assertion,
            )
        if reset_coordinates:
            card_object.set_coordinates_current(
                set_container = coordinates_default,
                ignore_assertion = ignore_assertion
                )

        # Resetting card attributes:
        card_object.reset_boundary()
        card_object.reset_state()

        # Clearing cache:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_table_property_list
            )
        
    
    def find_card(self, 
                  position_index: int, 
                  stack_index: int,
                  ignore_assertion: bool = False
                  ) -> Card_Object | None:
        """
        TODO: Create a docstring.
        
        :param int position_index: ...
        :param int stack_index: ...
        :param bool ignore_assertion: ...

        :return Card_Object: ...
        :return None: ...
        """

        # Assertion control:
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:
            ...

        # Acquiring card object (or None):
        card_object: Card_Object | None = self.table_map[position_index][stack_index]

        # Returning:
        return card_object
        
    
    def find_empty_position(self) -> int | None:
        """
        TODO: Create a docstring.
        """

        # Finding empty position by looping through all positions at bottom stack:
        empty_position_index: int | None = None
        stack_index: int = TABLE_STACK_BOTTOM_INDEX
        for position_index in self.table_map:

            # Acquiring object (or None) and evaluating:
            card_object: Card_Object | None = self.table_map[position_index][stack_index]
            if card_object is None:
                empty_position_index: int = position_index
                break
        
        # Returning:
        return empty_position_index


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    RENDER METHODS AND PROPERTIES BLOCK

    """


    def render(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Collecting and ordering card containers:
        card_container_list: tuple[tuple[Card_Object], ...] = (
            self.table_container_bottom, 
            self.table_container_top
            )
        
        # Rendering cards in order:
        for card_container in card_container_list:
            for card_object in card_container:
                card_object.render()
