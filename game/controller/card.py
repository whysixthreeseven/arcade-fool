# Typing and annotations:
from __future__ import annotations

# External libraries:
import random
import arcade

# Settings, session and context:
from game.settings import SETTINGS
from game.session import SESSION
from game import context, coordinates

# Cache management:
from functools import cached_property
from game.utilities.scripts import cache

# Various utilities:
from game.utilities import texturepack
from game.utilities.scripts import assertion, validate


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    CARD CLASS OBJECT CONSTRUCTOR
    
"""


class Card:
    """
    Card class object.
    
    This class object is responsible for the creation and management of a card object. Cards are the main elements of the game
    and, therefore, have the most logic written in them. Thus, this and other class instances utilize `functools` library's 
    `cached_property` decorator to cache their attributes and methods, and custom-written `utilities.scripts.cache` 
    module to manage the cache.
    
    All the render attributes are calculated and rendering on screen are done by the class native methods, with textures loaded,
    stored, and used by it. 
    
    There are a total of 52 available cards in the game, with 13 cards per suit, and 4 suits available. Default cards are cards
    including and above the six and stretch all the way to the aces, jokers are not part of the game. Trump cards are refered to
    cards whose suit is chosen to be trump suit for the game (or period of game, if secret mode is enabled in `SESSION`). Card
    objects can be used to compare one to another to determine if they can be played.
    """
    
    def __init__(self) -> None:
        """
        Card class object constructor.
        
        Initializes attributes with default values drawn from `SETTINGS` class instance, or with `None` or `0` value sentinels 
        to avoid raising errors when accessing them and `pyglet` complaining about creating render-related instances before the
        game screen is available to the user.
        """
        
        # Core attributes:
        self.__name: str = None
        self.__suit: str = None
        self.__trump: bool = None
        
        # Added attributes:
        self.__id: int = None
        self.__added_index: int = None
        
        # Texture pack attributes:
        self.__texturepack_front: texturepack.TexturePack = None
        self.__texturepack_back: texturepack.TexturePack = None
        
        # Texture object attributes:
        self.__texture_object_front: texturepack.Texture = None
        self.__texture_object_back: texturepack.Texture = None
        
        # Render attributes:
        self.__render_scale: float = SETTINGS.CARD_RENDER_SCALE_DEFAULT
        self.__render_alpha: int = SETTINGS.CARD_RENDER_ALPHA_DEFAULT
        self.__render_tilt: int = SETTINGS.CARD_RENDER_TILT_DEFAULT
        
        # Coordinates attributes:
        self.__coordinate_x_current: int = 0
        self.__coordinate_y_current: int = 0
        self.__coordinate_x_position: int = 0
        self.__coordinate_y_position: int = 0
        self.__coordinate_x_hover: int = 0
        self.__coordinate_y_hover: int = 0
        self.__coordinate_x_expected: int = 0
        self.__coordinate_y_expected: int = 0
        
        # State attributes:
        self.__state_visible: bool = False
        self.__state_revealed: bool = False
        self.__state_hovered: bool = False
        self.__state_selected: bool = False
        self.__state_faded: bool = False
        self.__state_playable: bool = False
        
        # Play location and index:
        self.__location: str = None
        self.__location_index: int = None
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        NATIVE METHODS
    
    """
    
    
    def __gt__(self, other: Card) -> bool:
        """
        Allows this card object compare itself to other cards based on its value. 
        
        The comparison is done by comparing the value of the cards and the suit of the cards. If the card is a trump card, it 
        will always be greater than other cards of the same suit. If the card is not a trump card, it will only be greater than 
        other cards of the same suit if its value is greater than the value of the other card.
        
        Returns
        -------
        assert_eval : `bool`
            `True` if the card is greater than the other card, `False` otherwise.
        """
        
        # Comparing values:
        assert_eval: bool = bool(
            self.trump and self.value > other.value or
            self.suit == other.suit and self.value > other.value
            )
        
        # Returning:
        return assert_eval


    def __lt__(self, other: Card) -> bool:
        """
        Allows this card object compare itself to other cards based on its value.
        
        The comparison is done by comparing the value of the cards and the suit of the cards. If the card is a trump card, it
        will always be less than other cards of the same suit. If the card is not a trump card, it will only be less than
        other cards of the same suit if its value is less than the value of the other card.
        
        Returns
        -------
        assert_eval : `bool`
            `True` if the card is less than the other card, `False` otherwise.
        """

        # Comparing values:
        assert_eval: bool = bool(
            self.trump and self.value < other.value or
            self.suit == other.suit and self.value < other.value
            )

        # Returning:
        return assert_eval
    
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the card object.
        
        Returns
        -------
        card : `str`
            A string representation of the card object.
        """
        
        # Generating string:
        card: str = f"{self.suit_ascii}{self.name_ascii}"       # TODO: Replace with a better repr string
        
        # Returning:
        return card
        
        
    def __str__(self) -> str:
        """
        Returns a string representation of the card object.

        Returns
        -------
        card : `str`
            A string representation of the card object.
        """
        
        # Generating string:
        card: str = f"{self.suit_ascii}{self.name_ascii}"
        
        # Returning:
        return card
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CLASS METHODS
    
    """
    
    
    @classmethod
    def generate(cls, init_id: int, init_suit: str, init_name: str, init_location: context.Location) -> Card:
        """
        Generates a new card object with the given attributes.
        
        Used by `Deck` controller to create a new instance of container. Does not call `game.utilities.script.cache` module's
        `refresh_object()` function at the end, allowing properties to remain "lazy" until they are first called to avoid any 
        issues with `pyglet` library creating and/or attempting to render objects on screen before the game window is 
        initialized.

        Parameters
        ----------
        init_id : `int`
            The id of the card.
        init_suit : `str`
            The suit of the card.
        init_name : `str`
            The name of the card.
        init_location : `context.Location`
            The location of the card in tuple collection format: `(context.CARD_LOCATION.VALUE, int)`.

        Returns
        -------
        card_object : `Card`
            The generated card object.
        """
        
        # Creating basic card object:
        card_object: Card = Card()
        
        # Adding core attributes:
        card_object.set_id(
            set_value = init_id,
            )
        card_object.set_suit(
            set_value = init_suit,
            )
        card_object.set_name(
            set_value = init_name,
            )
        
        # Updating location and coordinates:
        card_object.set_location(
            set_value = init_location,
            ignore_assertion = False,
            clear_cache = False,
            )
            
        # Loading default textures:
        card_object.set_texturepack_front(
            texturepack_object = SESSION.TEXTUREPACK_FRONT_SELECTED,
            update_texture = True,
            ignore_assertion = False,
            clear_cache = False,
            )
        card_object.set_texturepack_back(
            texturepack_object = SESSION.TEXTUREPACK_BACK_SELECTED,
            update_texture = True,
            ignore_assertion = False,
            clear_cache = False,
            )
        
        # Waking up all other attributes:
        card_object.clear_cached_attributes()
        
        # Returning:
        return card_object


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_core_attributes(self) -> tuple[str, ...]:
        """
        Core attributes-related cached properties list.
        
        Collects and returns all properties of this card object decorated with `functools` library's `cached_property` wrapper.
        Used to clear all related properties at once on certain events and when certain attributes change with their dedicated
        setter.
        
        Cached with `functools` library's `cached_property` decorator. Static, cannot be cleared.
        
        Returns
        -------
        cached_property_list : `tuple[str, ...]`
            A tuple collection of related cached properties.
        """
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "name",
            "name_ascii",
            "suit",
            "suit_ascii",
            "color",
            "value"
            "trump"
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_texture_attributes(self) -> tuple[str, ...]:
        """
        Texture and texturepack attributes-related cached properties list.
        
        Collects and returns all properties of this card object decorated with `functools` library's `cached_property` wrapper.
        Used to clear all related properties at once on certain events and when certain attributes change with their dedicated
        setter.
        
        Cached with `functools` library's `cached_property` decorator. Static, cannot be cleared.
        
        Returns
        -------
        cached_property_list : `tuple[str, ...]`
            A tuple collection of related cached properties.
        """
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "texturepack_front",
            "texturepack_back",
            "texture_filepath_front",
            "texture_filepath_back",
            "texture_object_front",
            "texture_object_back",
            "texture_object_selected",
            )

        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_boundary_attributes(self) -> tuple[str, ...]:
        """
        Boundary attributes-related cached properties list.
        
        Collects and returns all properties of this card object decorated with `functools` library's `cached_property` wrapper.
        Used to clear all related properties at once on certain events and when certain attributes change with their dedicated
        setter.
        
        Cached with `functools` library's `cached_property` decorator. Static, cannot be cleared.
        
        Returns
        -------
        cached_property_list : `tuple[str, ...]`
            A tuple collection of related cached properties.
        """
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "boundary_left",
            "boundary_right",
            "boundary_top",
            "boundary_bottom",
            "boundary_horizontal",
            "boundary_vertical",
            "boundary"
            )
        
        # Returning:
        return cached_property_list


    @cached_property
    def __cached_render_attributes(self) -> tuple[str, ...]:
        """
        Render attributes-related cached properties list.
        
        Collects and returns all properties of this card object decorated with `functools` library's `cached_property` wrapper.
        Used to clear all related properties at once on certain events and when certain attributes change with their dedicated
        setter.
        
        Cached with `functools` library's `cached_property` decorator. Static, cannot be cleared.
        
        Returns
        -------
        cached_property_list : `tuple[str, ...]`
            A tuple collection of related cached properties.
        """

        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "render_scale",
            "render_alpha",
            "render_tilt"
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_render_rect_attributes(self) -> tuple[str, ...]:
        """
        Render rect attributes-related cached properties list.
        
        Collects and returns all properties of this card object decorated with `functools` library's `cached_property` wrapper.
        Used to clear all related properties at once on certain events and when certain attributes change with their dedicated
        setter.
        
        Cached with `functools` library's `cached_property` decorator. Static, cannot be cleared.
        
        Returns
        -------
        cached_property_list : `tuple[str, ...]`
            A tuple collection of related cached properties.
        """

        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "render_rect",
            "render_width",
            "render_height",
            "render_text",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_coordinates_attributes(self) -> tuple[str, ...]:
        """
        Coordinates attributes-related cached properties list.
        
        Collects and returns all properties of this card object decorated with `functools` library's `cached_property` wrapper.
        Used to clear all related properties at once on certain events and when certain attributes change with their dedicated
        setter.
        
        Cached with `functools` library's `cached_property` decorator. Static, cannot be cleared.
        
        Returns
        -------
        cached_property_list : `tuple[str, ...]`
            A tuple collection of related cached properties.
        """

        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            
            # Current coordinates:
            "coordinate_x",
            "coordinate_y",
            "coordinates"
            
            # Position coordinates:
            "coordinate_x_position",
            "coordinate_y_position",
            "coordinates_position",
            
            # Hover coordinates:
            "coordinate_x_hover",
            "coordinate_y_hover",
            "coordinates_hover",
            
            # Expected coordinates:
            "coordinate_x_expected",
            "coordinate_y_expected",
            "coordinates_expected"
            )
        
        # Returning:
        return cached_property_list


    @cached_property
    def __cached_state_attributes(self) -> tuple[str, ...]:
        """
        State attributes-related cached properties list.
        
        Collects and returns all properties of this card object decorated with `functools` library's `cached_property` wrapper.
        Used to clear all related properties at once on certain events and when certain attributes change with their dedicated
        setter.
        
        Cached with `functools` library's `cached_property` decorator. Static, cannot be cleared.
        
        Returns
        -------
        cached_property_list : `tuple[str, ...]`
            A tuple collection of related cached properties.
        """

        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "state_visible",
            "state_revealed",
            "state_hovered",
            "state_selected",
            "state_faded",
            "state_idle",
            "state_playable",
            "state_secret",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_location_attributes(self) -> tuple[str, ...]:
        """
        Location attributes-related cached properties list.
        
        Collects and returns all properties of this card object decorated with `functools` library's `cached_property` wrapper.
        Used to clear all related properties at once on certain events and when certain attributes change with their dedicated
        setter.
        
        Cached with `functools` library's `cached_property` decorator. Static, cannot be cleared.
        
        Returns
        -------
        cached_property_list : `tuple[str, ...]`
            A tuple collection of related cached properties.
        """
    
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "location",
            "location_index",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_id_attributes(self) -> tuple[str, ...]:
        """
        Identicator attributes-related cached properties list.
        
        Collects and returns all properties of this card object decorated with `functools` library's `cached_property` wrapper.
        Used to clear all related properties at once on certain events and when certain attributes change with their dedicated
        setter.
        
        Cached with `functools` library's `cached_property` decorator. Static, cannot be cleared.
        
        Returns
        -------
        cached_property_list : `tuple[str, ...]`
            A tuple collection of related cached properties.
        """
    
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "id",
            "id_repr",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_added_index_attributes(self) -> tuple[str, ...]:
        """
        Added index attributes-related cached properties list.
        
        Collects and returns all properties of this card object decorated with `functools` library's `cached_property` wrapper.
        Used to clear all related properties at once on certain events and when certain attributes change with their dedicated
        setter.
        
        Cached with `functools` library's `cached_property` decorator. Static, cannot be cleared.
        
        Returns
        -------
        cached_property_list : `tuple[str, ...]`
            A tuple collection of related cached properties.
        """
    
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "added_index",
            )
        
        # Returning:
        return cached_property_list
    

    def clear_cached_core_attributes(self) -> None:
        """
        Clears all public cached core properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear texturepack properties of this card object.
        """

        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_core_attributes
            )
    
    
    def clear_cached_texture_attributes(self) -> None:
        """
        Clears all public cached texture properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear all cached properties of this card object.
        """
    
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_texture_attributes
            )
        
        
    def clear_cached_boundary_attributes(self) -> None:
        """
        Clears all public cached boundary properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear all cached properties of this card object.
        """
        
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_boundary_attributes
            )
        
    
    def clear_cached_render_attributes(self) -> None:
        """
        Clears all public cached render properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear all cached properties of this card object.
        """
    
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_render_attributes
            )
        
        
    def clear_cached_render_rect_attributes(self) -> None:
        """
        Clears all public cached render rect properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear texturepack properties of this card object.
        """
        
        # Clearing cache:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_render_rect_attributes
            )
        

    def clear_cached_coordinates_attributes(self) -> None:
        """
        Clears all public cached coordinates properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear texturepack properties of this card object.
        """
        
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_coordinates_attributes
            )
    
    
    def clear_cached_state_attributes(self) -> None:
        """
        Clears all public cached state properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear texturepack properties of this card object.
        """
        
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_state_attributes
            )
        
        
    def clear_cached_location_attributes(self) -> None:
        """
        Clears all public cached location properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear texturepack properties of this card object.
        """
            
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_location_attributes
            )
        
    
    def clear_cached_id_attributes(self) -> None:
        """
        Clears all public cached id properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear all cached properties of this card object.
        """
    
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_id_attributes
            )
    
    
    def clear_cached_added_index_attributes(self) -> None:
        """
        Clears all public cached added index properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear all cached properties of this card object.
        """
    
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_added_index_attributes
            )
        
    
    def clear_cached_attributes(self) -> None:
        """
        Clears all public cached properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and all property lists available to
        clear all cached properties of this card object in a single loop through lists collection.
        """
        
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_core_attributes,
            self.__cached_texture_attributes,
            self.__cached_boundary_attributes,
            self.__cached_render_attributes,
            self.__cached_render_rect_attributes,
            self.__cached_coordinates_attributes,
            self.__cached_state_attributes,
            self.__cached_location_attributes,
            self.__cached_id_attributes,
            self.__cached_added_index_attributes,
            )
        
        # Looping throught the list and clearing cache:
        for cached_property_list in cached_property_list_collection:
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARD NAME CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def name(self) -> str:
        
        # Returning:
        return self.__name
    
    
    @cached_property
    def name_ascii(self) -> str:
        
        # Generating a dictionary index:
        name_ascii_index = {
            attr_name.capitalize(): getattr(context.CARD_NAME_ASCII, attr_name)
            for attr_name, attr_value in context.CARD_NAME.__dict__.items()
            if not attr_name.startswith("_") and hasattr(context.CARD_NAME_ASCII, attr_name)
            }
        
        # Getting correct value:
        name_ascii: str = name_ascii_index.get(
            self.name,          # Cached property (None by default)
            None                # Default return, if name not set
            )
        
        # Returning:
        return name_ascii
    
    
    def set_name(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
            
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_name(
                validate_value = set_value
                )
            
        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "name",
                sentinel_value = None,
                raise_error = True
                )
            
        # Updating attribute:
        self.__name = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "name",
                "name_ascii",
                "value",
                "render_text"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARD SUIT CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def suit(self) -> str:

        # Returning:
        return self.__suit
    

    @cached_property
    def suit_ascii(self) -> str:

        # Generating a dictionary index:
        suit_ascii_index = {
            attr_name.capitalize(): getattr(context.CARD_SUIT_ASCII, attr_name)
            for attr_name, attr_value in context.CARD_SUIT.__dict__.items()
            if not attr_name.startswith("_") and hasattr(context.CARD_SUIT_ASCII, attr_name)
            }
        
        # Getting correct value:
        suit_ascii: str = suit_ascii_index.get(
            self.suit,          # Cached property (None by default)
            None                # Default return, if name not set
            )
        
        # Returning:
        return suit_ascii
    
    
    def set_suit(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
    
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_suit(
                validate_value = set_value
                )

        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "suit",
                sentinel_value = None,
                raise_error = True
                )
            
        # Updating attribute:
        self.__suit = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "suit",
                "suit_ascii",
                "color",
                "trump",
                "render_text"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARD COLOR CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def color(self) -> str:
        
        # Getting correct color:
        color_index: dict[str, str] = {
            context.CARD_SUIT.HEARTS: context.CARD_SUIT_COLOR.RED,
            context.CARD_SUIT.DIAMONDS: context.CARD_SUIT_COLOR.RED,
            context.CARD_SUIT.CLUBS: context.CARD_SUIT_COLOR.BLACK,
            context.CARD_SUIT.SPADES: context.CARD_SUIT_COLOR.BLACK,
            }
        color: str = color_index.get(
            self.suit,      # Cached property (None by default)
            None            # Default return, if suit not set
            )

        # Returning:
        return color
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARD VALUE CACHED PROPERTIES AND METHODS
    
    """


    @cached_property
    def trump(self) -> bool:
        
        # Returning:
        return self.__trump
    
    
    @cached_property
    def value(self) -> int:
        
        # Generating a dictionary index:
        value_index = {
            attr_name.capitalize(): getattr(context.CARD_VALUE, attr_name)
            for attr_name, attr_value in context.CARD_NAME.__dict__.items()
            if not attr_name.startswith("_") and hasattr(context.CARD_VALUE, attr_name)
            }
                
        # Getting correct value:
        value: str = value_index.get(
            self.name,      # Cached property (None by default)
            None            # Default return, if name not set
            )
                
        # Calculating value:
        if value is not None and self.trump:
            value += 100
        
        # Returning:
        return value


    def set_trump(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )

        # Updating attribute:
        self.__trump = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "trump",
                "value",
                "render_text",
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
    
    def switch_trump(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.__trump = not self.__trump
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "trump",
                "value"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COORDINATES (CURRENT) CACHED PROPERTIES AND METHODS
        
    """
    
    
    @cached_property
    def coordinate_x(self) -> int:
        
        # Returning:
        return self.__coordinate_x_current


    @cached_property
    def coordinate_y(self) -> int:

        # Returning:
        return self.__coordinate_y_current
    
    
    @cached_property
    def coordinates(self) -> tuple[int, int]:
        
        # Making container:
        coordinates: tuple[int, int] = (
            self.coordinate_x,
            self.coordinate_y
            )

        # Returning:
        return coordinates
        
        
    def set_coordinate_x(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_x_current = set_value

        # Clearing cache:
        if clear_cache:
            
            # Clearing target cached properties:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x",
                "coordinates",
                "render_rect",
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
            # Clearing related cached properties:
            self.clear_cached_boundary_attributes() 
            
            
    def adjust_coordinate_x(self, adjust_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = adjust_value,
                check_type = int,
                raise_error = True
                )
            
        # Updating attribute:
        coordinate_x_adjusted: int = self.coordinate_x + adjust_value
        self.set_coordinate_x(
            set_value = coordinate_x_adjusted,
            ignore_assertion = ignore_assertion,
            clear_cache = clear_cache
            )


    def set_coordinate_y(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_y_current = set_value
        
        # Clearing cache:
        if clear_cache:
            
            # Clearing target cached properties:
            cached_property_list: tuple[str, ...] = (
                "coordinate_y",
                "coordinates",
                "render_rect"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )

            # Clearing related cached properties:
            self.clear_cached_boundary_attributes()
            
            
    def adjust_coordinate_y(self, adjust_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = adjust_value,
                check_type = int,
                raise_error = True
                )

        # Updating attribute:
        coordinate_y_adjusted: int = self.coordinate_y + adjust_value
        self.set_coordinate_y(
            set_value = coordinate_y_adjusted,
            ignore_assertion = ignore_assertion,
            clear_cache = clear_cache
            )
            
    
    def set_coordinates(self, set_value: tuple[int, int], ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = set_value
                )
            
        # Unpacking coordinates:
        coordinate_x, coordinate_y = set_value
            
        # Updating attributes:
        self.set_coordinate_x(
            set_value = coordinate_x,
            ignore_assertion = True,
            clear_cache = False,
            )
        self.set_coordinate_y(
            set_value = coordinate_y,
            ignore_assertion = True,
            clear_cache = False,
            )
        
        # Clearing cache:
        if clear_cache:
            
            # Clearing target cached properties:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x",
                "coordinate_y",
                "coordinates",
                "render_rect"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
            # Clearing related cached properties:
            self.clear_cached_boundary_attributes()
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COORDINATES (POSITION) CACHED PROPERTIES AND METHODS
        
    """
    

    @cached_property
    def coordinate_x_position(self) -> int:
        
        # Returning:
        return self.__coordinate_x_position
    
    
    @cached_property
    def coordinate_y_position(self) -> int:

        # Returning:
        return self.__coordinate_y_position
    
    
    @cached_property
    def coordinates_position(self) -> tuple[int, int]:
        
        # Packing container:
        coordinates_position: tuple[int, int] = (
            self.__coordinate_x_position,
            self.__coordinate_y_position
            )

        # Returning:
        return coordinates_position
    
    
    def set_coordinate_x_position(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_x_position = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_position",
                "coordinates_position"
                )
            cache.clear_cached_property_list(
                target_oject = self,
                target_attribute = cached_property_list
                )
            
    
    def set_coordinate_y_position(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_y_position = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_y_position",
                "coordinates_position"
                )
            cache.clear_cached_property_list(
                target_oject = self,
                target_attribute = cached_property_list
                )
        
        
    def set_coordinates_position(self, set_value: tuple[int, int], ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = set_value
                )

        # Unpacking coordinates:
        coordinate_x, coordinate_y = set_value

        # Updating attributes:
        self.set_coordinate_x_position(
            set_value = coordinate_x,
            ignore_assertion = True,
            clear_cache = False,
            )
        self.set_coordinate_y_position(
            set_value = coordinate_y,
            ignore_assertion = True,
            clear_cache = False,
            )

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_position",
                "coordinate_y_position",
                "coordinates_position"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
            
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COORDINATES (EXPECTED) CACHED PROPERTIES AND METHODS
        
    """
            
    
    @cached_property
    def coordinate_x_expected(self) -> int:
        
        # Returning:
        return self.__coordinate_x_expected


    @cached_property
    def coordinate_y_expected(self) -> int:

        # Returning:
        return self.__coordinate_y_expected


    @cached_property
    def coordinates_expected(self) -> tuple[int, int]:

        # Packing container:
        coordinates_expected: tuple[int, int] = (
            self.__coordinate_x_expected,
            self.__coordinate_y_expected
            )

        # Returning:
        return coordinates_expected


    def set_coordinate_x_expected(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__coordinate_x_expected = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_expected",
                "coordinates_expected"
                )
            cache.clear_cached_property_list(
                target_oject = self,
                target_attribute_list = cached_property_list
                )
            
    
    def set_coordinate_y_expected(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_y_expected = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_y_expected",
                "coordinates_expected"
                )
            cache.clear_cached_property_list(
                target_oject = self,
                target_attribute_list = cached_property_list
                )
            
    
    def set_coordinates_expected(self, set_value: tuple[int, int], ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordiante_container(
                validate_value = set_value
                )

        # Unpacking coordinates:
        coordinate_x, coordinate_y = set_value
        
        # Updating attributes:
        self.set_coordinate_x_expected(
            set_value = coordinate_x,
            ignore_assertion = True,
            clear_cache = False,
            )
        self.set_coordinate_y_expected(
            set_value = coordinate_y,
            ignore_assertion = True,
            clear_cache = False,
            )

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_expected",
                "coordinate_y_expected",
                "coordinates_expected"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COORDINATES (HOVER) CACHED PROPERTIES AND METHODS
        
    """
    
    
    @cached_property
    def coordinate_x_hover(self) -> int:

        # Returning:
        return self.__coordinate_x_hover
    

    @cached_property
    def coordinate_y_hover(self) -> int:

        # Returning:
        return self.__coordinate_y_hover


    @cached_property
    def coordinates_hover(self) -> tuple[int, int]:

        # Packing container:
        coordinates_hover: tuple[int, int] = (
            self.__coordinate_x_hover,
            self.__coordinate_y_hover
            )

        # Returning:
        return coordinates_hover


    def set_coordinate_x_hover(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_x_hover = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_hover",
                "coordinates_hover"
                )
            cache.clear_cached_property_list(
                target_oject = self,
                target_attribute_list = cached_property_list
                )
            
    
    def set_coordinate_y_hover(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value
                )

        # Updating attribute:
        self.__coordinate_y_hover = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_y_hover",
                "coordinates_hover"
                )
            cache.clear_cached_property_list(
                target_oject = self,
                target_attribute_list = cached_property_list
                )
            
    
    def set_coordinates_hover(self, set_value: tuple[int, int], ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = set_value
                )

        # Unpacking coordinates:
        coordinate_x, coordinate_y = set_value
        
        # Updating attributes:
        self.set_coordinate_x_hover(
            set_value = coordinate_x,
            ignore_assertion = True,
            clear_cache = False,
            )
        self.set_coordinate_y_hover(
            set_value = coordinate_y,
            ignore_assertion = True,
            clear_cache = False,
            )

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x_hover",
                "coordinate_y_hover",
                "coordinates_hover"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        TEXTURE CACHED PROPETIES AND METHODS
    
    """
    
    
    @cached_property
    def texturepack_front(self) -> texturepack.TexturePack:
        
        # Returning:
        return self.__texturepack_front
    
    
    @cached_property
    def texturepack_back(self) -> texturepack.TexturePack:
        
        # Returning:
        return self.__texturepack_back
    
    
    @cached_property
    def texture_filepath_front(self) -> str:
        
        # Acquiring filename:
        texture_filepath: str = self.texturepack_front.texture_index[self.suit].get(self.name, None)
        if texture_filepath is None:
            error_message: str = f"Texture filepath for card <{self.suit_ascii}{self.name_ascii}> not provided."
            raise FileNotFoundError(error_message)

        # Returning:
        return texture_filepath
    
    
    @cached_property
    def texture_filepath_back(self) -> str:

        # Acquiring filename:
        texture_filepath: str = self.texturepack_back.texture_index[self.suit].get(self.name, None)
        if texture_filepath is None:
            error_message: str = f"Texture filepath for card <{self.suit_ascii}{self.name_ascii}> not provided."
            raise FileNotFoundError(error_message)

        # Returning:
        return texture_filepath
    
    
    @cached_property
    def texture_object_front(self) -> arcade.Texture:
        
        # Returning:
        return self.__texture_object_front
    
    
    @cached_property
    def texture_object_back(self) -> arcade.Texture:

        # Returning:
        return self.__texture_object_back
    
    
    @cached_property
    def texture_object_selected(self) -> arcade.Texture:
        
        # Selecting texture:
        texture_selected: texturepack.Texture = self.texture_object_front if self.state_revealed else self.texture_object_back

        # Returning:
        return texture_selected 
    
    
    def set_texturepack_front(self, texturepack_object: texturepack.TexturePack, update_texture: bool = True, 
                                    ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_texturepack(
                validate_value = texturepack_object
                )

        # Updating attribute:
        self.__texturepack_front = texturepack_object

        # Updating texture:
        if update_texture:
            self.load_texture_object_front(
                clear_cache = clear_cache
                )

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "texturepack_front",
                "texture_filepath_front",
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
    
    def set_texturepack_back(self, texturepack_object: texturepack.TexturePack, ignore_assertion: bool = False, 
                                   update_texture: bool = True, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_texturepack(
                validate_value = texturepack_object
                )

        # Updating attribute:
        self.__texturepack_back = texturepack_object

        # Updating texture:
        if update_texture:
            self.load_texture_object_back(
                clear_cache = clear_cache
                )

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "texturepack_back",
                "texture_filepath_back",
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
    
    
    def load_texture_object_front(self, clear_cache: bool = True) -> None:
        
        # Loading texture:
        texture: arcade.Texture = arcade.load_texture(
            file_path = self.texture_filepath_front
            )
        
        # Updating attribute:
        self.__texture_object_front = texture
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "texture_object_front",
                "render_rect",
                "render_width",
                "render_height",
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
    
    def load_texture_object_back(self, clear_cache: bool = True) -> None:

        # Loading texture:
        texture: arcade.Texture = arcade.load_texture(
            file_path = self.texture_filepath_back
            )

        # Updating attribute:
        self.__texture_object_back = texture

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "texture_object_back",
                "render_rect",
                "render_width",
                "render_height",
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        BOUNDARY CACHED PROPERTIES AND METHODS
    
    """
    
    
    @property
    def boundary_showcase(self) -> bool:
        
        # Checking if card is showcased:
        boundary_showcase: bool = bool(
            self.location == context.CARD_LOCATION.DECK and
            self.location_index == 0 or
            bool(
                SESSION.GAME_MODE_SECRET and 
                self.__location_index == 1
                )
            )
        
        # Returning:
        return boundary_showcase
    
    
    @cached_property
    def boundary_left(self) -> int:
        
        # Calculating showcase boundary:
        if self.boundary_showcase:
            boundary: int = int(
                self.coordinate_x - 
                self.render_height / 2
                )
            
        # Calculating default boundary:
        else:
            boundary: int = int(
                self.coordinate_x - 
                self.render_width / 2
                )
        
        # Returning:
        return boundary


    @cached_property
    def boundary_right(self) -> int:
        
        # Calculating showcase boundary:
        if self.boundary_showcase:
            boundary: int = int(
                self.coordinate_x + 
                self.render_height / 2
                )

        # Calculating default boundary:
        else:
            boundary: int = int(
                self.coordinate_x + 
                self.render_width / 2
                )

        # Returning:
        return boundary


    @cached_property
    def boundary_top(self) -> int:
        
        # Calculating showcase boundary:
        if self.boundary_showcase:
            boundary: int = int(
                self.coordinate_y + 
                self.render_width / 2
                )

        # Calculating default boundary:
        else:
            boundary: int = int(
                self.coordinate_y + 
                self.render_height / 2
                )

        # Returning:
        return boundary


    @cached_property
    def boundary_bottom(self) -> int:

        # Calculating showcase boundary:
        if self.boundary_showcase:
            boundary: int = int(
                self.coordinate_y - 
                self.render_width / 2
                )

        # Calculating default boundary:
        else:
            boundary: int = int(
                self.coordinate_y -
                self.render_height / 2
                )

        # Returning:
        return boundary
    
    
    @cached_property
    def boundary_horizontal(self) -> range:
        
        # Collecting boundary values:
        boundary: range = range(
            self.boundary_left, 
            self.boundary_right + 1
            )

        # Returning:
        return boundary
    
    
    @cached_property
    def boundary_vertical(self) -> range:

        # Collecting boundary values:
        boundary: range = range(
            self.boundary_bottom, 
            self.boundary_top + 1
            )

        # Returning:
        return boundary


    @cached_property
    def boundary(self) -> tuple[range, range]:
        
        # Collecting boundary values:
        boundary: tuple[range, range] = (
            self.boundary_horizontal,
            self.boundary_vertical
            )

        # Returning:
        return boundary
    
    
    def reset_boundary(self) -> None:
            
        # Clearing cache:
        self.clear_cached_boundary_attributes()
        
    
    def hit_boundary(self, hit_coordinates: tuple[int, int], ignore_assertion: bool = False) -> bool:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = hit_coordinates,
                )
        
        # Unpacking coordinates:
        hit_coordinate_x, hit_coordinate_y = hit_coordinates
        
        # Checking if coordinates hit card object's boundary:
        hit_boundary: bool = bool(
            hit_coordinate_x in self.boundary_horizontal and
            hit_coordinate_y in self.boundary_vertical
            )

        # Returning:
        return hit_boundary

        
    def hit_boundary_value(self, hit_coordinates: tuple[int, int], ignore_assertion: bool = False) -> int:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = hit_coordinates,
                )
        
        # Unpacking coordinates:
        hit_coordinate_x, hit_coordinate_y = hit_coordinates
        
        # Calculating coordinate x difference:
        hit_boundary_value: int = int(hit_coordinate_x / self.boundary_left)
        
        # Returning:
        return hit_boundary_value
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        RENDER (SCALE) CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def render_scale(self) -> float:
        
        # Returning:
        return self.__render_scale
    
    
    @cached_property
    def render_scale_default(self) -> float:
        
        # Returning:
        return SETTINGS.CARD_RENDER_SCALE_DEFAULT
    
    
    @cached_property
    def render_scale_step_mod_default(self) -> float:
        
        # Returning:
        return SETTINGS.CARD_RENDER_SCALE_STEP_MOD_DEFAULT
    
    
    @cached_property
    def render_scale_selected(self) -> float:

        # Returning:
        return SETTINGS.CARD_RENDER_SCALE_SELECT
    

    @cached_property
    def render_scale_step_mod_selected(self) -> float:

        # Returning:
        return SETTINGS.CARD_RENDER_SCALE_STEP_MOD_SELECT
        
        
    def set_render_scale(self, set_value: float, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_render_scale(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__render_scale = set_value

        # Clearing cache:
        if clear_cache:
            
            # Clearing target cached property:
            cached_property: str = "render_scale"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
            # Clearing related cached properties:
            self.clear_cached_boundary_attributes()
            
    
    def set_render_scale_default(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.set_render_scale(
            set_value = SETTINGS.CARD_RENDER_SCALE_DEFAULT,
            ignore_assertion = False,
            clear_cache = clear_cache,
            )
        
        
    def set_render_scale_selected(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.set_render_scale(
            set_value = SETTINGS.CARD_RENDER_SCALE_SELECT,
            ignore_assertion = False,
            clear_cache = clear_cache,
            )
        
        
    def transition_render_scale(self, target_value: float, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_render_scale(
                validate_value = target_value
                )
            
        # Updating to selected state:
        if target_value == self.render_scale_selected:
            if self.render_scale != self.render_scale_step_mod_selected:
                step_amount: float = self.__render_scale * self.render_scale_step_mod_selected
                self.adjust_render_scale(
                    adjust_value = step_amount,
                    ignore_assertion = False,
                    clear_cache = False,
                    )
                if self.__render_scale > self.render_scale_selected:
                    self.__render_scale = self.render_scale_selected
                
        # Updating to default state:
        elif target_value == self.render_scale_default:
            if self.render_scale != self.render_scale_default:
                step_amount: float = self.__render_scale * self.render_scale_step_mod_default
                self.adjust_render_scale(
                    adjust_value = step_amount,
                    ignore_assertion = False,
                    clear_cache = False,
                    )
                if self.__render_scale < self.render_scale_default:
                    self.__render_scale = self.render_scale_default

        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_scale"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def adjust_render_scale(self, adjust_value: float, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_render_scale(
                validate_value = adjust_value
                )

        # Updating attribute:
        render_scale_adjusted: float = self.render_scale + adjust_value
        self.__render_scale = render_scale_adjusted

        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_scale"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        RENDER (ALPHA) CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def render_alpha(self) -> int:
        
        # Returning:
        return self.__render_alpha
    
    
    @cached_property
    def render_alpha_default(self) -> int:
        
        # Returning:
        return SETTINGS.CARD_RENDER_ALPHA_DEFAULT
    
    
    @cached_property
    def render_alpha_faded(self) -> int:

        # Returning:
        return SETTINGS.CARD_RENDER_ALPHA_FADE


    def set_render_alpha(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_render_alpha(
                validate_value = set_value
                )

        # Updating attribute:
        self.__render_alpha = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_alpha"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )


    def set_render_alpha_default(self, clear_cache: bool = True) -> None:

        # Updating attribute:
        self.set_render_alpha(
            set_value = SETTINGS.CARD_RENDER_ALPHA_DEFAULT,
            ignore_assertion = True,
            clear_cache = clear_cache,
            )
        
    
    def set_render_alpha_faded(self, clear_cache: bool = True) -> None:

        # Updating attribute:
        self.set_render_alpha(
            set_value = SETTINGS.CARD_RENDER_ALPHA_FADE,
            ignore_assertion = True,
            clear_cache = clear_cache,
            )
        
    
    def transition_render_alpha(self, target_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_render_alpha(
                validate_value = target_value
                )

        # Updating to faded state:
        if target_value == self.render_alpha_faded:
            if self.render_alpha != self.render_alpha_step_mod_faded:
                step_amount: int = self.__render_alpha * self.render_alpha_step_mod_faded
                self.adjust_render_alpha(
                    adjust_value = step_amount,
                    ignore_assertion = False,
                    clear_cache = False,
                    )
                if self.__render_alpha < self.render_alpha_faded:
                    self.__render_alpha = self.render_alpha_faded

        # Updating to default state:
        elif target_value == self.render_alpha_default:
            if self.render_alpha != self.render_alpha_step_mod_default:
                step_amount: int = self.__render_alpha * self.render_alpha_step_mod_default
                self.adjust_render_alpha(
                    adjust_value = step_amount,
                    ignore_assertion = False,
                    clear_cache = False,
                    )
                if self.__render_alpha > self.render_alpha_default:
                    self.__render_alpha = self.render_alpha_default
                    
        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_alpha"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def adjust_render_alpha(self, adjust_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = adjust_value,
                check_type = int,
                raise_error = True
                )
        
        # Updating attribute:
        render_alpha_adjusted: int = self.render_alpha + adjust_value
        self.__render_alpha = render_alpha_adjusted
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_alpha"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
        
            
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        RENDER (TILT) CACHED PROPERTIES AND METHODS
    
    """

    
    @cached_property
    def render_tilt(self) -> int:
        
        # Returning:
        return self.__render_tilt
    
    
    @cached_property
    def render_tilt_default(self) -> int:
        
        # Returning:
        return SETTINGS.CARD_RENDER_TILT_DEFAULT
    
    
    @cached_property
    def render_tilt_opp(self) -> int:

        # Returning:
        return SETTINGS.CARD_RENDER_TILT_OPP
    
    
    @cached_property
    def render_tilt_deck(self) -> int:
        
        # Returning:
        return SETTINGS.CARD_RENDER_TILT_DECK


    @cached_property
    def render_tilt_deck_bottom(self) -> int:
        
        # Returning:
        return SETTINGS.CARD_RENDER_TILT_DECK_BOTTOM
    
    
    @cached_property
    def render_tilt_random(self) -> int:
        
        # Generating a new random tilt angle:
        tilt_axis: int = random.choice(SETTINGS.CARD_RENDER_TILT_AXIS_LIST)
        tilt_angle_selected: int = random.randint(SETTINGS.CARD_RENDER_TILT_MIN, SETTINGS.CARD_RENDER_TILT_MAX)
        tilt_angle_random: int = tilt_axis * tilt_angle_selected
        
        # Returning:
        return tilt_angle_random
    
    
    @cached_property
    def render_tilt_step_in(self) -> float:
        
        # Returning:
        return SETTINGS.CARD_RENDER_TILT_STEP_IN
    
    
    @cached_property
    def render_tilt_step_out(self) -> float:

        # Returning:
        return SETTINGS.CARD_RENDER_TILT_STEP_OUT
    
    
    def set_render_tilt(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_render_tilt(
                validate_value = set_value,
                )
            
        # Updating attribute:
        self.__render_tilt = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_tilt"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            

    def set_render_tilt_default(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.set_render_tilt(
            set_value = self.render_tilt_default,
            ignore_assertion = True,
            clear_cache = clear_cache,
            )
        
    
    def set_render_tilt_random(self, clear_cache: bool = True) -> None:
        
        # Clearing previous use cache:
        cached_property: str = "render_tilt_random"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )

        # Updating attribute:
        self.set_render_tilt(
            set_value = self.render_tilt_random,
            ignore_assertion = True,
            clear_cache = clear_cache,
            )
        
        
    def transition_render_tilt(self, target_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_render_tilt(
                validate_value = target_value,
                )
        
        if target_value == self.render_tilt_default:
            step_amount: float = self.render_tilt_step_out
        else:
            step_amount: float = self.render_tilt_step_in
            
        # Calculating new value:
        adjust_value: int = abs(self.render_tilt - int(self.render_tilt * step_amount))
        if adjust_value == 0:
            adjust_value = 1
        if self.render_tilt > target_value:
            adjust_value = -adjust_value
        
        # Updating attribute:
        self.adjust_render_tilt(
            adjust_value = adjust_value,
            ignore_assertion = False,
            clear_cache = False,
            )
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_tilt"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
        
    
    def adjust_render_tilt(self, adjust_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = adjust_value,
                check_type = int,
                raise_error = True
                )

        # Updating attribute:
        render_tilt_adjusted: int = self.render_tilt + adjust_value
        self.__render_tilt = render_tilt_adjusted

        # Clearing cache:
        if clear_cache:
            cached_property: str = "render_tilt"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        OTHER RENDER CACHED PROPERTIES AND METHODS
    
    """


    @cached_property
    def render_rect(self) -> arcade.Rect:
        
        # Creating a rectnagle object:
        rect_object: arcade.Rect = arcade.XYWH(
            x = self.coordinate_x,
            y = self.coordinate_y,
            width = self.render_width,
            height = self.render_height
            )
        
        # Returning:
        return rect_object
    
    
    @cached_property
    def render_rect_color(self) -> context.RGB_Color:
        
        # Returning:
        return SETTINGS.CARD_RENDER_BG_COLOR
    
    
    @cached_property
    def render_width(self) -> int:
        
        # Calculating:
        render_width: int = int(SETTINGS.CARD_TEXTURE_WIDTH * self.render_scale)
        
        # Returning:
        return render_width
    
    
    @cached_property
    def render_height(self) -> int:
        
        # Calculating:
        render_height: int = int(SETTINGS.CARD_TEXTURE_HEIGHT * self.render_scale)

        # Returning:
        return render_height
    
    
    @cached_property
    def render_text(self) -> arcade.Text:
        
        # Creating text object:
        text: arcade.Text = arcade.Text(
            text = self.__repr__(),
            x = self.coordinate_x,
            y = int(self.coordinate_y - self.render_height / 2 - self.render_height / 8),
            color = SETTINGS.CARD_RENDER_TEXT_COLOR,
            font_size = SETTINGS.CARD_RENDER_TEXT_FONT_SIZE,
            font_name = SETTINGS.CARD_RENDER_TEXT_FONT_NAME,
            anchor_x = "center",
            anchor_y = "center",
            )
        
        # Returning:
        return text
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        STATE CACHED PROPERTIES AND METHODS
        
    """
    
    
    @cached_property
    def state_visible(self) -> bool:
        
        # Returning:
        return self.__state_visible
    
    
    @cached_property
    def state_revealed(self) -> bool:
        
        # Returning:
        return self.__state_revealed
    
    
    @cached_property
    def state_hovered(self) -> bool:
        
        # Returning:
        return self.__state_hovered
    
    
    @cached_property
    def state_selected(self) -> bool:
        
        # Returning:
        return self.__state_selected
    
    
    @cached_property
    def state_faded(self) -> bool:
        
        # Returning:
        return self.__state_faded
    
    
    @cached_property
    def state_idle(self) -> bool:
        
        # Checking:
        state_idle: bool = bool(
            self.coordinate_x == self.coordinate_x_expected and 
            self.coordinate_y == self.coordinate_y_expected and
            not self.state_hovered and
            not self.state_selected
            )

        # Returning:
        return state_idle
    
    
    def reset_state_global(self, clear_cache: bool = True) -> None:
        
        # Resetting:
        self.__state_visible: bool = False
        self.__state_revealed: bool = False
        self.__state_hovered: bool = False
        self.__state_selected: bool = False
        self.__state_faded: bool = False
        self.__state_playable: bool = False
        
        # Clearing cache:
        if clear_cache:
            self.clear_cached_state_attributes()
        

    def set_state_visible(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )
            
        # Updating attribute:
        self.__state_visible = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_visible"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    
    
    def switch_state_visible(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.__state_visible = not self.__state_visible

        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_visible"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )


    def set_state_revealed(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )
            
        # Updating attribute:
        self.__state_revealed = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "state_revealed",
                "texture_object_selected"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )


    def switch_state_revealed(self, clear_cache: bool = True) -> None:

        # Updating attribute:
        self.__state_revealed = not self.__state_revealed

        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_revealed"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_state_hovered(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__state_hovered = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "state_hovered",
                "state_idle"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute = cached_property_list
                )
            

    def switch_state_hovered(self, clear_cache: bool = True) -> None:

        # Updating attribute:
        self.__state_hovered = not self.__state_hovered

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "state_hovered",
                "state_idle"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute = cached_property_list
                )
            
    
    def set_state_selected(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__state_selected = set_value

        # Clearing cache:
        if clear_cache:
            if clear_cache:
                cached_property_list: tuple[str, ...] = (
                    "state_selected",
                    "state_idle"
                    )
                cache.clear_cached_property_list(
                    target_object = self,
                    target_attribute = cached_property_list
                    )
            
    
    def switch_state_selected(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.__state_selected = not self.__state_selected

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "state_selected",
                "state_idle"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute = cached_property_list
                )
            
            
    def set_state_faded(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_state(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__state_faded = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_faded"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def switch_state_faded(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        self.__state_faded = not self.state_faded
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_faded"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_state_playable(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__state_playable = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_playable"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    
    
    def switch_state_playable(self, clear_cache: bool = True) -> None:

        # Updating attribute:
        self.__state_playable = not self.__state_playable

        # Clearing cache:
        if clear_cache:
            cached_property: str = "state_playable"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        LOCATION CACHED PROPERTIES AND METHODS
        
    """
    
    
    @cached_property
    def location(self) -> str:
        """
        Card object's current location (general): "Table", "Hand", "Opponet", "Deck", or "Discard".
        
        Uses exclusively default values found in `context.CARD_LOCATION` class collection.
        
        Cached property. Can be flushed via `cache` script's `clear_cached_property` function, or cache-management methods 
        available to this class, or with `clear_cache` parameter in its setter method.
        
        Returns
        -------
        self.__location : `str`
            Card object's current location (general): `"Table"`, `"Hand"`, `"Opponet"`, `"Deck"`, or `"Discard"`.
        """
        
        # Returning:
        return self.__location
    
    
    @cached_property
    def __location_precalc_coordinates(self) -> dict[str, dict[int, tuple[int, int]]]:
        """
        Card object's precalculated coordinates in dictionary format available for three locations: "Deck", "Discard", and 
        "Table". Used for quick coordinates update on location change.
                
        Accessed by method `self.update_coordinates_location()` providing `self.location` on location change event, if location
        uses precalculated coordinates. This property is for internal use only!
        
        Cached. Cannot be cleared.
        
        Returns
        -------
        location_coordinates : `dict[str, dict[int, tuple[int, int]]]`
            Card object's precalculated coordinates in dictionary format: `{CARD_LOCATION.VALUE: {int: tuple[int, int]}}`.
        """

        # Compiling coordinates dictionary index:
        location_coordinates: dict[str, dict[int, tuple[int, int]]] = {
            context.CARD_LOCATION.TABLE: coordinates.LOCATION_TABLE_COORDINATES_INDEX,
            context.CARD_LOCATION.DECK: coordinates.LOCATION_DECK_COORDINATES_INDEX,
            context.CARD_LOCATION.DISCARD: coordinates.LOCATION_DISCARD_COORDINATES_INDEX,
            }
        
        # Returning:
        return location_coordinates
    
    
    def set_location(self, set_value: tuple[str, int], ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        """
        Sets new location value for card object.
        
        This method uses only default values found in `context.CARD_LOCATION` class collection, and will raise raise 
        `AssertionError` if its validate method `self.__validate_location()` is unable to assert parameter's validity. Its 
        validation can be skipped if `SESSION.ENABLE_ASSERTION` is disabled or if parameter `ignore_assertion` is flagged as
        `False`.
        
        Does not automatically update card object's coordinates. To do so, use method `self.update_coordinates_location()`
        and provide coordinates for `calculated_coordinates` parameter if location does not have precalculated set of 
        coordinates, such as "Hand" or "Opponent".
        
        Clears related cache, if parameter `clear_cache` is set to `True`.
        
        Parameters
        ----------
        set_value : `tuple[str, int]`
            New location value for card object in tuple collection format: `(CARD_LOCATION.VALUE, int)`.
        ignore_assertion : `bool`, optional
            If `True`, assertion control is ignored. The default is `False`.
        clear_cache : `bool`, optional
            If `True`, related cached properties are cleared. The default is `True`.
        """
        
        # Unpacking:
        set_location, set_location_index = set_value
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_location(
                validate_value = set_location
                )
            validate.validate_card_location_index(
                validate_value = set_location_index
                )
            
        # Updating attributes:
        self.__location = set_location
        self.__location_index = set_location_index
        
        # Clearing cache:
        if clear_cache:
            self.clear_cached_location_attributes()
        
    
    def set_location_hand(self, location_index: int = 0, clear_cache: bool = True) -> None:
        """
        Sets card object's location to "Hand" and updates its index value.
        
        Does not automatically update card object's coordinates. To do so, use method `self.update_coordinates_location()`
        and provide coordinates for `calculated_coordinates` parameter if location does not have precalculated set of 
        coordinates, such as "Hand" or "Opponent".
        
        While general location is handled internally, may raise `AssertionError` if its validate method 
        `self.__validate_location_index()` is unable to assert parameter's validity, mainly `location_index` paremeter. 
        Parameter `location_index` is optional, but expected to be an `int` type value in `range(0, SETTINGS.DECK_SIZE_MAX)`
        range (0 through 51).

        Clears related cache, if parameter `clear_cache` is set to `True`.
        
        Parameters
        ----------
        location_index : `int`, optional
            New index value for card object's location. The default is `0`.
        clear_cache : `bool`, optional
            If `True`, related cached properties are cleared. The default is `True`.
        """
        
        # Updating attribute:
        location_container: context.Location = (
            context.CARD_LOCATION.HAND, 
            location_index
            )
        self.set_location(
            set_value = (context.CARD_LOCATION.HAND, location_index),
            ignore_assertion = False,
            clear_cache = clear_cache
            )
        
    def set_location_deck(self, location_index: int = 0, clar_cache: bool = True) -> None:
        """
        Sets card object's location to "Deck" and updates its index value.
        
        Does not automatically update card object's coordinates. To do so, use method `self.update_coordinates_location()`
        and provide coordinates for `calculated_coordinates` parameter if location does not have precalculated set of 
        coordinates, such as "Hand" or "Opponent".
        
        While general location is handled internally, may raise `AssertionError` if its validate method 
        `self.__validate_location_index()` is unable to assert parameter's validity, mainly `location_index` paremeter. 
        Parameter `location_index` is optional, but expected to be an `int` type value in `range(0, SETTINGS.DECK_SIZE_MAX)`
        range (0 through 51).

        Clears related cache, if parameter `clear_cache` is set to `True`.
        
        Parameters
        ----------
        location_index : `int`, optional
            New index value for card object's location. The default is `0`.
        clear_cache : `bool`, optional
            If `True`, related cached properties are cleared. The default is `True`.
        """
        
        # Updating attribute:
        location_container: context.Location = (
            context.CARD_LOCATION.DECK, 
            location_index
            )
        self.set_location(
            set_value = location_container,
            ignore_assertion = False,
            clear_cache = clar_cache
            )
        
        
    def set_location_discard(self, location_index: int = 0, clear_cache: bool = True) -> None:
        """
        Sets card object's location to "Discard" and updates its index value.
        
        Does not automatically update card object's coordinates. To do so, use method `self.update_coordinates_location()`
        and provide coordinates for `calculated_coordinates` parameter if location does not have precalculated set of 
        coordinates, such as "Hand" or "Opponent".
        
        While general location is handled internally, may raise `AssertionError` if its validate method 
        `self.__validate_location_index()` is unable to assert parameter's validity, mainly `location_index` paremeter. 
        Parameter `location_index` is optional, but expected to be an `int` type value in `range(0, SETTINGS.DECK_SIZE_MAX)`
        range (0 through 51).

        Clears related cache, if parameter `clear_cache` is set to `True`.
        
        Parameters
        ----------
        location_index : `int`, optional
            New index value for card object's location. The default is `0`.
        clear_cache : `bool`, optional
            If `True`, related cached properties are cleared. The default is `True`.
        """

        # Updating attribute:
        location_container: context.Location = (
            context.CARD_LOCATION.DISCARD, 
            location_index
            )
        self.set_location(
            set_value = location_container,
            ignore_assertion = False,
            clear_cache = clear_cache
            )
        
    
    def set_location_table(self, location_index: int = 0, clear_cache: bool = True) -> None:
        """
        Sets card object's location to "Table" and updates its index value.
        
        Does not automatically update card object's coordinates. To do so, use method `self.update_coordinates_location()`
        and provide coordinates for `calculated_coordinates` parameter if location does not have precalculated set of 
        coordinates, such as "Hand" or "Opponent".
        
        While general location is handled internally, may raise `AssertionError` if its validate method 
        `self.__validate_location_index()` is unable to assert parameter's validity, mainly `location_index` paremeter. 
        Parameter `location_index` is optional, but should to be an `int` type value in `range(0, SETTINGS.DECK_SIZE_MAX)`
        range (0 through 51). Unique to "Table" location, it is expected to be in `range(0, 12)` range (0 through 11).

        Clears related cache, if parameter `clear_cache` is set to `True`.
        
        Parameters
        ----------
        location_index : `int`, optional
            New index value for card object's location. The default is `0`.
        clear_cache : `bool`, optional
            If `True`, related cached properties are cleared. The default is `True`.
        """
        
        # Updating attribute:
        location_container: context.Location = (
            context.CARD_LOCATION.DECK, 
            location_index
            )
        self.set_location(
            set_value = location_container,
            ignore_assertion = True,
            clear_cache = clear_cache
            )
        

    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        INDEX CACHED PROPERTIES AND METHODS
        
    """
    
    
    @cached_property
    def location_index(self) -> int:
        """
        Card object's current location index: integers 0 through 51.
        
        Location index is used to calculate coordinates of card on screen. While locations such as "Deck", "Discard" and "Table"
        use precalculated values based on all available index values (0 through 51), `Hand` controller calculates coordinates for
        locations "Hand" and "Opponent".
        
        For pile-type locations index simply shows it's position on stack (the lowest being the first or the closest to the table,
        and the highest being the last or the closes to the player). "Table" location uses stack system (pairs of 0-1, 2-3, 4-5, 
        ..., 10-11), where even numbers are bottom positions and odd numbers are top positions.
        
        Additionally, Table location uses these index values to determine offset coordinates values, and pile-type locations use
        them to slightly shift coordinates to top-right corner to create a 3D visual effect of the stack for better readability 
        (being able to visually determine approximate size of a pile).
        
        Cached property. Can be flushed via `cache` script's `clear_cached_property` function, or cache-management methods 
        available to this class, or with `clear_cache` parameter in its setter method.
        
        Returns
        -------
        self.__location_index : `int`
            Card object's current location index.
        """

        # Returning:
        return self.__location_index


    def set_location_index(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        """
        Sets a new location index for card object.
        
        This method may raise `AssertionError` if its validate method `self.__validate_location_index()` is unable to assert 
        parameter's validity. Its validation can be skipped if `SESSION.ENABLE_ASSERTION` is disabled or if parameter 
        `ignore_assertion` is flagged as `False`.
        
        Does not automatically update card object's coordinates. To do so, use method `self.update_coordinates_location()`
        and provide coordinates for `calculated_coordinates` parameter if location does not have precalculated set of 
        coordinates, such as "Hand" or "Opponent".
        
        Clears related cache, if parameter `clear_cache` is set to `True`.
        
        Parameters
        ----------
        set_value : `int`
            New location index value for card object.
        ignore_assertion : `bool`, optional
            If `True`, assertion control is ignored. The default is `False`.
        clear_cache : `bool`, optional
            If `True`, related cached properties are cleared. The default is `True`.
        
        """

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_location_index(
                validate_value = set_value
                )

        # Updating attribute:
        self.__location_index = set_value

        # Clearing cache:
        cached_property: str = "location_index"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        ID CACHED PROPERTIES AND METHODS
        
    """
    
    
    @cached_property
    def id(self) -> int:
        """
        Card object's unique identifier.
        
        Used to track individual cards through multiple games.
        
        Cached with `functools` module's `cached_property` decorator. Can be flushed via `utilities.scripts.cache` module's
        `clear_cached_property` function, or cache-management methods available to this class, or with `clear_cache` parameter
        in its setter method.

        Returns
        -------
        self.__id : `int`
            Card object's unique identifier.
        """
        
        # Returning:
        return self.__id
    
    
    @cached_property
    def id_repr(self) -> str:
        """
        Card object's unique identifier formatted as string.
        
        Converts `self.id` to be represented as a `str` in `#00000X` format.

        Cached with `functools` module's `cached_property` decorator. Can be flushed via `utilities.scripts.cache` module's
        `clear_cached_property` function, or cache-management methods available to this class, or with `clear_cache` parameter
        in its setter method.

        Returns
        -------
        id_repr : `str`
            Card object's unique identifier formatted as string.
        """
        
        # Formatting to string:
        id_repr: str = f"#{self.id:06d}"
        
        # Returning:
        return id_repr
    
    
    def set_id(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        """
        Sets a new unique identifier for card object.

        This method may raise `AssertionError` if its validate method `self.__validate_id()` is unable to assert parameter's
        validity. Its validation can be skipped if `SESSION.ENABLE_ASSERTION` is disabled or if parameter `ignore_assertion`
        is flagged as `False`.

        Clears related cache, if parameter `clear_cache` is set to `True`.

        Parameters
        ----------
        set_value : `int`
            New unique identifier value for card object.
        ignore_assertion : `bool`, optional
            If `True`, assertion control is ignored. The default is `False`.
        clear_cache : `bool`, optional
            If `True`, related cached properties are cleared. The default is `True`.
        """

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_id(
                validate_value = set_value
                )
            
        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "id",
                sentinel_value = None,
                raise_error = True
                )

        # Updating attribute:
        self.__id = set_value

        # Clearing cache:
        if clear_cache:
            self.clear_cached_id_attributes()
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        ADDED INDEX CACHED PROPERTIES AND METHODS
        
    """
    
    
    @cached_property
    def added_index(self) -> int:
        """
        Card object's index representing its position (order) added to new container (Hand, Deck, or Discard piles). The lower 
        it is the "older" the card is, the higher it is the "newer" the card is.
        
        Used for sorting methods available to `Hand` controller class object.

        Cached with `functools` module's `cached_property` decorator. Can be flushed via `utilities.scripts.cache` module's
        `clear_cached_property` function, or cache-management methods available to this class, or with `clear_cache` parameter
        in its setter method.
        
        Returns
        -------
        self.__added_index : `int`
            Card object's index representing its position (order) added to new container (Hand, Deck, or Discard piles).
        """
        
        # Returning:
        return self.__added_index
    
    
    def set_added_index(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        """
        Sets a new index representing card object's position (order) added to new container (Hand, Deck, or Discard piles).
        
        Called by container controllers when card object changes its location and is added to a different container. Added index 
        is determined by controller based on number of cards previously present in the container. The lower the index is the 
        "older" the card is, the higher it is the "newer" the card is.

        This method may raise `AssertionError` if its validate method `self.__validate_added()` is unable to assert parameter's
        validity. Its validation can be skipped if `SESSION.ENABLE_ASSERTION` is disabled or if parameter `ignore_assertion`
        is flagged as `False`.

        Clears related cache, if parameter `clear_cache` is set to `True`.
        
        Parameters
        ----------
        set_value : `int`
            New index representing card object's position (order) added to new container (Hand, Deck, or Discard piles).
        """

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_added_index(
                validate_value = set_value
                )

        # Updating attribute:
        self.__added_index = set_value

        # Clearing cache:
        cached_property: str = "added_index"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        

    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DISPLAY METHODS
        
    """
    
    
    def display(self) -> None:
        """
        Renders the card object's texture on screen. Used by `Gameshell` object's `on_draw` method within loop logic. 
        
        Uses predefined `arcade.Rect` object, card object's `self.texture_object_selected` texture based on its state and other
        render properties.
        """
        
        # Rendering:
        arcade.draw_texture_rect(
            texture = self.texture_object_selected,
            rect = self.render_rect,
            angle = self.render_tilt,
            alpha = self.render_alpha,
            )


    def display_info(self) -> None:
        """
        Renders the card object's debug info on screen. Used by `Gameshell` object's `on_draw` method within loop logic. 
        
        Uses predefined `arcade.Text` object and other core attributes values available to the card. Calls 
        `self.render_text.draw()` method to render text object on screen.
        """
        
        # Calling text object's draw method:
        self.render_text.draw()
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        JOB METHODS
        
    """
    
    
    def slide(self, target_coordinates: tuple[int, int], speed_modifier: float, 
                    ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        """
        Slides card object's position to new coordinates provided in `target_coordinates` parameter. Uses `speed_modifier` to 
        determine how fast the card should slide to new coordinates. 
        
        Parameter `speed_modifier` cannot be less than default min value in `SETTINGS`, otherwise the card will never reach its
        destination. If `speed_modifier` is set to `0.00` the slide will finish its job instantly. 
        
        Used by `Gameshell` object's `on_update` method within loop logic.
        
        Calls card object's native method `set_coordinates_position()` to update card's coordinates values. This and other similar
        methods may raise `AssertionError` if `SESSION.ENABLE_ASSERTION` is set to `True` and coordinates container provided does
        not pass validation and assertion checks. Precalculated coordinates do not required assertion control.
        
        Clears related cache, if parameter `clear_cache` is set to `True`.
        
        Parameters
        ----------
        target_coordinates : `tuple[int, int]`
            Coordinates tuple collection to slide card object to.
        speed_modifier : `float`
            Speed modifier to determine how fast the card should slide to new coordinates.
        ignore_assertion : `bool` = `True`
            Flag to determine if assertion control should be ignored. If set to `True`, assertion control will be ignored.
        clear_cache : `bool` = `True`
            Flag to determine if related cache should be cleared. If set to `True`, related cache will be cleared.
        """
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = target_coordinates
                )
            
        # TODO: Continue!
        
        
    def update_coordinates_location(self, calculated_coordinates: tuple[int, int] | None, clear_cache: bool = True) -> None:
        """
        Updated coordinates based on card's location and `calculated_coordinates` parameter provided.
        
        If `calculated_coordinates` parameter is set to None, assumes that card's current location is either "Deck", "Discard", or
        "Table", allowing it to load precaclulcated coordinates values from `self.__location_precalc_coordinates` dictionary index
        cached property. Otherwise, assumes that `calculated_coordinates` parameter is provided, allowing it to update card's
        coordinates based on provided value.
        
        Parameter `calculated_coordinates` is calculated and provided by `Hand` controller and is mutable, based on card 
        object's current location index in hand. Hand controller checks how many cards there are in its container and based on 
        its value and `SETTINGS.__AREA_HAND_WIDTH` (and other predetermined surface restrictions) calculates new coordinates for
        each card available.
        
        Calls card object's native method `set_coordinates_position` to update card's coordinates values. This and other similar
        methods may raise `AssertionError` if `SESSION.ENABLE_ASSERTION` is set to `True` and coordinates container provided does
        not pass validation and assertion checks. Precalculated coordinates do not required assertion control.
        
        Parameters
        ----------
        calculated_coordinates : `tuple[int, int]` | `None`
            Coordinates to update card's position with. If set to None, assumes that card's current location is either "Deck",
            "Discard", or "Table", allowing it to load precaclulcated coordinates values from `self.__location_precalc_coordinates`
        clear_cache : `bool` = True
            If set to True, clears cached properties and attributes.
        """
        
        # Loading precalculated coordinates:
        if calculated_coordinates is None:
            coordinates_precaculated: bool = True if self.location in self.__location_precalc_coordinates.keys() else False
            if coordinates_precaculated:
                
                # Updating coordinates (position):
                coordinates_position: tuple[int, int] = self.__location_precalc_coordinates[self.location][self.location_index]
                self.set_coordinates_position(
                    set_value = coordinates_position,
                    ignore_assertion = True,
                    clear_cache = clear_cache
                    )
        
        # Updating coordinates based on provided value:
        else:

            # Updating coordinates (position):
            self.set_coordinates_position(
                set_value = calculated_coordinates,
                ignore_assertion = False,
                clear_cache = clear_cache
                )
            
    
    def update_coordinates_state(self, clear_cache: bool = True) -> None:
        """
        Updates `coordinates_expected` cached properties based on card object's state.
        
        If card object is in "Selected" state, updates `coordinates_expected` cached property to `coordinates_selected` value, if
        card object is in "Hovered" state, updates `coordinates_expected` cached property to `coordinates_hovered` value, and if
        card object is in "Default" (on in-position) state, updates `coordinates_expected` cached property to 
        `coordinates_position` value, expecting it to be in its place.
        
        This method takes priority in checking states, as "selected" state takes the highest priority due to user's mouse 
        movement. It is technically possible to have a card object selected on screen and have it being "hovered" over at the 
        same time, if cursor lingers. Thus, it first checks `self.state_selected`, then `self.state_hovered`, and only then 
        attempts to reset `self.coordinates_expected` to `self.coordinates_position`.

        Calls card object's native method `set_coordinates_expected` to update card's coordinates values. This and other similar
        methods may raise `AssertionError` if `SESSION.ENABLE_ASSERTION` is set to `True` and coordinates container provided does
        not pass validation and assertion checks. Precalculated coordinates do not required assertion control, thus parameters
        `ignore_assertion` are set to `True`. Adjust them for debug purposes only.

        Parameters
        ----------
        clear_cache : `bool` = `True`
            If set to True, clears cached properties and attributes.
        """
        
        # Selected state:
        if self.state_selected:
            
            # Checking if expected coordinates are set to selected coordinates:
            if self.coordinates_expected != self.coordinates_selected:
                self.set_coordinates_expected(
                    set_value = self.coordinates_selected,
                    ignore_assertion = True,
                    clear_cache = clear_cache
                    )
        
        # Hovered state:
        elif self.state_hovered:
            
            # Checking if expected coordinates are set to hover coordinates:
            if self.coordinates_expected != self.coordinates_hovered:
                self.set_coordinates_expected(
                    set_value = self.coordinates_hovered,
                    ignore_assertion = True,
                    clear_cache = clear_cache
                    )

        # Default (in position) state:
        else:
            
            # Checking if expected coordinates are set to default (in position) coordinates:
            if self.coordinates_expected != self.coordinates_position:
                self.set_coordinates_expected(
                    set_value = self.coordinates_position,
                    ignore_assertion = True,
                    clear_cache = clear_cache
                    )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        JOB METHODS
        
    """
    
    
    def auto_scale(self) -> None:
        """
        Scaler method. Automatically adjusts card object's scale values based on its state and available scale values.
        
        If card object is in "Selected" state, adjusts `render_scale` cached property to `render_scale_selected` value, and if
        card object is in "Default" (on in-position) state, adjusts `render_scale` cached property to `render_scale_default` 
        value.
        
        Used by `Gameshell` object via `on_update()` method to automatically adjust card object's scale values within game logic 
        loop.
        
        Calls card object's native method `transition_render_scale()` to update card's scale values. This and other similar
        methods may raise `AssertionError` if `SESSION.ENABLE_ASSERTION` is set to `True` and scale value provided does not
        pass validation and assertion checks. Precalculated scale values do not required assertion control, thus parameters
        `ignore_assertion` are set to `True`. Adjust them for debug purposes only.
        """
        
        # Preparing flag variables:
        clear_cache: bool = False
        job_required: bool = False
        
        # Checking selected states:
        if self.state_selected:
            if self.render_scale != self.render_scale_selected:
                render_scale_target: float = self.render_scale_selected
                job_required = True
                
        # Checking default state:
        else:
            if self.render_scale != self.render_scale_default:
                render_scale_target: float = self.render_scale_default
                job_required = True
            
        # Running job:
        if job_required:
            render_scale_prev: float = self.render_scale
            self.transition_render_scale(
                target_value = render_scale_target,
                ignore_assertion = True,
                clear_cache = False,
                )
            clear_cache = self.__render_scale != render_scale_prev
                
            # Clearing cache, if required:
            if clear_cache:
                cached_property_list: tuple[str, ...] = (
                    "render_scale",
                    "render_rect",
                    "render_text"
                    )
                cache.clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = cached_property_list
                    )
                
    
    def auto_tilt(self, instant_mode: bool = False) -> None:
        """
        Tilter method. Automatically adjusts card object's tilt values based on its state and available tilt values.

        If card object is in "Idle" state, adjusts `render_tilt` cached property to `render_tilt_random` value, and if
        card object is in "Default" (on in-position) state, adjusts `render_tilt` cached property to `render_tilt_default`
        value. If card object is in "Opponent" state, adjusts `render_tilt` cached property to `render_tilt_opp` value.

        Used by `Gameshell` object via `on_update()` method to automatically adjust card object's tilt values within game logic 
        loop.
        
        Calls card object's native method `transition_render_tilt()` to update card's tilt values. This and other similar
        methods may raise `AssertionError` if `SESSION.ENABLE_ASSERTION` is set to `True` and tilt value provided does not
        pass validation and assertion checks. Precalculated tilt values do not required assertion control, thus parameters
        `ignore_assertion` are set to `True`. Adjust them for debug purposes only.
        """
        
        # Preparing flag variables:
        clear_cache: bool = False
        job_required: bool = False
        
        # Checking hovered or selected states:
        if self.state_idle:
            if self.render_tilt != self.render_tilt_random:
                render_tilt_target: int = self.render_tilt_random
                job_required = True
                
        # Checking default state:
        else:
            if self.location == context.CARD_LOCATION.OPPONENT:
                if self.render_tilt != self.render_tilt_opp:
                    render_tilt_target: int = self.render_tilt_opp
                    job_required = True
            elif self.location == context.CARD_LOCATION.PLAYER:
                if self.render_tilt != self.render_tilt_default:
                    render_tilt_target: int = self.render_tilt_default
                    job_required = True

        # Running job:
        if job_required:
            render_tilt_prev: int = self.render_tilt
            if instant_mode:
                self.set_render_tilt(
                    set_value = render_tilt_target,
                    ignore_assertion = True,
                    clear_cache = False,
                    )
            else:
                self.transition_render_tilt(
                    target_value = render_tilt_target,
                    ignore_assertion = True,
                    clear_cache = False,
                    )
            clear_cache = self.__render_tilt != render_tilt_prev
            
            # Clearing cache, if required:
            if clear_cache:
                cached_property_list: tuple[str, ...] = (
                    "render_tilt",
                    )  
                cache.clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = cached_property_list
                    )
                
                # Checking if old randomly generated tilt angle needs to be cleared:
                if not self.state_selected and not self.state_hovered:
                    if self.render_tilt == render_tilt_target:
                        cached_property: str = "render_tilt_random"
                        cache.clear_cached_property(
                            target_object = self,
                            target_attribute = cached_property
                            )


    def auto_alpha(self) -> None:
        """
        Alpha controller method. Automatically adjusts card object's alpha values based on its state.

        If card object is in "Faded" state, adjusts `render_alpha` cached property to `render_alpha_faded` value. If card
        object is in "Default" (on in-position) state, adjusts `render_alpha` cached property to `render_alpha_default`
        value.
        
        Used by `Gameshell` object via `on_update()` method to automatically adjust card object's alpha values within game logic
        loop.
        
        Calls card object's native method `transition_render_alpha()` to update card's alpha values. This and other similar
        methods may raise `AssertionError` if `SESSION.ENABLE_ASSERTION` is set to `True` and alpha value provided does not
        pass validation and assertion checks. Precalculated alpha values do not required assertion control, thus parameters
        `ignore_assertion` are set to `True`. Adjust them for debug purposes only.
        """

        # Preparing flag variables:
        clear_cache: bool = False
        job_required: bool = False
        
        # Checking faded state:
        if self.state_faded:
            if self.render_alpha != self.render_alpha_faded:
                render_alpha_target: int = self.render_alpha_faded
                job_required = True

        # Checking default state:
        else:
            if self.render_alpha != self.render_alpha_default:
                render_alpha_target: int = self.render_alpha_default
                job_required = True

        # Running job:
        if job_required:
            render_alpha_prev: int = self.render_alpha
            self.transition_render_alpha(
                target_value = render_alpha_target,
                ignore_assertion = True,
                clear_cache = False,
                )
            clear_cache = self.__render_alpha != render_alpha_prev
            
            # Clearing cache, if required:
            if clear_cache:
                cached_property_list: tuple[str, ...] = (
                    "render_alpha",
                    )  
                cache.clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = cached_property_list
                    )

