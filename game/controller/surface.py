# Settings, session and context:
from game.session import SESSION

# Cache management:
from functools import cached_property
from game.utilities.scripts import cache

# Various utilities:
from game.utilities import area
from game.utilities.scripts import validate


class SurfaceController:
    
    
    def __init__(self) -> None:
        
        # Area attributes:
        self.__area_player: area.Area = area.AREA_PLAYER
        self.__area_opponent: area.Area = area.AREA_OPPONENT
        self.__area_deck: area.Area = area.AREA_DECK
        self.__area_discard: area.Area = area.AREA_DISCARD
        self.__area_table: area.Area = area.AREA_TABLE
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_area_attributes(self) -> tuple[str, ...]:
        
        # Collecting area attributes:
        cached_area_attributes: tuple[str, ...] = (
            "area_focus",
            )
        
        # Returning:
        return cached_area_attributes
    
    
    def clear_cached_area_attributes(self) -> None:
        
        # Clearing cached area attributes:
        cache.clear_cached_property_list(
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
            cache.clear_cached_property_list(
                target_object = self, 
                target_attribute_list = cached_property_list
                )
            
    
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
            self.__area_deck,
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
    
    
    @cached_property
    def area_focus(self) -> area.Area | None:
        """
        `Area` object user's cursor is currently in, or `None` if cursor is outside game window.
        
        Cached with `functools` module's `cached_property`. Can be cleared with `game.utilities.scripts.cache` module's function 
        `clear_cached_property()`, or by calling a native method related to cached property group.
        
        Returns
        ----------
        self.__area_focus : `Area`
            `Area` object user's cursor is currently in. `None`, if cursor is outside game window.
        """
        
        # Returning:
        return self.__area_focus
    
    
    def set_focus_area(self, set_value: area.Area | None, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        """
        Sets a new focus `Area` object for the `Surface` class instance. Can be `None`, if user's cursor is outsde game window.
        Uses only default variables provided by `game.utilities.area` module: `AREA_PLAYER`, `AREA_OPPONENT`, `AREA_DECK`, 
        `AREA_DISCARD`, and `AREA_TABLE`. Alternatively can point at existing attributes inside its class, e.g. 
        `self.__area_player`.
            
        This method may raise `AssertionError` if its validate method `self.__validate_area()` is unable to assert 
        parameter's validity. Its validation can be skipped if `SESSION.ENABLE_ASSERTION` is disabled or if parameter 
        `ignore_assertion` is flagged as `False`.
        
        Clears cached property `area_focus` if `clear_cache` is `True`.

        Parameters
        ----------
        set_value : `Area` | `None`
            The new `Area` object to set as focus. `None`, if cursor is outside game window.
        ignore_assertion : `bool` = `False`
            If `True`, will ignore assertion checks. `False` by default.
        """
        
        # Assertion control:
        if set_value is not None:
            if SESSION.ENABLE_ASSERTION and not ignore_assertion:
                validate.validate_area(
                    validate_value = set_value,
                    )
            
        # Updating attribute:
        self.__area_focus = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "area_focus"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property,
                )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SURFACE CACHED PROPERTIES AND METHODS
    
    """
    
    
    # TODO: Implement!
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        LOCATE METHODS
    
    """
    
    
    def locate_area(self, coordinates: tuple[int, int], ignore_assertion: bool = False) -> area.Area | None:
        
        # Preparing variables:
        area_located: area.Area | None = None
        
        # Unpacking coordinates:
        for area in self.__area_list:
            area_hit: bool = area.hit_boundary(
                hit_coordinates = coordinates,
                ignore_assertion = ignore_assertion
                )
            
            # Returning area on hit and exiting:
            if area_hit:
                area_located: area.Area = area
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
        for area_object in self.__area_list:
            area_object.display()

