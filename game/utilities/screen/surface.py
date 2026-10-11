# Cache management:
from functools import cached_property

# Various utilities:
from game.utilities.screen import area


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    SURFACE CLASS OBJECT CONSTRUCTOR
    
"""


class Surface:
    
    
    def __init__(self) -> None:
        
        # Area attributes:
        self.__area_player: area.Area = area.AREA_PLAYER
        self.__area_player_info: area.Area = area.AREA_PLAYER_INFO
        self.__area_opponent: area.Area = area.AREA_OPPONENT
        self.__area_opponent_info: area.Area = area.AREA_OPPONENT_INFO
        self.__area_deck: area.Area = area.AREA_DECK
        self.__area_deck_container: area.Area = area.AREA_DECK_CONTAINER
        self.__area_deck_info: area.Area = area.AREA_DECK_INFO
        self.__area_discard: area.Area = area.AREA_DISCARD
        self.__area_discard_info: area.Area = area.AREA_DISCARD_INFO
        self.__area_table: area.Area = area.AREA_TABLE
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED AREA PROPERTIES AND METHODS
    
    """
        
        
    @cached_property
    def __area_list(self) -> tuple[area.Area, ...]:
        """
        A list of all `area.Area` objects stored in the `Surface` class instance. Internal use only, inaccessible outside its class.
        
        Used to validate `set_area_focus()` parameter and to mass render all debug areas on screen.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        area_list : `tuple[Area, ...]`
            A list of all `area.Area` objects stored in the `Surface` class instance.
        """
        
        # Collecting areas:
        area_list: tuple[area.Area, ...] = (
            self.__area_player,
            self.__area_player_info,
            self.__area_opponent,
            self.__area_opponent_info,
            self.__area_deck_container,
            self.__area_deck,
            self.__area_deck_info,
            self.__area_discard,
            self.__area_table,
            self.__area_discard_info,
            )
        
        # Returning:
        return area_list


    @cached_property
    def __area_ino_list(self) -> tuple[area.Area, ...]:

        # Collecting area objects:
        area_info_list: tuple[area.Area, ...] = (
            self.__area_player_info,
            self.__area_opponent_info,
            self.__area_deck_info,
            self.__area_discard_info,
            )

        # Returning:
        return area_info_list
        
    
    @cached_property
    def __area_render_order(self) -> tuple[area.Area, ...]:
        
        # Collecting areas:
        area_list: tuple[area.Area, ...] = (
            self.__area_player,
            self.__area_player_info,
            self.__area_opponent,
            self.__area_opponent_info,
            self.__area_deck,
            self.__area_deck_container,
            self.__area_deck_info,
            self.__area_discard,
            self.__area_discard_info,
            self.__area_table,
            )
        
        # Returning:
        return area_list
    
    
    @cached_property
    def area_player(self) -> area.Area:
        """
        Player `area.Area` object. Used to determine area boundaries for cards and cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_player : `area.Area`
            Player `area.Area` object.
        """
        
        # Returning:
        return self.__area_player
    
    
    @cached_property
    def area_player_info(self) -> area.Area:
        """
        Player info `area.Area`` object. Used to determine area boundaries for cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_player_info : `area.Area`
            Player info `area.Area` object.
        """
        
        # Returning:
        return self.__area_player_info


    @cached_property
    def area_opponent(self) -> area.Area:
        """
        Opponent (hand) `area.Area` object. Used to determine area boundaries for cards and cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_opponent : `area.Area`
            Opponent `area.Area` object.
        """

        # Returning:
        return self.__area_opponent
    
    
    @cached_property
    def area_opponent_info(self) -> area.Area:
        """
        Opponent info `area.Area` object. Used to determine area boundaries for cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_opponent_info : `area.Area`
            Opponent info `area.Area` object.
        """

        # Returning:
        return self.__area_opponent_info


    @cached_property
    def area_deck(self) -> area.Area:
        """
        Deck `area.Area` object. Used to determine area boundaries for cards and cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_deck : `area.Area`
            Deck `area.Area` object.
        """
        
        # Returning:
        return self.__area_deck
    
    
    @cached_property
    def area_deck_container(self) -> area.Area:
        """
        Deck container `area.Area` object. Used to determine area boundaries for cards and cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_table : `area.Area`
            Deck container `area.Area` object.
        """

        # Returning:
        return self.__area_deck_container
    
    
    @cached_property
    def area_deck_info(self) -> area.Area:
        """
        Deck info `area.Area` object. Used to determine area boundaries for cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_deck_info : `area.Area`
            Deck info `area.Area` object.
        """
        
        # Returning:
        return self.__area_deck_info


    @cached_property
    def area_discard(self) -> area.Area:
        """
        Discard `area.Area` object. Used to determine area boundaries for cards and cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_discard : `area.Area`
            Discard `area.Area` object.
        """

        # Returning:
        return self.__area_discard
    
    
    @cached_property
    def area_discard_info(self) -> area.Area:
        """
        Discard info `area.Area` object. Used to determine area boundaries for cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_discard_info : `area.Area`
            Discard info `area.Area` object.
        """
        
        # Returning:
        return self.__area_deck_info


    @cached_property
    def area_table(self) -> area.Area:
        """
        Table `area.Area` object. Used to determine area boundaries for cards and cursor on render surface.
        
        Cached with `functools` module's `cached_property`. Static, cannot be cleared.
        
        Returns
        ----------
        self.__area_table : `area.Area`
            Table `area.Area` object.
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


    def display_info(self) -> None:

        

