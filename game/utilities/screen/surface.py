# Settings, session and context:
from game.session import SESSION

# Cache management:
from functools import cached_property
from game.utilities.scripts import cache

# Various utilities:
from game.utilities.screen import area


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    SURFACE CLASS OBJECT CONSTRUCTOR
    
"""


class Surface:
    
    
    def __init__(self) -> None:
        
        # Area attributes:
        self.__area_player: area.Area = area.AREA_PLAYER
        self.__area_opponent: area.Area = area.AREA_OPPONENT
        self.__area_deck_container: area.Area = area.AREA_DECK_CONTAINER
        self.__area_deck: area.Area = area.AREA_DECK
        self.__area_discard: area.Area = area.AREA_DISCARD
        self.__area_table: area.Area = area.AREA_TABLE
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED AREA PROPERTIES AND METHODS
    
    """
        
        
    @cached_property
    def __area_list(self) -> tuple[area.Area, ...]:
        """
        A list of all `Area` objects stored in the `Surface` class instance. Internal use only, inaccessible outside its class.
        
        Used to validate `set_area_focus()` parameter and to mass render all debug areas on screen.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        area_list : `tuple[Area, ...]`
            A list of all `Area` objects stored in the `Surface` class instance.
        """
        
        
        # Collecting areas:
        area_list: tuple[area.Area, ...] = (
            self.__area_player,
            self.__area_opponent,
            self.__area_deck_container,
            self.__area_deck,
            self.__area_discard,
            self.__area_table,
            )
        
        # Returning:
        return area_list
    
    
    @cached_property
    def __area_render_order(self) -> tuple[area.Area, ...]:
        
        # Collecting areas:
        area_list: tuple[area.Area, ...] = (
            self.__area_player,
            self.__area_opponent,
            self.__area_deck,
            self.__area_deck_container,
            self.__area_discard,
            self.__area_table,
            )
        
        # Returning:
        return area_list
    
    
    @cached_property
    def area_player(self) -> area.Area:
        """
        Player `Area` object. Used to determine area boundaries for cards and cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_player : `Area`
            Player `Area` object.
        """
        
        # Returning:
        return self.__area_player


    @cached_property
    def area_opponent(self) -> area.Area:
        """
        Opponent (hand) `Area` object. Used to determine area boundaries for cards and cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_opponent : `Area`
            Opponent `Area` object.
        """

        # Returning:
        return self.__area_opponent


    @cached_property
    def area_deck(self) -> area.Area:
        """
        Deck `Area` object. Used to determine area boundaries for cards and cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_deck : `Area`
            Deck `Area` object.
        """
        
        # Returning:
        return self.__area_deck
    
    
    @cached_property
    def area_deck_container(self) -> area.Area:
        """
        Deck container `Area` object. Used to determine area boundaries for cards and cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_table : `Area`
            Deck container `Area` object.
        """

        # Returning:
        return self.__area_deck_container


    @cached_property
    def area_discard(self) -> area.Area:
        """
        Discard `Area` object. Used to determine area boundaries for cards and cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_discard : `Area`
            Discard `Area` object.
        """

        # Returning:
        return self.__area_discard


    @cached_property
    def area_table(self) -> area.Area:
        """
        Table `Area` object. Used to determine area boundaries for cards and cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_table : `Area`
            Table `Area` object.
        """

        # Returning:
        return self.__area_table
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        LOCATE METHODS
    
    """
    
    
    def locate_area(self, coordinates: tuple[int, int], ignore_assertion: bool = False) -> area.Area | None:
        
        # Preparing variables:
        area_located: area.Area | None = None
        
        # Unpacking coordinates:
        for area_stored in self.__area_list:
            area_hit: bool = area_stored.hit_boundary(
                hit_coordinates = coordinates,
                ignore_assertion = ignore_assertion
                )
            
            # Returning area on hit and exiting:
            if area_hit:
                area_located: area.Area = area_stored
                break
        
        # Returning:
        return area_located
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DISPLAY METHODS
    
    """
    
    
    def display_area(self, area_object: area.Area) -> None:
        
        # TODO: Implement:
        ...
        
        # Calling display method:
        area_object.display()
    
    
    def display_debug(self) -> None:
        
        # TODO: Implement
        ...
        
        # Calling display method for all areas:
        for area_object in self.__area_render_order:
            area_object.display()

