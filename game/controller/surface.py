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

# Assertion control:
from game.utilities.scripts.assertion import (
    assert_setter_entry,
    assert_value_type,
    assert_value_default,
    assert_value_ge_zero,
    assert_value_gt_zero,
    assert_value_not_empty,
    assert_value_in_range,
    )

# Area objects:
from game.utilities.area import (
    Area, 
    AREA_PLAYER, 
    AREA_OPPONENT, 
    AREA_DECK, 
    AREA_DISCARD, 
    AREA_TABLE
    )


class Surface:
    
    
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
            "area_focus",
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
        VALIDATE METHODS
    
    """
    
    
    def __validate_area(self, validate_value: Area) -> None:
        """
        Validates `Area` object.
        
        Uses `game.utilities.scripts.assertion` module's functions to validate. These functions raise `AssertionError` on failed
        validation attempt.
        
        Parameters
        ----------
        validate_value : `Area`
            `Area` object to validate.
        """
        
        
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = Area,
            raise_error = True,
            )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED AREA PROPERTIES AND METHODS
    
    """
        
        
    @cached_property
    def __area_list(self) -> tuple[Area, ...]:
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
    def area_opponent(self) -> Area:
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
    def area_deck(self) -> Area:
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
    def area_discard(self) -> Area:
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
    def area_table(self) -> Area:
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
    def area_focus(self) -> Area | None:
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
    
    
    def set_focus_area(self, set_value: Area | None, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
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
                self.__validate_area(
                    validate_value = set_value,
                    )
            
        # Updating attribute:
        self.__area_focus = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "area_focus"
            clear_cached_property(
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
    
    
    def display_debug(self) -> None:
        
        # TODO: Implement
        ...
        
        # Calling display method for all areas:
        for area_object in self.__area_list:
            area_object.display()

