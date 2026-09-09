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
    
    
    def display(self) -> None:
        
        # TODO: Implement
        ...
        
        if SESSION.ENABLE_DEBUG:
            for area in self.__area_list:
                area.display()

