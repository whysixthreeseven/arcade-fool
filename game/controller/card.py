# Typing and annotations:
from __future__ import annotations

# External libraries:
import arcade
import random
import pathlib

# Cache management:
from functools import cached_property
from game.utilities.scripts import cache

# Settings, session and context:
from game.common.settings import SETTINGS
from game.common.session import SESSION
from game.common.context import VAR 

# Namespace module
from game.common import namespace

# Utility modules:
from game.utilities.scripts import assertion, validation


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    CARD OBJECT CLASS CONSTRUCTOR

"""


class CardObject:

    def __init__(self) -> None:

        # Core attribute:
        self.__name: str = None
        self.__suit: str = None
        self.__trump: bool = False

        # Sprite attribute:
        self.__arcadesprite: arcade.Sprite = None

        # State attributes:
        self.__state_hovered: bool = None
        self.__state_selected: bool = None
        self.__state_playable: bool = None
        self.__state_controlled: bool = None
        self.__state_showcase: bool = None

        # Coordinates attributes:
        self.__coordinate_x_current: float = None
        self.__coordinate_y_current: float = None
        self.__coordinate_x_expected: float = None
        self.__coordinate_y_expected: float = None
        self.__coordinate_x_position: float = None
        self.__coordinate_y_position: float = None
        self.__coordinate_x_hover: float = None
        self.__coordinate_y_hover: float = None
        self.__coordinate_x_select: float = None
        self.__coordinate_y_select: float = None

        # Render attributes:
        self.__render_tilt_current: int = None
        self.__render_alpha_current: int = None
        self.__render_scale_current: int = None


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        NATIVE METHODS OVERRIDE
    
    """


    def __repr__(self) -> str:
        """
        Card object's representation method. Formats card object to be displayed in the console.

        Returns:
            card_repr (`str`): Card object's representation.
        """

        # Formatting card string:
        card_repr: str = f"{self.suit_ascii}{self.name_ascii}"

        # Returning:
        return card_repr


    def __str__(self) -> str:
        """
        Card object's string method. Formats card object to be displayed in the console.

        Returns:
            card_str (`str`): Card object's string.
        """

        # Formatting card string:
        card_string: str = f"{self.suit_ascii}{self.name_ascii}"

        # Returning:
        return card_string


    def __gt__(self, other: CardObject) -> bool:
        """
        Card object's greater than method. Compares card object's value with another card object's value if both are of same suit
        or this card object is trump.

        Parameters:
            other (`CardObject`): Other card object to compare with.

        Returns:
            gt_check (`bool`): Card object's greater than check.
        """

        # Evaluating:
        gt_check: bool = bool(
            self.suit == other.suit and self.value > other.value
                or self.trump and self.value > other.value
            )

        # Returning:
        return gt_check


    def __lt__(self, other: CardObject) -> bool:
        """
        Card object's less than method. Compares card object's value with another card object's value if both are of same suit
        or the other card object is trump.

        Parameters:
            other (`CardObject`): Other card object to compare with.

        Returns:
            lt_check (`bool`): Card object's less than check.
        """

        # Evaluating:
        lt_check: bool = bool(
            self.suit == other.suit and self.value < other.value
                or other.trump and self.value < other.trump
            )

        # Returning:
        return lt_check



    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        NAME CACHED PROPERTIES AND METHODS
    
    """


    @cached_property
    def name(self) -> str:
        """
        Card object's default name property.

        Returns:
            self.__name (`str`): Card object's name.
        """

        # Returning:
        return self.__name


    @cached_property
    def name_repr(self) -> str:
        """
        Card object's name representation property. Formats name property to be displayed in the game.

        Returns:
            name_repr (`str`): Card object's name representation.
        """

        # Formatting name string:
        name_repr: str = self.__name.capitalize()

        # Returning:
        return name_repr


    @cached_property
    def name_ascii(self) -> str:
        """
        Card object's name ASCII representation property. Selects ASCII character from `game.common.context` module's `VAR`.

        Returns:
            name_ascii (`str`): Card object's name ASCII representation.
        """

        # Selecting name ASCII char:
        name_ascii: str = VAR.CARD.NAME_ASCII.BY_NAME[self.__name]

        # Returning:
        return name_ascii


    def set_name(
            self,
            set_value: str,
            ignore_assertion: bool = False,
            clear_cache: bool = True,
            ) -> None:
        """
        Set new name property for card object. Only default values found in `game.common.context` module's `VAR` are allowed.

        Parameters:
            set_value (`str`): New name value to set.
            ignore_assertion (`bool`, optional): Ignore assertion control. Defaults to `False`.
            clear_cache (`bool`, optional): Clear cached properties. Defaults to `True`.
        
        Raises:
            AssertionError: If assertion control is enabled and `set_value` is not a valid card name.
            AttributeError: If card object's name was already set.
        """

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            custom_error: str = f"Invalid card name set value: <{set_value}>. Use default list in `game.common.context` module."
            validation.validate_card_name(
                validate_value = set_value,
                custom_error = custom_error,
                )

        # Checking if attribute was set before:
        if SESSION.DEBUG.ENABLE_DEBUG:
            if self.__name is not None:
                error_message: str = f"Card object's name was already set to: <{self.__name}>. Attempting to overwrite?"
                raise AttributeError(error_message)

        # Updating attribute:
        self.__name = set_value

        # Clearing cache, if required:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "name",
                "name_repr",
                "name_ascii",
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list,
                )


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SUIT CACHED PROPERTIES AND METHODS
    
    """


    @cached_property
    def suit(self) -> str:
        """
        Card object's default suit property.

        Returns:
            self.__suit (`str`): Card object's suit.
        """

        # Returning:
        return self.__suit


    @cached_property
    def suit_repr(self) -> str:
        """
        Card object's suit representation property. Formats suit property to be displayed in the game.

        Returns:
            suit_repr (`str`): Card object's suit representation.
        """

        # Formatting suit string:
        suit_repr: str = self.__suit.capitalize()

        # Returning:
        return suit_repr


    @cached_property
    def suit_ascii(self) -> str:
        """
        Card object's suit ASCII representation property. Selects ASCII character from `game.common.context` module's `VAR`.

        Returns:
            suit_ascii (`str`): Card object's suit ASCII representation.
        """

        # Selecting suit ASCII char:
        suit_ascii: str = VAR.CARD.SUIT_ASCII.BY_SUIT[self.__suit]

        # Returning:
        return suit_ascii


    def set_suit(
            self,
            set_value: str,
            ignore_assertion: bool = False,
            clear_cache: bool = True,
            ) -> None:
        """
        Set new suit property for card object. Only default values found in `game.common.context` module's `VAR` are allowed.

        Parameters:
            set_value (`str`): New suit value to set.
            ignore_assertion (`bool`, optional): Ignore assertion control. Defaults to `False`.
            clear_cache (`bool`, optional): Clear cached properties. Defaults to `True`.

        Raises:
            AssertionError: If assertion control is enabled and `set_value` is not a valid card suit.
            AttributeError: If card object's suit was already set.
        """

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            custom_error: str = f"Invalid card suit set value: <{set_value}>. Use default list in `game.common.context` module."
            validation.validate_card_suit(
                validate_value = set_value,
                custom_error = custom_error,
                )

        # Checking if attribute was set before:
        if SESSION.DEBUG.ENABLE_DEBUG:
            if self.__suit is not None:
                error_message: str = f"Card object's suit was already set to: <{self.__suit}>. Attempting to overwrite?"
                raise AttributeError(error_message)

        # Updating attribute:
        self.__suit = set_value

        # Clearing cache, if required:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "suit",
                "suit_repr",
                "suit_ascii",
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list,
                )


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        TRUMP FLAG SET & ADJUST METHODS
    
    """


    @property
    def trump(self) -> bool:
        """
        Card object's trump flag property.

        Returns:
            self.__trump (`bool`): Card object's trump flag.
        """

        # Returning:
        return self.__trump


    def set_trump(
            self,
            set_value: bool,
            ignore_assertion: bool = False,
            clear_cache: bool = True,
            ) -> None:
        """
        Set new trump flag property for card object.

        Parameters:
            set_value (`bool`): New trump flag value to set.
            ignore_assertion (`bool`, optional): Ignore assertion control. Defaults to `False`.
            clear_cache (`bool`, optional): Clear cached properties. Defaults to `True`.

        Raises:
            AssertionError: If assertion control is enabled and `set_value` is not a valid boolean value.
        """

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            validation.validate_flag(
                validate_value = set_value,
                custom_error = None,
                )

        # Updating attribute:
        self.__trump = set_value

        # Clearing cache, if required:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "trump",
                "value",
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list,
                )


    def switch_trump(self) -> None:
        """
        Switch card object's trump flag property value.
        """

        # Switching:
        self.__trump = not self.__trump


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        VALUE CACHED PROPERTIES AND METHODS
    
    """


    @cached_property
    def value_base(self) -> int:
        """
        Card object's base value.

        Returns:
            card_value_base (`int`): Card object's base value.
        """

        # Acquiring value
        card_value_base: int = VAR.CARD.VALUE.BY_NAME[self.__name]

        # Returning:
        return card_value_base


    @cached_property
    def value(self) -> int:
        """
        Card object's value. Used to compare cards of the same suit and determine container's total value.

        Returns:
            card_value (`int`): Card object's value (including trump bonus, if card suit is trump).
        """

        # Acquring value:
        card_value: int = VAR.CARD.VALUE.BY_NAME[self.__name]

        # Adding trump value modifier, if card suit is trump:
        if self.__trump:
            card_value =  card_value + VAR.CARD.VALUE.TRUMP_BONUS

        # Returning:
        return card_value


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COORDINATES SET & ADJUST METHODS
    
    """


    def __set_coordinate_x(
            self, 
            set_value: float, 
            set_target: namespace.CoordinatesType, 
            ignore_assertion: bool = False, 
            ) -> None:
        """
        Set a new coordinate x for one of the coordinate types stored in this class.

        Constructs attribute name to get and set with `target_attribute: str = f"_CardObject__coordinate_x_{set_target}"`, therefore
        `set_target` parameter must be a valid `namespace.CoordinatesType` value (default).

        Used by named setter methods.

        Parameters:
            set_value (`float`): New coordinate x value to set.
            set_target (`Literal["current", "position", "expected", "hover", "select"]`): Target coordinate type to set 
                coordinate x for.
            ignore_assertion (`bool`, optional): Ignore assertion control. Defaults to `False`.

        Raises:
            AssertionError: If assertion control is enabled and `set_value` is not a valid coordinate value.
        """

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            validation.validate_coordinate(
                validate_value = set_value,
                custom_error = None,
                )

        # Updating attribute:
        target_attribute: str = f"_CardObject__coordinate_x_{set_target}"
        setattr(self, target_attribute, set_value)


    def __adjust_coordinate_x(
            self,
            adjust_value: float,
            adjust_target: namespace.CoordinatesType,
            ignore_assertion: bool = False,
            ) -> None:
        """
        Adjust a coordinate x for one of the coordinate types stored in this class.

        Constructs attribute name to get and set with `target_attribute: str = f"_CardObject__coordinate_x_{adjust_target}"`, therefore
        `adjust_target` parameter must be a valid `namespace.CoordinatesType` value (default).

        Used by named setter methods.

        Parameters:
            adjust_value (`float`): Value to adjust coordinate x by.
            adjust_target (`Literal["current", "position", "expected", "hover", "select"]`): Target coordinate type to adjust
                coordinate x for.
            ignore_assertion (`bool`, optional): Ignore assertion control. Defaults to `False`.

        Raises:
            AssertionError: If assertion control is enabled and `adjust_value` is not a valid coordinate value.
        """

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_is_valid_type(
                check_value = adjust_value,
                check_type = float,
                raise_error = True,
                custom_error = None
                )

        # Calculating new coordinate value:
        target_attribute: str = f"_CardObject__coordinate_x_{adjust_target}"
        set_value = getattr(self, target_attribute) + adjust_value

        # Updating attribute:
        self.__set_coordinate_x(
            set_value = set_value,
            set_target = adjust_target,
            ignore_assertion = ignore_assertion
            )


    def __set_coordinate_y(
            self, 
            set_value: float, 
            set_target: namespace.CoordinatesType, 
            ignore_assertion: bool = False, 
            ) -> None:
        """
        Set a new coordinate y for one of the coordinate types stored in this class.

        Constructs attribute name to get and set with `target_attribute: str = f"_CardObject__coordinate_y_{set_target}"`, therefore
        `set_target` parameter must be a valid `namespace.CoordinatesType` value (default).

        Used by named setter methods.

        Parameters:
            set_value (`float`): New coordinate y value to set.
            set_target (`Literal["current", "position", "expected", "hover", "select"]`): Target coordinate type to set 
                coordinate y for.
            ignore_assertion (`bool`, optional): Ignore assertion control. Defaults to `False`.

        Raises:
            AssertionError: If assertion control is enabled and `set_value` is not a valid coordinate value.
        """

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            validation.validate_coordinate(
                validate_value = set_value,
                custom_error = None,
                )

        # Updating attribute:
        target_attribute: str = f"_CardObject__coordinate_y_{set_target}"
        setattr(self, target_attribute, set_value)


    def __adjust_coordinate_y(
            self,
            adjust_value: float,
            adjust_target: namespace.CoordinatesType,
            ignore_assertion: bool = False,
            ) -> None:
        """
        Adjust a coordinate y for one of the coordinate types stored in this class.

        Constructs attribute name to get and set with `target_attribute: str = f"_CardObject__coordinate_y_{adjust_target}"`, therefore
        `adjust_target` parameter must be a valid `namespace.CoordinatesType` value (default).

        Used by named setter methods.

        Parameters:
            adjust_value (`float`): Value to adjust coordinate y by.
            adjust_target (`Literal["current", "position", "expected", "hover", "select"]`): Target coordinate type to adjust
                coordinate y for.
            ignore_assertion (`bool`, optional): Ignore assertion control. Defaults to `False`.

        Raises:
            AssertionError: If assertion control is enabled and `adjust_value` is not a valid coordinate value.
        """

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_is_valid_type(
                check_value = adjust_value,
                check_type = float,
                raise_error = True,
                custom_error = None
                )

        # Calculating new coordinate value:
        target_attribute: str = f"_CardObject__coordinate_y_{adjust_target}"
        set_value = getattr(self, target_attribute) + adjust_value

        # Updating attribute:
        self.__set_coordinate_y(
            set_value = set_value,
            set_target = adjust_target,
            ignore_assertion = ignore_assertion
            )


    def __set_coordinates(
            self,
            set_value: namespace.Coordinates,
            set_target: namespace.CoordinatesType,
            ignore_assertion: bool = False,
            ) -> None:
        """
        Set new coordinates for one of the coordinate types stored in this class.

        Unpacks coordinates provided with `set_value` and calls inner setter methods: `self.__set_coordinate_x()` and 
        `self.__set_coordinate_y()`.

        Parameters:
            set_value (`tuple[float, float]`): New coordinates to set.
            set_target (`Literal["current", "position", "expected", "hover", "select"]`): Target coordinate type to set
                coordinates for.
            ignore_assertion (`bool`, optional): Ignore assertion control. Defaults to `False`.

        Raises:
            AssertionError: If assertion control is enabled and `set_value` is not a valid coordinate container.
        """

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            validation.validate_coordinate_container(
                validate_value = set_value,
                custom_error = None,
                )

        # Unpacking and updating coordinates:
        coordinate_x, coordinate_y = set_value
        self.__set_coordinate_x(
            set_value = coordinate_x,
            set_target = set_target,
            ignore_assertion = ignore_assertion,
            )
        self.__set_coordinate_y(
            set_value = coordinate_y,
            set_target = set_target,
            ignore_assertion = ignore_assertion,
            )


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COORDINATES PROPERTIES AND METHODS

    """


    @cached_property
    def coordinates_current(self) -> namespace.Coordinates:
        """
        Set of coordinates where card object is currently located on screen.

        Returns:
            coordinates_current (`tuple[float, float]`): Set of coordinates where card object is currently located on screen.
        """

        # Packing up:
        coordinates_current: namespace.Coordinates = (
            self.__coordinate_x_current,
            self.__coordinate_y_current
            )

        # Returning:
        return coordinates_current


    @cached_property
    def coordinates_expected(self) -> namespace.Coordinates:
        """
        Set of coordinates where card object is expected to be located on screen.

        Returns:
            coordinates_expected (`tuple[float, float]`): Set of coordinates where card object is expected to be located on 
                screen.
        """

        # Packing up:
        coordinates_expected: namespace.Coordinates = (
            self.__coordinate_x_expected,
            self.__coordinate_y_expected,
            )

        # Returning:
        return coordinates_expected


    @cached_property
    def coordinates_position(self) -> namespace.Coordinates:
        """
        Set of coordinates where card object is supposed to be on screen, based on its location and area.

        Returns:
            coordinates_position (`tuple[float, float]`): Set of coordinates where card object is supposed to be on screen,
                based on its location and area.
        """

        # Packing up:
        coordinates_position: namespace.Coordinates = (
            self.__coordinate_x_position,
            self.__coordinate_y_position,
            )

        # Returning:
        return coordinates_position


    @cached_property
    def coordinates_hover(self) -> namespace.Coordinates:
        """
        Set of coordinates where card object is supposed to be when hovered over.

        Returns:
            coordinates_hover (`tuple[float, float]`): Set of coordinates where card object is supposed to be when hovered over.
        """

        # Packing up:
        coordinates_hover: namespace.Coordinates = (
            self.__coordinate_x_hover,
            self.__coordinate_y_hover,
            )

        # Returning:
        return coordinates_hover


    @cached_property
    def coordinates_select(self) -> namespace.Coordinates:
        """
        Set of coordinates where card object is supposed to be when selected.

        Returns:
            coordinates_select (`tuple[float, float]`): Set of coordinates where card object is supposed to be when selected.
        """

        # Packing up:
        coordinates_select: namespace.Coordinates = (
            self.__coordinate_x_select,
            self.__coordinate_y_select,
            )

        # Returning:
        return coordinates_select


    @cached_property
    def coordinates_unplayable(self) -> namespace.Coordinates:
        """
        Set of coordinates where card object is supposed to be when unplayable.

        Returns:
            coordinates_unplayable (`tuple[float, float]`): Set of coordinates where card object is supposed to be when unplayable.
        """

        # TODO!
        ...


    def set_coordinates_current(
            self, 
            set_value: namespace.Coordinates, 
            ignore_assertion: bool = False, 
            clear_cache: bool = True
            ) -> None:
        """
        Set new value for card object's current coordinates x and y.

        Uses `__set_coordinates()` inner method.

        Clears target and related properties cached with `functools` library's wrapper `cached_property` when enabled.

        Parameters:
            set_value (`tuple[float, float]`): New value for card object's current coordinates.
            ignore_assertion (`bool`, optional): Whether to ignore assertion tests. Defaults to `False`.
            clear_cache (`bool`, optional): Whether to clear cached properties. Defaults to `True`.
        """

        # Updating attributes:
        if self.coordinates_current != set_value:
            self.__set_coordinates(
                set_value = set_value,
                set_target = "current",
                ignore_assertion = ignore_assertion
                )

            # Clearing cache:
            if clear_cache:
                cached_property_list: tuple[str, ...] = (
                    "coordinates_current",
                    )
                cache.clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = cached_property_list
                    )


    def set_coordinates_expected(
            self,
            set_value: namespace.Coordinates,
            ignore_assertion: bool = False,
            clear_cache: bool = True,
            ) -> None:
        """
        Set new value for card object's expected coordinates x and y.

        Uses `__set_coordinates()` inner method.

        Clears target and related properties cached with `functools` library's wrapper `cached_property` when enabled.

        Parameters:
            set_value (`tuple[float, float]`): New value for card object's expected coordinates.
            ignore_assertion (`bool`, optional): Whether to ignore assertion tests. Defaults to `False`.
            clear_cache (`bool`, optional): Whether to clear cached properties. Defaults to `True`.
        """

        # Updating attributes:
        if self.coordinates_expected != set_value:
            self.__set_coordinates(
                set_value = set_value,
                set_target = "expected",
                ignore_assertion = ignore_assertion
                )

            # Clearing cache:
            if clear_cache:
                cached_property_list: tuple[str, ...] = (
                    "coordinates_expected",
                    )
                cache.clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = cached_property_list
                    )


    def set_coordinates_position(
            self,
            set_value: namespace.Coordinates,
            ignore_assertion: bool = False,
            clear_cache: bool = True,
            ) -> None:
        """
        Set new value for card object's position coordinates x and y.

        Uses `__set_coordinates()` inner method.

        Clears target and related properties cached with `functools` library's wrapper `cached_property` when enabled.

        Parameters:
            set_value (`tuple[float, float]`): New value for card object's position coordinates.
            ignore_assertion (`bool`, optional): Whether to ignore assertion tests. Defaults to `False`.
            clear_cache (`bool`, optional): Whether to clear cached properties. Defaults to `True`.
        """

        # Updating attributes:
        if self.coordinates_position != set_value:
            self.__set_coordinates(
                set_value = set_value,
                set_target = "position",
                ignore_assertion = ignore_assertion
                )

            # Clearing cache:
            if clear_cache:
                cached_property_list: tuple[str, ...] = (
                    "coordinates_position",
                    )
                cache.clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = cached_property_list
                    )


    def set_coordinates_hover(
            self, 
            set_value: namespace.Coordinates, 
            ignore_assertion: bool = False, 
            clear_cache: bool = True
            ) -> None:
        """
        Set new value for card object's hover coordinates x and y.

        Uses `__set_coordinates()` inner method.

        Clears target and related properties cached with `functools` library's wrapper `cached_property` when enabled.

        Parameters:
            set_value (`tuple[float, float]`): New value for card object's hover coordinates.
            ignore_assertion (`bool`, optional): Whether to ignore assertion tests. Defaults to `False`.
            clear_cache (`bool`, optional): Whether to clear cached properties.
        """

        # Updating attributes:
        self.__set_coordinates(
            set_value = set_value,
            set_target = "hover",
            ignore_assertion = ignore_assertion
            )

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinates_hover",
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )


    def set_coordinates_select(
            self, 
            set_value: namespace.Coordinates, 
            ignore_assertion: bool = False, 
            clear_cache: bool = True
            ) -> None:
        """
        Set new value for card object's select coordinates x and y.

        Uses `__set_coordinates()` inner method.

        Clears target and related properties cached with `functools` library's wrapper `cached_property` when enabled.

        Parameters:
            set_value (`tuple[float, float]`): New value for card object's select coordinates.
            ignore_assertion (`bool`, optional): Whether to ignore assertion tests. Defaults to `False`.
            clear_cache (`bool`, optional): Whether to clear cached properties. Defaults to `True`.
        """

        # Updating attributes:
        self.__set_coordinates(
            set_value = set_value,
            set_target = "select",
            ignore_assertion = ignore_assertion
            )

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinates_select",
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        STATE SET AND SWITCH METHODS
    
    """


    def __set_state(
            self,
            set_value: bool,
            set_target: namespace.StateType,
            ignore_assertion: bool = False
            ) -> None:
        """
        Set a state boolean value for one of the state types stored in this class.
        
        Constructs attribute name to get and set with `target_attribute: str = f"_CardObject__state_{set_target}"`, therefore
        `set_target` parameter must be a valid `namespace.StateType` value (default).

        Used by named setter methods.

        Parameters:
            set_value (`bool`): Value to set for the state.
            set_target (`str`): State type to set value for. Must be a valid `namespace.StateType` value.
            ignore_assertion (`bool`, optional): Whether to ignore assertion tests. Defaults to `False`.

        Raises:
            AssertionError: If `set_value` is not a valid boolean value.
        """

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            validation.validate_flag(
                validate_value = set_value,
                custom_error = None,
                )

        # Updating attribute:
        target_attribute: str = f"_CardObject__state_{set_target}"
        setattr(self, target_attribute, set_value)


    def __switch_state(
            self,
            switch_target: namespace.StateType,
            ) -> None:
        """
        Switch a state boolean value for one of the state types stored in this class.

        Constructs attribute name to get and set with `target_attribute: str = f"_CardObject__state_{switch_target}"`, therefore
        `switch_target` parameter must be a valid `namespace.StateType` value (default).

        Used by named setter methods.

        Parameters:
            switch_target (`str`): State type to switch value for. Must be a valid `namespace.StateType` value.
        """

        # Updating attribute:
        target_attribute: str = f"_CardObject__state_{switch_target}"
        set_value: bool = not getattr(self, target_attribute)
        setattr(self, target_attribute, set_value)
    

    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        STATE PROPERTIES AND METHODS
    
    """


    @property
    def state_ready(self) -> bool:
        """
        Returns `True` if `CardObject` class instance is fully set up and ready for use, `False` otherwise. Checks attributes and 
        their sentinel value (mostly `None`). If any exist, breaks check and returns `False`.

        Used when generating cards and loading textures.

        Returns:
            state_ready (`bool`):
        """

        # Asserting card object is ready:
        ...     # TODO


    @property
    def state_hovered(self) -> bool:
        """
        Card's hovered state. Set and switched by game controller on event.

        Returns:
            self.__state_hovered (`bool`): `True` if card is currently being hovered over, `False` otherwise.
        """

        # Returning:
        return self.__state_hovered


    @property
    def state_selected(self) -> bool:
        """
        Card's selected state. Set and switched by game controller on event.

        Returns:
            self.__state_selected (`bool`): `True` if card is currently selected, `False` otherwise.
        """

        # Returning:
        return self.__state_selected


    @property
    def state_playable(self) -> bool:
        """
        Card's playable state. Set and switched by game controller on event.

        Returns:
            self.__state_playable (`bool`): `True` if card is currently playable, `False` otherwise.
        """

        # Returning:
        return self.__state_playable


    @property
    def state_controlled(self) -> bool:
        """
        Card's controlled state. Set and switched by game controller on event.

        Controlled state signifies game controller if `CardObject` is released and can be manipulated freely by any other 
        controller and/or player, otherwise it is locked and can only be manipulated by the controller that has it selected.

        Returns:
            self.__state_controlled (`bool`): `True` if card is currently controlled, `False` otherwise.
        """

        # Returning:
        return self.__state_controlled


    @property
    def state_idle(self) -> bool:
        """
        Card's idle state.

        Returns:
            state_idle (`bool`): `True` if card is not moving, `False` otherwise.
        """

        # Asserting card object is not moving:
        state_idle: bool = self.coordinates_current == self.coordinates_expected

        # Returning:
        return state_idle

    
    @property
    def state_showcase(self) -> bool:
        """
        Card's showcase state. Set to cards on the bottom of the Deck positions (secret and/or trump cards).

        Returns:
            self.__state_showcase (`bool`): `True` if card is a showcase card, `False` otherwise.
        """

        # Returning:
        return self.__state_showcase


    def set_state_ready(
            self,
            set_value: bool = True,
            ignore_assertion: bool = False,
            ) -> None:
        """
        Force set `CardObject` class instance ready state. Developer method use only!

        Uses `__set_state()` inner method.

        Parameters:
            set_value (`bool`): `True` to set `CardObject` class instance ready state, `False` to unset it.
            ignore_assertion (`bool`): `True` to ignore assertion, `False` to enable it.
        """

        # Setting state:
        self.__set_state(
            set_value = set_value,
            set_target = "ready",
            ignore_assertion = ignore_assertion,
            )
        
    
    def set_state_hovered(
            self,
            set_value: bool = True,
            ignore_assertion: bool = False,
            clear_cache: bool = True,
            ) -> None:
        """
        Set `CardObject` class instance hovered state. Called by game controller on event.

        Uses `__set_state()` inner method.

        Parameters:
            set_value (`bool`): `True` to set `CardObject` class instance hovered state, `False` to unset it.
            ignore_assertion (`bool`): `True` to ignore assertion, `False` to enable it.
            clear_cache (`bool`): `True` to clear related cached properties, `False` to ignore.
        """

        # Setting state:
        self.__set_state(
            set_value = set_value,
            set_target = "hovered",
            ignore_assertion = ignore_assertion,
            )

        # Clearing cache, if required:
        if clear_cache:
            ...         # TODO: Implement


    def switch_state_hovered(
            self,
            clear_cache: bool = True
            ) -> None:
        """
        Swtich `CardObject` class instance hovered state. Called by game controller on event.

        Uses `__switch_state()` inner method.

        Parameters:
            clear_cache (`bool`): `True` to clear related cached properties, `False` to ignore.
        """

        # Switching state:
        self.__switch_state(
            switch_target = "hovered",
            )

        # Clearing cache, if required:
        if clear_cache:
            ...         # TODO: Implement

    
    def set_state_selected(
            self,
            set_value: bool,
            ignore_assertion: bool = False,
            clear_cache: bool = True,
            ) -> None:
        """
        Set `CardObject` class instance selected state. Called by game controller on event.

        Parameters:
            set_value (`bool`): `True` to set `CardObject` class instance selected state, `False` to unset it.
            ignore_assertion (`bool`): `True` to ignore assertion, `False` to enable it.
            clear_cache (`bool`): `True` to clear related cached properties, `False` to ignore.
        """

        # Setting state:
        self.__set_state(
            set_value = set_value,
            set_target = "selected",
            ignore_assertion = ignore_assertion,
            )

        # Clearing cache, if required:
        if clear_cache:
            ...         # TODO: Implement

    
    def switch_state_selected(
            self,
            clear_cache: bool = True
            ) -> None:
        """
        Swtich `CardObject` class instance selected state. Called by game controller on event.

        Uses `__switch_state()` inner method.

        Parameters:
            clear_cache (`bool`): `True` to clear related cached properties, `False` to ignore.
        """

        # Switching state:
        self.__switch_state(
            switch_target = "selected",
            )

        # Clearing cache, if required:
        if clear_cache:
            ...         # TODO: Implement
        

    def set_state_controlled(
            self,
            set_value: bool,
            ignore_assertion: bool = False,
            clear_cache: bool = True,
            ) -> None:
        """
        Set `CardObject` class instance controlled state. Called by game controller on event.

        Uses `__set_state()` inner method.

        Parameters:
            set_value (`bool`): `True` to set `CardObject` class instance controlled state, `False` to unset it.
            ignore_assertion (`bool`): `True` to ignore assertion, `False` to enable it.
            clear_cache (`bool`): `True` to clear related cached properties, `False` to ignore.
        """

        # Setting state:
        self.__set_state(
            set_value = set_value,
            set_target = "controlled",
            ignore_assertion = ignore_assertion,
            )

        # Clearing cache, if required:
        if clear_cache:
            ...         # TODO: Implement


    def switch_state_controlled(
        self,
        clear_cache: bool = True
        ) -> None:
        """
        Swtich `CardObject` class instance controlled state. Called by game controller on event.

        Uses `__switch_state()` inner method.

        Parameters:
            clear_cache (`bool`): `True` to clear related cached properties, `False` to ignore.
        """

        # Switching state:
        self.__switch_state(
            switch_target = "controlled",
            )

        # Clearing cache, if required:
        if clear_cache:
            ...         # TODO: Implement


    def set_state_showcase(
        self,
        set_value: bool,
        ignore_assertion: bool = False,
        clear_cache: bool = True,
        ) -> None:
        """
        Set `CardObject` class instance showcase state. Called by game controller on event.

        Uses `__set_state()` inner method.

        Parameters:
            set_value (`bool`): `True` to set `CardObject` class instance showcase state, `False` to unset it.
            ignore_assertion (`bool`): `True` to ignore assertion, `False` to enable it.
            clear_cache (`bool`): `True` to clear related cached properties, `False` to ignore.
        """

        # Setting state:
        self.__set_state(
            set_value = set_value,
            set_target = "showcase",
            ignore_assertion = ignore_assertion,
            )

        # Clearing cache, if required:
        if clear_cache:
            ...         # TODO: Implement

    
    def switch_state_showcase(
        self,
        clear_cache: bool = True,
        ) -> None:
        """
        Swtich `CardObject` class instance showcase state. Called by game controller on event.

        Uses `__switch_state()` inner method.

        Parameters:
            clear_cache (`bool`): `True` to clear related cached properties, `False` to ignore.
        """

        # Switching state:
        self.__switch_state(
            switch_target = "showcase",
            )

        # Clearing cache, if required:
        if clear_cache:
            ...         # TODO: Implement

    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        RENDER (TILT) PROPERTIES AND METHODS
    
    """


    @property
    def render_tilt_current(self) -> int:
        """
        Card's current tilt angle.

        Returns:
            self.__render_tilt_current (`int`): Card's current tilt angle.
        """

        # Returning:
        return self.__render_tilt_current


    @cached_property
    def render_tilt_random(self) -> int:
        """
        Random tilt angle between min and max values stored in `SETTINGS.CARD.RENDER.TILT` settings module.

        Cached with `functools` module's `@cached_property` decorator. Must be cleared before generating a new random tilt angle.
        Can be cleared by related methods.

        Returns:
            tilt_angle (`int`): Random tilt angle.
        """

        # Generating new tilt angle:
        tilt_axis: int = random.choice(SETTINGS.CARD.RENDER.TILT.RANDOM_AXIS)
        tilt_angle_random: int = random.randint(
            SETTINGS.CARD.RENDER.TILT.RANDOM_ANGLE_MIN,
            SETTINGS.CARD.RENDER.TILT.RANDOM_ANGLE_MAX
            )
        tilt_angle: int = tilt_angle_random * tilt_axis

        # Returning:
        return tilt_angle


    @cached_property
    def render_tilt_arch(self) -> int:
        """
        Arched tilt angle based on card's coordinates on screen and their relation to the middle of the table surface.

        Cached with `functools` module's `@cached_property` decorator. Must be cleared before generating a new arch tilt angle.
        Can be cleared by related methods.

        Returns:
            tilt_angle (`int`): Arched tilt angle.
        """

        # TODO: Implement!
        ...


    def set_render_tilt(
            self,
            set_value: int,
            ignore_assertion: bool = False,
            clear_cache: bool = True,
            ) -> None:
        """
        Set a new render tilt angle for `CardObject` class instance.

        Parameters:
            set_value (`int`): New render tilt angle.
            ignore_assertion (`bool`): `True` to ignore assertion, `False` to enable it.
            clear_cache (`bool`): `True` to clear related cached properties, `False` to ignore.

        Raises:
            AssertionError: If assertion is enabled and `set_value` is not a valid type.
        """

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_is_valid_type(
                check_value = set_value,
                check_type = int,
                raise_error = True,
                custom_error = False,
                )

        # Updating attribute:
        if self.render_tilt_current != set_value:
            self.__render_tilt_current = set_value

            # Clearing cache, if required:
            if clear_cache:
                ...             # TODO: Clear related and target cached properties!
