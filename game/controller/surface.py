# Arcade library:
import arcade
from arcade import Rect, Text, Texture, XYWH

# Cache management:
from functools import cached_property
from game.utilities.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list,
    refresh_object,
    )

# Settings and session instances:
from game.settings import SETTINGS
from game.session import SESSION

# Area objects:
from game.utilities.area import Area, AREA_PLAYER, AREA_OPPONENT, AREA_DECK, AREA_DISCARD, AREA_TABLE


class SurfaceController:
    
    
    def __init__(self) -> None:
        
        # Area attributes:
        self.__area_player: Area = AREA_PLAYER
        self.__area_opponent: Area = AREA_OPPONENT
        self.__area_deck: Area = AREA_DECK
        self.__area_discard: Area = AREA_DISCARD
        self.__area_table: Area = AREA_TABLE
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_area_attributes(self) -> tuple[str, ...]:
        
        # Collecting area attributes:
        cached_area_attributes: tuple[str, ...] = (
            "__area_player",
            "__area_opponent",
            "__area_deck",
            "__area_discard",
            "__area_table",
            )
        
        # Returning:
        return cached_area_attributes
    
    
    def clear_cached_area_attributes(self) -> None:
        
        # Clearing cached area attributes:
        clear_cached_property_list(
            target_object = self, 
            target_attribute_list = self.__cached_area_attributes
            )
        
    
    def clear_cached_attributes(self) -> None:
        
        # Collecting cached attributes:
        cached_property_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_area_attributes,
            )
        
        # Clearing cached attributes:
        for cached_property_list in cached_property_collection:
            clear_cached_property_list(
                target_object = self, 
                target_attribute_list = cached_property_list
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED AREA PROPERTIES AND METHODS
    
    """
        
        
    @cached_property
    def __area_list(self) -> tuple[Area, ...]:
        
        # Collecting areas:
        area_list: tuple[Area, ...] = (
            self.__area_player,
            self.__area_opponent,
            self.__area_deck,
            self.__area_discard,
            self.__area_table,
            )
        
        # Returning:
        return area_list
    
    
    @cached_property
    def area_player(self) -> Area:
        
        # Returning:
        return self.__area_player


    @cached_property
    def area_opponent(self) -> Area:

        # Returning:
        return self.__area_opponent


    @cached_property
    def area_deck(self) -> Area:

        # Returning:
        return self.__area_deck


    @cached_property
    def area_discard(self) -> Area:

        # Returning:
        return self.__area_discard


    @cached_property
    def area_table(self) -> Area:

        # Returning:
        return self.__area_table
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SURFACE CACHED PROPERTIES AND METHODS
    
    """
    
    
    # TODO: Implement!
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        LOCATE METHODS
    
    """
    
    
    def locate_area(self, coordinates: tuple[int, int], ignore_assertion: bool = False) -> Area | None:
        
        # Unpacking coordinates:
        for area in self.__area_list:
            area_hit: bool = area.hit_boundary(
                check_coordinates = coordinates,
                ignore_assertion = ignore_assertion
                )
            
            # Returning area on hit and exiting:
            if area_hit:
                return area
        
        # Nothing hit any of the boundaries:
        else:
            
            # Raising error, if enabled:
            if SESSION.ENABLE_DEBUG:
                error_message: str = f"Coordinates {coordinates} do not belong to any area."
                raise ValueError(error_message)
            
            # Otherwise returning None:
            return None

    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DISPLAY METHODS
    
    """
    
    
    def display_area(self, area_object: Area) -> None:
        
        # TODO: Implement:
        ...
        
        # Calling display method:
        area_object.display()
    
    
    def display_all(self) -> None:
        
        # TODO: Implement
        ...
        
        # Calling display method for all areas:
        if SESSION.ENABLE_DEBUG:
            for area in self.__area_list:
                area.display()

