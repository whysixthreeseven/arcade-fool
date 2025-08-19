# Annotation import:
from __future__ import annotations

# Cache-related modules and scripts import:
from game.collections.scripts import clear_cached_property
from functools import cached_property

# System-management library import:
import os

# Random library import:
import random

# Arcade-related import:
import arcade
from arcade import Texture, Rect

# Settings and variables import list:
from game.variables import *
from game.settings import *

# Developer session values:
from game.session import (
    DEV_ENABLE_ASSERTION,
    DEV_ENABLE_ECHO,
    )

# Assertion functions import:
from game.collections.scripts import (
    assert_value_is_default,
    assert_value_is_valid_type,
    assert_value_in_valid_range,
    )


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CARD CLASS BLOCK

"""


class Card:
    """
    ## About

    Card object with suit and type (core), position, state on screen and in-game, coordinates on
    screen, boundary, and texture object and texture-related attributes. In a card game, a Card is
    arguably the most import piece of the game, thus this class has a lot to do and therefore a lot
    to offer.

    As there may be up to (all) 36 cards rendered and interacted with on the screen at the same 
    time, this class features most of its properties as cached properties via functools' wrapper.
    Most of the cached properties can be cleared, however some cannot and remain as they were 
    generated for the first time until the card is removed from game (and/or garbage collected).

    ## Life-cycle

    Cards are generated, put (set position) into a deck (deck controller's container). From there,
    they are "drawn" (or dealt) to hands (player controller's container). From there they are being
    updated, compared with other card objects on the table, and played (moved to table controller's
    container). From the table the card may be swept back to a hand (player controller) or to a 
    discard pile (discard controller's container). And that is a life cycle of a card.

    ## Type value

    All the 36 cards are unique and there cannot be duplicates. The lowest value card is a Six, and
    the highest value card is an Ace. Cards value start from 6 and increases by 1 with each rank, 
    thus, Six's value is 6, while Jack's value is 11. Trump suit status increases the value of a 
    given card by its modifier (100 by default). Thus, a Six of Hearts (non-trump) will have a 
    value of 6, while Six of Spades (trump) will have a value of 106. A Six of Spades will beat
    all cards that are non-trump cards, but will follow the hierarchy within the trump suit.

    Cards are compared to one another by their value, should they have the same suit (Hearts, 
    Diamonds, Clubs or Spades), or should one of the cards (compared with, not to) be a trump card
    (have its suit declared as trump suit).

    ## Rendering

    While rendered static and upright most of the time on the screen, a card can be interacted with
    by being hovered over or selected on click. When hovered over it may "slide" on screen 
    depending on its location, e.g. cards in hand will slide up a little to stand out when hovered
    over, which is helpful when having one too many cards in hand; cards on the table (top stack)
    will move aside revealing the card upder them, which is helpful when one needs to see what 
    card was played.
    """

    # Default (expected) card types list:
    CARD_TYPE_LIST: tuple[str, ...] = (
        VAR_CARD_TYPE_SIX,                  # 6
        VAR_CARD_TYPE_SEVEN,                # 7
        VAR_CARD_TYPE_EIGHT,                # 8
        VAR_CARD_TYPE_NINE,                 # 9
        VAR_CARD_TYPE_TEN,                  # 10
        VAR_CARD_TYPE_JACK,                 # J
        VAR_CARD_TYPE_QUEEN,                # Q
        VAR_CARD_TYPE_KING,                 # K
        VAR_CARD_TYPE_ACE                   # A
        )

    # Default card type value index:
    CARD_TYPE_VALUE_INDEX: dict[str, int] = {
        VAR_CARD_TYPE_SIX:   6,
        VAR_CARD_TYPE_SEVEN: 7,
        VAR_CARD_TYPE_EIGHT: 8,
        VAR_CARD_TYPE_NINE:  9,
        VAR_CARD_TYPE_TEN:   10,
        VAR_CARD_TYPE_JACK:  11,
        VAR_CARD_TYPE_QUEEN: 12,
        VAR_CARD_TYPE_KING:  13,
        VAR_CARD_TYPE_ACE:   14
        }
    CARD_TRUMP_VALUE_BONUS: int = 100

    # Card default (expected) suit list:
    CARD_SUIT_LIST: tuple[str, ...] = (
        VAR_CARD_SUIT_HEARTS,               # ♡
        VAR_CARD_SUIT_DIAMONDS,             # ♢
        VAR_CARD_SUIT_CLUBS,                # ♧
        VAR_CARD_SUIT_SPADES                # ♤
        )
    
    # Card suit color index:
    CARD_SUIT_COLOR_INDEX: dict[str, str] = {
        VAR_CARD_SUIT_HEARTS:   VAR_CARD_SUIT_COLOR_RED,
        VAR_CARD_SUIT_DIAMONDS: VAR_CARD_SUIT_COLOR_RED,
        VAR_CARD_SUIT_CLUBS:    VAR_CARD_SUIT_COLOR_BLACK,
        VAR_CARD_SUIT_SPADES:   VAR_CARD_SUIT_COLOR_BLACK
        }
    
    # Card suit unicode index:
    CARD_SUIT_UNICODE_INDEX: dict[str, str] = {
        VAR_CARD_SUIT_HEARTS:   "♡",
        VAR_CARD_SUIT_DIAMONDS: "♢",
        VAR_CARD_SUIT_CLUBS:    "♧",
        VAR_CARD_SUIT_SPADES:   "♤"
        }
    

    def __init__(self) -> None:

        # Core attributes:
        self.__card_suit: str = VAR_CARD_SUIT_NOT_SET
        self.__card_type: str = VAR_CARD_TYPE_NOT_SET

        # Position attributes:
        self.__position_added:   int | None = None
        self.__position_hand:    int | None = None
        self.__position_table:   int | None = None
        self.__position_stack:   int | None = None
        self.__position_deck:    int | None = None
        self.__position_discard: int | None = None

        # State attributes:
        self.__state_trump:    bool = False
        self.__state_playable: bool = False
        self.__state_revealed: bool = False
        self.__state_selected: bool = False
        self.__state_hovered:  bool = False

        # Coordinates attributes:
        self.__coordinate_x: int = 0
        self.__coordinate_y: int = 0

        # Texture attributes:
        self.__texture_pack:               str | None = None
        self.__texture_cover_filename:     str | None = None
        self.__texture_cover_filepath:     str | None = None
        self.__texture_cover_object:   Texture | None = None
        self.__texture_front_filename:     str | None = None
        self.__texture_front_filepath:     str | None = None
        self.__texture_front_object:   Texture | None = None

    
    def __repr__(self) -> str:
        """
        Overwrites native __repr__ magic method.

        Constructs a string in format SUIT_UNICODE+TYPE_UNICODE @LOCATION -> "♡J @table".

        Used to print card object to console when debugging or (not implemented yet) when rendering
        hints during hover events.

        :return str: (If card is fully initialized) If ready, formatted string repr value in a 
            readable format, e.g. "♡J @table". (If not initialized) Otherwise "Card (not set)".

        """
        
        # Generating a repr string:
        repr_string: str = "Card (not set)"
        if self.state_ready:
            repr_string: str = "{card_suit_unicode}{card_type_unicode} @{location_repr}".format(
                card_suit_unicode = self.card_suit_unicode,
                card_type_unicode = self.card_type_unicode,
                location_repr = self.location_repr.lower()
                )
        
        # Returning:
        return repr_string


    def __gt__(self, card_object: Card) -> bool:
        """
        Overwrites native __gt__ magic method. 
        
        Compares two card objects and determines if this card object has a greater type value, 
        should both be of the same suit (or this card object is a trump card). 
        
        Returns True, if cards can be compared and this card has a greater type value. Example: 
        A card ♤K has a greater type value than ♤6, thus returns True. Or a card ♧8 has a 
        different suit than ♡K, but it is a trump card, thus we compare their type value; trump
        cards' value is modified and is significantly higher than non-trump cards, therefore ♧8 
        trump card's value is greater than ♡K, thus returns True.
        
        False, if cards cannot be compared due to suit differences (and/or this card is not a 
        trump card type), or if this card has a lesser type value.

        Used when checking if a card is playable while defending by comparing cards on the table
        (bottom stack position) with cards in hand. If a card in hand appears to be of a greater 
        type value than a given card on the table, it may be set as playable (check Card class).

        :param Card card_object: (Implicit) Can only be compared to same instance type objects.

        :return bool: Boolean result of type value comparison. If able to compare and type value 
            is greater, returns True. If failed to compare, or type value is lesser, returns False.
        """
        
        # Checking if two cards can be compared (trump or same suit values):
        eval_result: bool = False
        if self.state_trump or self.card_suit == card_object.set_card_suit:

            # Comparing:
            eval_result: bool = self.card_type_value > card_object.card_type_value

        # Returning:
        return eval_result


    def __lt__(self, card_object: Card) -> bool:
        """
        Overwrites native __lt__ magic method. 
        
        Compares two card objects and determines if this card object has a lesser type value, 
        should both be of the same suit. This method ignore trump state, as it is irrelevant.
        
        Returns True, if cards can be compared and this card has a lesser type value. Example: 
        A card ♤6 has a lesser type value than ♤K, thus returns True. 
        
        False, if cards cannot be compared due to suit differences or if this card has a lesser 
        type value.

        :param Card card_object: (Implicit) Can only be compared to same instance type objects.

        :return bool: Boolean result of type value comparison. If able to compare and type value 
            is lesser, returns True. If failed to compare, or type value is greater, returns False.
        """
        
        # Checking if two cards can be compared:
        eval_result: bool = False
        if self.card_suit == card_object.set_card_suit:

            # Comparing:
            eval_result: bool = self.card_type_value < card_object.card_type_value

        # Returning:
        return eval_result


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CLASS STATIC METHODS BLOCK
    
    Card's static methods that are available across the module and/or project, giving other scripts
    and option to create card objects via a method with all required setters onboard. Made to be a 
    static method to avoid circular import error via script.py file, and to avoid creating more 
    setter methods and checks.

    """


    @staticmethod
    def create_card_object(init_suit: str, init_type: str) -> Card:
        """
        Creates and returns a card object with a set suit and type attributes, and loaded cover
        and front texture files based on the default texture pack. Made to be a static method to
        avoid circular import error via script.py file, and to avoid creating more setter methods 
        and checks.

        :param str init_suit: Suit string value, must be a default value, e.g. "CARD_SUIT_HEARTS".
        :param str init_type: Type string value, must be a default value, e.g. "CARD_TYPE_SIX".

        :return Card: Card class-type object.
        """

        # Creating a card:
        card_object: Card = Card()
        
        # Setting core attributes:
        card_object.set_card_suit(
            set_value = init_suit
            )
        card_object.set_card_type(
            set_value = init_type
            )
        
        # Loading a default texture pack:
        card_object.set_texture_pack(
            set_value = VAR_CARD_TEXTURE_PACK_DEFAULT
            )

        # Returning:
        return card_object
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    MISC METHODS BLOCK
    
    Miscellaneous private methods related to card object designed to reduce code repetition and 
    redundancy, or to simplify several for-loops when clearing cache with a function imported from
    scripts.py.

    """


    def __convert_to_repr(self, attribute_string: str) -> str:
        """
        Converts a default (stored in variables.py script) variable string to its formatted repr 
        (or display/render-friendly) version by removing the variable tag and formatting the string.
        Example: "CARD_SUIT_HEARTS" -> "Hearts"

        :param str attribute_string: Default variable string, e.g. "CARD_SUIT_HEARTS"

        :return str: Tagless formatted attribute string value, e.g. "CARD_SUIT_HEARTS" -> "Hearts"
        """

        # Splitting and formatting:
        char_split: str = "_"
        repr_string_tagless:   str = attribute_string.split(char_split)[-1]
        repr_string_formatted: str = repr_string_tagless.capitalize()

        # Returning:
        return repr_string_formatted
    

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
    their block's cachced property lists (e.g. __cached_suit_property_list would return all the 
    cached property (attribute) string value names to clear via a different clear cache function).

    These tuple containers are stored as cached properties within the class and not made as 
    wrappers due to some of the setter methods optional cache clearing policy and other methods 
    aiming to clear only one (or two) cached property (attribute) at a time, but not the whole 
    block, e.g. set_coordinate_x will only clear a coordinate_x cached property (and other within
    a different block).

    """


    @cached_property
    def __cached_suit_property_list(self) -> tuple[str, ...]:
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
            "card_suit",
            "card_suit_repr",
            "card_suit_color",
            "card_suit_color_repr",
            "card_suit_unicode"
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_type_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache. 
        
        Cached. Cannot be cleared.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g. for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "card_type",
            "card_type_repr",
            "card_type_value",
            "card_type_unicode"
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_position_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache. 
        
        Cached. Cannot be cleared.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g. for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "position_added",
            "position_hand",
            "position_table",
            "position_stack",
            "position_deck",
            "position_discard",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_location_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache.

        Cached. Cannot be cleared.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g. for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "location",
            "location_repr",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_state_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache.

        Cached. Cannot be cleared.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g. for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "state_trump",
            "state_playable",
            "state_revealed",
            "state_selected",
            "state_hovered",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_texture_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache.

        Cached. Cannot be cleared.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g. for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "texture_cover_filename",
            "texture_cover_filepath",
            "texture_cover_object",
            "texture_front_filename",
            "texture_front_filepath",
            "texture_front_object",
            "texture_pack",
            "texture_pack_repr",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_coordinates_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache.

        Cached. Cannot be cleared.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g. for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "coordinate_x",
            "coordinate_y",
            "coordinate_y_hand",
            "coordinate_y_hand_hover",
            "coordinates",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_boundary_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache.

        Cached. Cannot be cleared.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g. for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "boundary_left",
            "boundary_right",
            "boundary_bottom",
            "boundary_top",
            "boundary_range_horizontal",
            "boundary_range_vertical",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_render_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache.

        Cached. Cannot be cleared.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g. for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "render_scale",
            "render_angle",
            "render_width",
            "render_height",
            "render_texture",
            )
        
        # Returning:
        return cached_property_list

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    SUIT METHODS AND PROPERTIES BLOCK
    
    Suit-related methods and properties that store, set and manage all the card object's attributes
    related to a suit. All suit-related variables are stored in variables.py script in game module,
    except for unicode versions that are indexed in class object's attributes (not instance) under 
    in tuple containers and dictionaries, e.g.: Card.CARD_SUIT_UNICODE_INDEX for unicode mapping or
    Card.CARD_SUIT_LIST for a default accepted list of suits.

    There are four suits in total: Hearts, Diamonds, Clubs, and Spades; and two colors: Red for 
    Hearts and Diamonds, and black for Clubs and Spades. 
    
    Suits are used to compare cards between themselves when determining which card has a greater 
    value (but only if they have the same suit, or one suit is a trump suit), or a lesser value 
    (again, same suit only). Other core controllers, such as PlayerController uses suit value to 
    determine if the first dealt hand needs to be dealt again should there be five or more cards of
    the same suit. Suit is a part of overwritten __gt__ and __lt__ magic method comparissons.
    
    Most if not all setter methods have assertion control that (if enabled) will attempt to assert
    that parameters meant to set a new value for an attribute is a valid type, and is a default
    value (from a list of default values in class attributes).

    """

    
    @cached_property
    def card_suit(self) -> str:
        """
        Card object's default suit value as is in variables.py script, e.g. "CARD_SUIT_HEARTS".
        
        Used to determine if a hand needs to be dealt again (five cards of the same suit on first 
        deal); to compare card type values where cards must be of the same suit; to create a repr
        (or display) version of the card's suit by removing the variable tag and formatting string, 
        e.g. "Hearts". 
        
        Cached.

        :return str: Card object's default suit value as is in variables.py script, e.g. 
            "CARD_SUIT_HEARTS"
        """

        # Returning:
        return self.__card_suit
    

    @cached_property
    def card_suit_color(self) -> str:
        """
        Card object's default suit value as is in variables.py script, e.g. "CARD_SUIT_COLOR_RED".

        (Not implemented) Used to evaluate hand's potency by color. to create a repr (or display) 
        version of the card's suit color by removing the variable tag and formatting string, e.g. 
        "Red". 
        
        Cached.

        :return str: Card object's default suit value as is in variables.py script, e.g. 
            "CARD_SUIT_COLOR_RED".
        """

        # Acquiring suit color:
        card_suit_color: str = Card.CARD_SUIT_COLOR_INDEX[self.card_suit]

        # Returning:
        return card_suit_color

    
    @cached_property
    def card_suit_repr(self) -> str:
        """
        Card object's formatted suit value, e.g. "Hearts".

        Used to display card object's suit value in-game in a readable format. Uses class's misc
        method __convert_to_repr() to remove tag from its default string value and return as a 
        formatted string, e.g. "CARD_SUIT_HEARTS" -> "Hearts"; and to create a filename for front
        texture, e.g. "{card_suit_repr}_{card_type_repr}.png" -> "hearts_six.png".

        Cached.

        :return str: Card object's formatted suit value, e.g. "Hearts".
        """

        # Formatting string:
        repr_string_formatted: str = self.__convert_to_repr(
            attribute_string = self.card_suit,
            )

        # Returning:
        return repr_string_formatted
    

    @cached_property
    def card_suit_color_repr(self) -> str:
        """
        Card object's formatted suit color value, e.g. "Red".

        Used to display card object's suit color value in-game in a readable format. Uses class's
        misc method __convert_to_repr() to remove tag from its default string value and return as 
        a formatted string, e.g. "CARD_SUIT_COLOR_RED" -> "Red".

        Cached.

        :return str: Card object's formatted suit value, e.g. "Red".
        """

        # Formatting string:
        repr_string_formatted: str = self.__convert_to_repr(
            attribute_string = self.card_suit_color,
            )

        # Returning:
        return repr_string_formatted

    
    @cached_property
    def card_suit_unicode(self) -> str:
        """
        Card object's suit unicode value, e.g. ♡ for Hearts, or ♢ for Diamonds, or ♧ for Clubs, 
        or ♤ Spades. 
        
        Used to construct a __repr__ string for Card class object; to print a card object into 
        console; or to display a hint when hovering over a suit or a card object.

        Cached.

        :return str: Card object's suit unicode value, e.g. ♡ for Hearts, etc.
        """

        # Acquiring suit unicode:
        card_suit_unicode: str = Card.CARD_SUIT_UNICODE_INDEX[self.card_suit]

        # Returning:
        return card_suit_unicode

    
    def set_card_suit(self, set_value: str) -> None:
        """
        Sets a new card suit value to a card object, if current suit value is different. Must be 
        a default value as in variables.py script, e.g. "CARD_SUIT_HEARTS".

        Automatically clears suit property related cached attributes, and "state_ready" attribute.

        :param str set_value: Card suit string value in its default form, as in variables.py
            script, e.g. "CARD_SUIT_HEARTS".

        :raise AssertionError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected string), or parameter value not in default list (expected list
            stored in Card.CARD_SUIT_LIST).
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = str
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default:
            valid_list: tuple[str, ...] = Card.CARD_SUIT_LIST
            assert_value_is_default(
                check_value = set_value,
                valid_list  = valid_list,
                raise_error = True
                )

        # Updating attribute:
        if self.card_suit != set_value:
            self.__card_suit: str = set_value

            # Clearing cache (suit):
            self.__clear_cached_property_list(
                target_list = self.__cached_suit_property_list
                )
                
            # Clearing cache (state ready):
            self.__clear_cached_property(
                target_attribute = "state_ready"
                )
                

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    TYPE METHODS AND PROPERTIES BLOCK
    
    Type-related methods and properties that store, set and manage all the card object's attributes
    related to a type. All type-related variables are stored in variables.py script in game module,
    except for unicode versions that are being generated based on type (named types produce the 
    first letter, numeric types produce their type number), e.g.: Card.CARD_TYPE_LIST for a default 
    accepted list of types.

    There are a total of 9 different types of card types: Six (6), Seven (7), Eight (8), Nine (9),
    Ten (10), Jack (J), Queen (Q), King (K), and Ace (A), with Six being the weakest card type (the
    lowest value) and Ace being the strongest card type (the highest value).
    
    Types are used to calculate type value with the lowest 6 (Six) and highest 14 (Ace). Trump suit
    value modifier adds 100 on top, thus making the lowest trump card value 106 (Six, trump) and 
    114 (Ace, trump). Types and type value are mapped within Card.CARD_TYPE_VALUE_INDEX dictionary
    in class attribute and acquired via cached property methods.
    
    These values are used to compare cards when determining which card has a greater value (but only 
    if they have the same suit, or one suit is a trump suit), or a lesser value (again, same suit 
    only). Other core controllers, such as PlayerController uses suit value to determine if the first
    dealt hand needs to be dealt again should there be five or more cards of the same suit. These 
    comparissons can be done by directly comparing type's value or by using overwritten __gt__ and 
    __lt__ magic methods.
    
    Most if not all setter methods have assertion control that (if enabled) will attempt to assert
    that parameters meant to set a new value for an attribute is a valid type, and is a default
    value (from a list of default values in class attributes).

    """


    @cached_property
    def card_type(self) -> str:
        """
        Card object's default type value as is in variables.py script, e.g. "CARD_TYPE_JACK".
        
        Used to compare cards on table and in hand when determining which cards need to be set 
        state as playable, e.g. a card of type "CARD_TYPE_JACK" can only be played when there are
        no cards on table, or only when there is at least one card of the same type already played;
        and to create a repr (or display) version of the card's type by removing the variable tag 
        and formatting string, e.g. "Jack". 
        
        Cached.

        :return str: Card object's default type value as is in variables.py script, e.g. 
            "CARD_TYPE_JACK"
        """

        # Returning:
        return self.__card_type
    

    @cached_property
    def card_type_repr(self) -> str:
        """
        Card object's formatted type value, e.g. "Jack".

        Used to display card object's type value in-game in a readable format. Uses class's misc
        method __convert_to_repr() to remove tag from its default string value and return as a 
        formatted string, e.g. "CARD_TYPE_JACK" -> "Jack"; and to create a filename for front
        texture, e.g. "{card_suit_repr}_{card_type_repr}." -> "hearts_six.png".

        Cached.

        :return str: Card object's formatted type value, e.g. "Jack".
        """

        # Formatting string:
        repr_string_formatted: str = self.__convert_to_repr(
            attribute_string = self.card_type,
            )

        # Returning:
        return repr_string_formatted

    
    @cached_property
    def card_type_value(self) -> int:
        """
        Card object's integer type value, e.g. 6 for a card of type "CARD_TYPE_SIX", or (if trump)
        107 for a card of type "CARD_TYPE_SEVEN" which state_trump is True (trump modifier applied).

        Used to compare card objects and determine which card's value is greater if both of cards 
        have the same suit value, as well as determine which card is playable (or needs to be set
        as such) when defending; to calculate hand's total value to determine which player is in a
        better (or even winning) position.

        Cached.

        :return int: Card object's integer type value, e.g. 6 for a card of type "CARD_TYPE_SIX".
        """

        # Acquiring card type value:
        card_type_value: int = Card.CARD_TYPE_VALUE_INDEX[self.card_type]
        if self.state_trump:
            card_type_value: int = card_type_value + Card.CARD_TRUMP_VALUE_BONUS

        # Returning:
        return card_type_value

    
    @cached_property
    def card_type_unicode(self) -> str:
        """
        Card object's type unicode value, e.g. "6" for Six or "J" for Jack - the first letter of
        a named card type, or full numerical value (not calculated type value) for numerical card
        type.
        
        Used to construct a __repr__ string for Card class object; to print a card object into 
        console; or to display a hint when hovering over a card object.

        Cached.

        :return str: Card object's type unicode value, e.g. J for Jack, etc.
        """

        # Generating a named type list:
        card_type_named_list: tuple[str, ...] = (
            VAR_CARD_TYPE_JACK,
            VAR_CARD_TYPE_QUEEN,
            VAR_CARD_TYPE_KING,
            VAR_CARD_TYPE_ACE
            )
        
        # If card type is Jack, or Queen, or King, or Ace, - take letter:
        if self.card_type in card_type_named_list:
            card_type_repr_char: str = self.card_type_repr[0]
            card_type_unicode: str = card_type_repr_char.upper()
        
        # If card is 6, or 7, or 8, or 9, or 10, - take value:
        else:
            card_type_value_char: str = str(self.card_type_value)
            card_type_unicode: str = card_type_value_char.upper()

        # Returning:
        return card_type_unicode


    def set_card_type(self, set_value: str) -> None:
        """
        Sets a new card type value to a card object, if current type value is different. Must be 
        a default value as in variables.py script, e.g. "CARD_TYPE_LIST".

        Automatically clears type property related cached attributes, and "state_ready" attribute.

        :param str set_value: Card type string value in its default form, as in variables.py
            script, e.g. "CARD_TYPE_LIST".

        :raise AssertionError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected string), or parameter value not in default list (expected list
            stored in Card.CARD_TYPE_LIST).
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = str
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default:
            valid_list: tuple[str, ...] = Card.CARD_TYPE_LIST
            assert_value_is_default(
                check_value = set_value,
                valid_list  = valid_list,
                raise_error = True
                )

        # Updating attribute:
        if self.card_type != set_value:
            self.__card_type: str = set_value

            # Clearing cache (type):
            self.__clear_cached_property_list(
                target_list = self.__cached_type_property_list,
                )
            
            # Clearing cache (state ready):
            self.__clear_cached_property(
                target_attribute = "state_ready"
                ) 
            

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    POSITION METHODS AND PROPERTIES BLOCK
    
    Positions methods and properties set, store and manage card object's position index and its 
    location in game, help sort cards in hand by assigning new position values, or restore their 
    positions as cards were initially added to the hand (PlayerController's container).

    Each position's default value is None, and these default values are restored once one of the 
    positions is set to an integer value, thus removing related but unaffected properties. Example
    usage would be to set a position on table to 0 (left-move spot) and stack position to 0 (bottom
    spot in stack) and update related via setter parameter, bringing all other position values to 
    None. All these called methods will also clear position related cache for all positions and 
    location property.

    These positions are used to determine card's location via (cached) property location and its
    formatted version location_repr by checking all positions if they are equal to None, or to an
    integer type value.

    Position indexes are also used to set correct coordinates x and y when moving cards in game
    and rendering them, e.g. all cards in hand (player) are bound to a pre-specified coordinate y
    in settings.py CARD_COORDINATE_Y_HAND_PLAYER, but their coordinate x will differ based on their
    position. Cached coordinates properties will also auto-adjust based on the card object's state
    "hovered" and slide when called to a coordinate based on their location and current position,
    e.g. cards will slide up and down in hands, and right and left when on top stack position on
    the table when hovered or let alone.

    """


    @cached_property
    def position_added(self) -> int | None:
        """
        Card object's added to the hand index, e.g. 5, if there were 5 more cards already in hand 
        (PlayerController's container) and they occupied position index in range 0 to 4. If card
        is not in hand, this property will always return None.

        This property's attribute can be automatically updated to be None if one of other related
        setter methods are called, but position is different, e.g. if set_position_deck is called,
        other attributes are set to None to signify the change of location. Cached properties such
        as location and location_repr rely on this and other methods to accurately show the 
        location of the card at any given time in game.

        Used to sort cards by their added position (added time), from first added to last, thus
        keeping older cards to the left-most position, and adding newer cards to the right.

        Cached.

        :return int: Card object's added to the hand index in range 0 to 35, e.g. 5.
        :return None: None, if card object is NOT in hand (PlayerController's container).
        """

        # Returning:
        return self.__position_added
    

    @cached_property
    def position_hand(self) -> int | None:
        """
        Card object's position in hand index, e.g. 2, if this card object is the third from the 
        left-most position. If card is not in hand, this property will always return None.

        This property's attribute can be automatically updated to be None if one of other related
        setter methods are called, but position is different, e.g. if set_position_deck is called,
        other attributes are set to None to signify the change of location. Cached properties such
        as location and location_repr rely on this and other methods to accurately show the 
        location of the card at any given time in game.

        Used when sorting cards by any method but by added time, e.g. if sorted by suit cards will
        be assigned position in hand depending on their suit first, and then their value within the
        suit. Thus, the card with position 0 will be at the left-most position in hand, and the 
        largest position index will be at the right-most spot.

        Cached.

        :return int: Card object's position in hand index in range 0 to 35, e.g. 5.
        :return None: None, if card object is NOT in hand (PlayerController's container).
        """

        # Returning:
        return self.__position_hand
    

    @cached_property
    def position_table(self) -> int | None:
        """
        Card object's position on the table, e.g. 0, if this card object is the first card played
        this turn and occupies the left-most spot on the table. If card is not on the table, this 
        property will always return None.

        Table position is one of two index values that are used to determine cards' coordinates on
        the table, where the other one is stack position. 

        This property's attribute can be automatically updated to be None if one of other related
        setter methods are called, but position is different, e.g. if set_position_deck is called,
        other attributes are set to None to signify the change of location. Cached properties such
        as location and location_repr rely on this and other methods to accurately show the 
        location of the card at any given time in game.

        Used to calculate and set correct coordinates to the card during the game when the card is
        played.

        Cached.

        :return int: Card object's position on table index in range 0 to 5, e.g. 0.
        :return None: None, if card object is NOT on table (TableController's container).
        """

        # Returning:
        return self.__position_table
    

    @cached_property
    def position_stack(self) -> int | None:
        """
        Card object's position in stack, e.g. 0 if card is on the bottom of the stack, or 1 if card
        is on the top of the stack. If card is not on the table, this property will always return 
        None.

        Stack position is one of two index values that are used to determine cards' coordinates on
        the table, where the other one is table position. 

        This property's attribute can be automatically updated to be None if one of other related
        setter methods are called, but position is different, e.g. if set_position_deck is called,
        other attributes are set to None to signify the change of location. Cached properties such
        as location and location_repr rely on this and other methods to accurately show the 
        location of the card at any given time in game.

        Used to calculate and set correct coordinates to the card during the game when the card is
        played.

        Cached.

        :return int: Card object's position in stack index in range 0 to 1, e.g. 0.
        :return None: None, if card object is NOT on table (TableController's container).
        """

        # Returning:
        return self.__position_stack
    

    @cached_property
    def position_deck(self) -> int | None:
        """
        Card object's position in deck, e.g. 0 if card is on the bottom of the deck (last), or 35 
        if card is on the top of the deck (next to draw). If card is not in the deck, this property 
        will always return None.

        This property's attribute can be automatically updated to be None if one of other related
        setter methods are called, but position is different, e.g. if set_position_hand is called,
        other attributes are set to None to signify the change of location. Cached properties such
        as location and location_repr rely on this and other methods to accurately show the 
        location of the card at any given time in game.

        (Not implemented) Used to track card position in deck and swap trump card as a bonus 
        setting per game session.

        Cached.

        :return int: Card object's position in deck index in range 0 to 35, e.g. 0.
        :return None: None, if card object is NOT in deck (DeckController's container).
        """

        # Returning:
        return self.__position_deck
    

    @cached_property
    def position_discard(self) -> int | None:
        """
        Card object's position in discard pile, e.g. 0 if card is on the bottom of the discard pile 
        (was first added), or 35 if card is on the top of the discard pile (was last added). If 
        card is not in the discard, this property will always return None.

        This property's attribute can be automatically updated to be None if one of other related
        setter methods are called, but position is different, e.g. if set_position_hand is called,
        other attributes are set to None to signify the change of location. Cached properties such
        as location and location_repr rely on this and other methods to accurately show the 
        location of the card at any given time in game.

        Used to track the order of cards discarded.
        
        Cached.

        :return int: Card object's position in discard index in range 0 to 35, e.g. 0.
        :return None: None, if card object is NOT in discard (DiscardController's container).
        """

        # Returning:
        return self.__position_discard
    

    def set_position_added(self, position_index: int, update_related: bool = True) -> None:
        """
        Sets a new position added to the card object. This method may reset other position-related 
        attributes to None, if this stter changes the location of the card in game, e.g. setting a
        new position added will set position in deck to None, as it is no longer (or can no longer)
        be in deck container.

        Automatically clears location and position property related cached attributes if parameter 
        update_related is True, otherwise clears only "position_added" attribute.

        :param int position_index: Integer value of a new position added. Must be in range 0-35.
        :param bool update_related: Flag to update related position attributes, setting them to
            None, if this setter changes the location of the card in game.

        :raise AssertionError: (If enabled) Raises AssertionError if parameters value type are 
            invalid, or position index is out of range.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = position_index,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = update_related,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default:
            valid_range: range = range(0, 36)       # <- 36 cards, assuming all 36 cards in one hand.
            assert_value_in_valid_range(
                check_value = position_index,
                valid_range = valid_range,
                raise_error = True
                )

        # Updating attribute:
        if self.position_added != position_index:
            self.__position_added: int = position_index

            # Cache list:
            cached_position_property_list: tuple[str, ...] = tuple(
                "position_added"
                )

            # Updating related positions:
            if update_related:
                self.__position_table:   int | None = None
                self.__position_stack:   int | None = None
                self.__position_deck:    int | None = None
                self.__position_discard: int | None = None

                # Updating cached property list:
                cached_position_property_list: tuple[str, ...] = self.__cached_position_property_list
            
            # Clearing cache (position):
            self.__clear_cached_property_list(
                target_list = cached_position_property_list
                )
                
            # Clearing cache (location):
            self.__clear_cached_property_list(
                target_list = self.__cached_location_property_list
                )
    

    def set_position_hand(self, position_index: int, update_related: bool = True) -> None:
        """
        Sets a new position in hand to the card object. This method may reset other position-related
        attributes to None, if this stter changes the location of the card in game, e.g. setting a
        new position in hand will set position in deck to None, as it is no longer (or can no longer)
        be in deck container.

        Automatically clears location and position property related cached attributes if parameter 
        update_related is True, otherwise clears only "position_hand" attribute.

        :param int position_index: Integer value of a new position in hand. Must be in range 0-35.
        :param bool update_related: Flag to update related position attributes, setting them to
            None, if this setter changes the location of the card in game.

        :raise AssertionError: (If enabled) Raises AssertionError if parameters value type are 
            invalid, or position index is out of range.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = position_index,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = update_related,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default:
            valid_range: range = range(0, 36)       # <- 36 cards, assuming all 36 cards in one hand.
            assert_value_in_valid_range(
                check_value = position_index,
                valid_range = valid_range,
                raise_error = True
                )

        # Updating attribute:
        if self.position_hand != position_index:
            self.__position_hand: int = position_index

            # Cache list:
            cached_position_property_list: tuple[str, ...] = tuple(
                "position_hand"
                )

            # Updating related positions:
            if update_related:
                self.__position_table:   int | None = None
                self.__position_stack:   int | None = None
                self.__position_deck:    int | None = None
                self.__position_discard: int | None = None

                # Updating cached property list:
                cached_position_property_list: tuple[str, ...] = self.__cached_position_propaerty_list
            
            # Clearing cache (position):
            self.__clear_cached_property_list(
                target_list = cached_position_property_list
                )
                
            # Clearing cache (location):
            self.__clear_cached_property_list(
                target_list = self.__cached_location_property_list
                )
    

    def set_position_table(self, position_index: int, stack_index: int, update_related: bool = True) -> None:
        """
        Sets a new position on table to the card object. The method may reset other position-related
        attributes to None, if this stter changes the location of the card in game, e.g. setting a
        new position in hand will set position in deck to None, as it is no longer (or can no longer)
        be in deck container.

        Automatically clears location and position property related cached attributes if parameter 
        update_related is True, otherwise clears only "position_table" and "position_stack" attributes.

        :param int position_index: Integer value of a new position on table. Must be in range 0-5.
        :param int stack_index: Integer value of a new position in stack. Must be in range 0-1.
        :param bool update_related: Flag to update related position attributes, setting them to
            None, if this setter changes the location of the card in game.

        :raise AssertionError: (If enabled) Raises AssertionError if parameters value type are 
            invalid, or position index is out of range.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            for value_index in (position_index, stack_index):
                valid_type: type = int
                assert_value_is_valid_type(
                    check_value = value_index,
                    valid_type  = valid_type,
                    raise_error = True,
                    )
            
            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = update_related,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default:
            valid_range: range = range(TABLE_POSITION_COUNT_MAX)    # 0 to 5 position index
            assert_value_in_valid_range(
                check_value = position_index,
                valid_range = valid_range,
                raise_error = True
                )
            
            # Asserting value is default:
            valid_range: range = range(TABLE_STACK_TOP_INDEX + 1)   # 0 to 1 stack index
            assert_value_in_valid_range(
                check_value = stack_index,
                valid_range = valid_range,
                raise_error = True
                )

        # Updating attributes:
        self.__position_table: int = position_index
        self.__position_stack: int = stack_index

        # Cache list:
        cached_position_property_list: tuple[str, ...] = (
            "position_table",
            "position_stack",
            )

        # Updating related positions:
        if update_related:
            self.__position_hand:    int | None = None
            self.__position_added:   int | None = None
            self.__position_deck:    int | None = None
            self.__position_discard: int | None = None

            # Updating cached property list:
            cached_position_property_list: tuple[str, ...] = self.__cached_position_property_list

        # Clearing cache (position):
        self.__clear_cached_property_list(
            target_list = cached_position_property_list
            )
            
        # Clearing cache (location):
        self.__clear_cached_property_list(
            target_list = self.__cached_location_property_list
            )
            
    
    def set_position_deck(self, position_index: int, update_related: bool = True) -> None:
        """
        Sets a new position in deck to the card object. The method may reset other position-related
        attributes to None, if this stter changes the location of the card in game, e.g. setting a
        new position in hand will set position in deck to None, as it is no longer (or can no longer)
        be in deck container.

        Automatically clears location and position property related cached attributes if parameter 
        update_related is True, otherwise clears only "position_deck" attribute.

        :param int position_index: Integer value of a new position in deck. Must be in range 0-35.
        :param bool update_related: Flag to update related position attributes, setting them to
            None, if this setter changes the location of the card in game.

        :raise AssertionError: (If enabled) Raises AssertionError if parameters value type are 
            invalid, or position index is out of range.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = position_index,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = update_related,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default:
            valid_range: range = range(0, 36)       # <- 36 cards, assuming all 36 cards are in deck
            assert_value_in_valid_range(
                check_value = position_index,
                valid_range = valid_range,
                raise_error = True
                )

        # Updating attributes:
        self.__position_deck: int = position_index

        # Cache list:
        cached_position_property_list: tuple[str, ...] = (
            "position_deck",
            )

        # Updating related positions:
        if update_related:
            self.__position_hand:    int | None = None
            self.__position_added:   int | None = None
            self.__position_table:   int | None = None
            self.__position_stack:   int | None = None
            self.__position_discard: int | None = None

            # Updating cached property list:
            cached_position_property_list: tuple[str, ...] = self.__cached_position_property_list

        # Clearing cache (position):
        self.__clear_cached_property_list(
            target_list = cached_position_property_list
            )
            
        # Clearing cache (location):
        self.__clear_cached_property_list(
            target_list = self.__cached_location_property_list
            )
            
    
    def set_position_discard(self, position_index: int, update_related: bool = True) -> None:
        """
        Sets a new position in discard pile to the card object. The method may reset other position
        -related attributes to None, if this stter changes the location of the card in game, e.g. 
        setting a new position in hand will set position in deck to None, as it is no longer (or 
        can no longer) be in deck container.

        Automatically clears location and position property related cached attributes if parameter 
        update_related is True, otherwise clears only "position_discard" attribute.

        :param int position_index: Integer value of a new position in discard pile. Must be in range 
            0-35, assuming all cards are in discard pile.
        :param bool update_related: Flag to update related position attributes, setting them to
            None, if this setter changes the location of the card in game.

        :raise AssertionError: (If enabled) Raises AssertionError if parameters value type are 
            invalid, or position index is out of range.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = position_index,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = update_related,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default:
            valid_range: range = range(0, 36)       # <- 36 cards, assuming all 36 cards are in discard
            assert_value_in_valid_range(
                check_value = position_index,
                valid_range = valid_range,
                raise_error = True
                )

        # Updating attributes:
        self.__position_discard: int = position_index

        # Cache list:
        cached_position_property_list: tuple[str, ...] = (
            "position_deck",
            )

        # Updating related positions:
        if update_related:
            self.__position_hand:    int | None = None
            self.__position_added:   int | None = None
            self.__position_table:   int | None = None
            self.__position_stack:   int | None = None
            self.__position_deck:    int | None = None

            # Updating cached property list:
            cached_position_property_list: tuple[str, ...] = self.__cached_position_property_list

        # Clearing cache (position):
        self.__clear_cached_property_list(
            target_list = cached_position_property_list
            )
            
        # Clearing cache (location):
        self.__clear_cached_property_list(
            target_list = self.__cached_location_property_list
            )
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    LOCATION PROPERTIES BLOCK
    
    Location properties analyzed card object's position attributes and determines location based on
    their assigned values: integer or None-type. 
    
    If a position is assigned an integer value, then card object's location will return a string 
    value, e.g. "CARD_LOCATION_HAND" if position in  hand in not None, or "CARD_LOCATION_DISCARD" 
    if position in discard is not None etc. Repr method would return a formatted string by removing
    default location variable tag, e.g. "CARD_LOCATION_HAND" -> "Hand".

    Used to determine render properties, such as rotation angle and scale, as well allowing other
    controllers to manipulate cards by calling slide methods; and to adjust coordinates based on
    its location. 
    
    It is also used to simplify assertions and check statements and to have readable variables 
    instead of implicitly used and stored position index values. Example used in one of the slide
    methods: if self.location == VAR_CARD_LOCATION_HAND -> gives better readability, then checking
    position index and checking if it is an instance of an integer or None-type.

    """


    @cached_property
    def location(self) -> str:
        """
        Location value in its default format as in variables.py script, e.g. "CARD_LOCATION_HAND",
        or "CARD_LOCATION_TABLE" strings. 
        
        This property checks all position index attributes and returns a location string that is
        corresponding to the position, e.g. if position in hand index is equal to 1 (and not None)
        this property will return "CARD_LOCATION_HAND".

        Used to determine render properties, such as rotation angle and scale, as well allowing other
        controllers to manipulate cards by calling slide methods; and to adjust coordinates based on
        its location. 

        Cached.

        :return str: Location value in its default format as in variables.py script, e.g. 
            "CARD_LOCATION_HAND" string. 
        """

        # Matching location variables and position attributes:
        location_string: str = VAR_CARD_LOCATION_NOT_SET
        location_index: dict[str, int | None] = {
            VAR_CARD_LOCATION_HAND:    self.position_hand,
            VAR_CARD_LOCATION_TABLE:   self.position_table,
            VAR_CARD_LOCATION_DECK:    self.position_deck,
            VAR_CARD_LOCATION_DISCARD: self.position_discard
            }
        
        # Selecting position:
        for location, position_index in location_index.items():
            if position_index is not None:
                location_string: str = location
                break
        
        # Returning:
        return location_string
    

    @cached_property
    def location_repr(self) -> str:
        """
        Location formatted value, e.g. "Hand", or  "Discard".

        Used to display card object's location value in-game in a readable format. Uses class's 
        misc method __convert_to_repr() to remove tag from its default string value and return as 
        a  formatted string, e.g. "CARD_LOCATION_DISCARD" -> "Discard".

        Cached.

        :return str: Location formatted value, e.g. "Hand", or  "Discard".
        """

        # Formatting string:
        repr_string_formatted: str = self.__convert_to_repr(
            attribute_string = self.location,
            )

        # Returning:
        return repr_string_formatted

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    STATE METHODS AND PROPERTIES BLOCK
    
    State methods and properties reflects the change of the card object's based on the events in 
    game. While only one state is used internally (state_ready), the other states are changed based
    on the events.

    Hovered and selected states are based on player's input. If a card is clicked (or other) - it 
    is selected, deselecting other (if any) cards; if it is played, it is deselected etc. Hovered 
    state reacts to player's cursor (or other). Hover state is set when player's cursor is hovered
    over a card (that can be hovered over, e.g. - playable and owner's card, or opponent's card), 
    and is set to default state if cursor leaves the card boundaries.

    Trump state shows that card object's suit is a trump suit (decided by DeckController upon deck
    creation, or changed with GameController on suit swap), and this tate allows the type value 
    calculation to add bonus value modifier.

    Plyable state is set and changed based on the player's active and focus states after the game
    controller checks whether or not a card can be played based on the cards on the table and their
    value compared to its own. 

    """


    @cached_property
    def state_ready(self) -> bool:
        """
        Boolean value that represents card object's complete (or incomplete) initialization as a 
        Card class object. It checks if card object's suit and type attributes were set to any 
        but default values and returns a check result.

        Used for checks in __repr__ magic method and other methods that require card object's 
        complete setup.

        Cached.

        :return bool: Boolean value representation of card object's complete initialization. True,
            if its suit and type attributes are set to values different from their defaults, e.g.
            suit not set to "CARD_SUIT_NOT_SET" and type not set to "CARD_TYPE_NOT_SET. False, if
            otherwise.
        """

        # Checking:
        state_ready: bool = bool(
            self.card_suit != VAR_CARD_SUIT_NOT_SET and
            self.card_type != VAR_CARD_TYPE_NOT_SET
            )
        
        # Returning:
        return state_ready


    @cached_property
    def state_trump(self) -> bool:
        """
        Boolean value that represents card object's suit being a trump suit.

        Used for card type value comparisons between card objects, as it state determines whether
        or not to add Card.CARD_TRUMP_VALUE_BONUS bonus value stored in class attributes to the 
        default type value.

        Cached.

        :return bool: Boolean value that represents card object's suit being a trump suit. True,
            if card object's suit is a trump suit. False, otherwise.
        """

        # Returning:
        return self.__state_trump
    

    @cached_property
    def state_playable(self) -> bool:
        """
        Boolean value that represents card object's playable state, in other words if a Player that
        controls the card can play it during its current turn. 
         
        Used for the defending player to have their hand (PlayerController's container) checked if 
        there are any cards which have a greater type value (and same stui, if not trump) compared 
        to the card objects on table; or the attacking player to determine whether they have any 
        cards of the same base type value as any of the cards on the table.

        This boolean flag may caused cards to slide to their "unplayable" position, if enabled in
        session.py script.

        Example: Attacking player has ♡K, ♤8 and ♧Q in hand, and there are currently ♡8 and ♡A on
        table, making ♤8 a playable card during his turn. They play the card, and now the defending
        player must have his hand update to see if there is any card object that has a greater 
        value that ♤8 (8), for example ♤9 (9) or ♡10 (110, trump bonus). Thus, these cards are set
        as plyable.

        Cached.

        :return bool: Boolean value that represents card object's playable state. True, if the card
            object can be played during current turn and within this focus state. False, otherwise.
        """

        # Returning:
        return self.__state_playable
    

    @cached_property
    def state_selected(self) -> bool:
        """
        Boolean value that represents card object's selected state. True, if card object is being
        selected at the moment, and False otherwise.

        Used to show if player selects (click on) a card object during the game. 
        
        This state alters several render-related properties, such as: render_scale (returns a 
        greater float value), render_angle (returns a non-default value by generating a new angle
        to render card texture with).

        Cached.

        :return bool: Boolean value that represents card object's selected state. True, if card 
            object is being selected at the moment. Otherwise, False.
        """

        # Returning:
        return self.__state_selected
    

    @cached_property
    def state_hovered(self) -> bool:
        """
        Boolean value that represents card object's hover state. True, if card object is being
        hovered over at the moment, and False otherwise.

        Used to show if player hovers over a card object during the game (if able).

        This state allows slide methods() to adjust coordinates based on state and coordinates
        difference at any give moment: if card is hovered, but coordinates are not at the hover
        state position, slide methods() will adjust the position, etc.

        Cached.

        :return bool: Boolean value that represents card object's hovered state. True, if card
            object is being hovered over at the moment. Otherwise, False.
        """

        # Returning:
        return self.__state_hovered
    

    @cached_property
    def state_revealed(self) -> bool:
        """
        Boolean value that shows if this card object was revealed to the player by being put either
        on the table or in hand. Opponent's hand (PlayerController's container) is not revealed by
        default, as well as deck discard containers.

        Used by render properties to determine which loaded texture object to use (front or cover) 
        to render card object on screen.

        Cached.

        :return bool: Boolean value that shows if this card object was revealed to the player. True,
            if revealed. Otherwise, False.
        """

        # Returning:
        return self.__state_revealed
    

    def set_state_trump(self, set_value: bool) -> None:
        """
        Sets a new trump state for card object.

        Called by DeckController upon new deck instance creation: deck creates 36 instances of Card 
        class object, randomly selects a trump suit value and then updates the cards of that one 
        selected stui with this method.

        Automatically clears related cached property cache.

        :param bool set_value: New trump state for card object. True, if card suit is considered to
            be trump suit. False otherwise.

        :raise AssertionError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected boolean).
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )

        # Updating attribute
        if self.state_trump != set_value:
            self.__state_trump: bool = set_value

            # Clearing cache:
            cached_property_list: tuple[str, ...] = (
                "state_trump",
                "card_type_value"       # <- Trump state affects card's value.
                )
            self.__clear_cached_property_list(
                target_list = cached_property_list
                )
    

    def set_state_playable(self, set_value: bool) -> None:
        """
        Sets a new playable state for card object.

        Used when Gameshell or other GameController checks card available to players and analyzes 
        the current state and cards on the table. If card can be played (its value is greater than
        that of a card or cards on the table and it has the same suit), then this method is called
        and its state is changed. Same if otherwise.

        Automatically clears related cached property cache.

        :param bool set_value: New playabe state for card object. True, if card suit is considered 
            to be playable. False otherwise.

        :raise AssertionError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected boolean).
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )

        # Updating attribute:
        if self.state_playable != set_value:
            self.__state_playable: bool = set_value

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "state_playable"
                )
    

    def set_state_revealed(self, set_value: bool) -> None:
        """
        Sets a new revealed state for card object.

        Used when a card is revealed to the player during an in-game event, e.g. card played on 
        table, dealt to hand, revealed from deck. If enabled in session, opponent's hand as well as
        discard piles can be revealed too. Thus, True if revealed, False otherwise.

        Automatically clears related cached property cache.

        :param bool set_value: New revealed state for card object. True, if card suit is considered 
            to be revealed to player. False otherwise.

        :raise AssertionError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected boolean).
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )

        # Updating attribute:
        if self.state_revealed != set_value:
            self.__state_revealed: bool = set_value

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "state_revealed"
                )

            # Clearing cache (render):
            self.__clear_cached_property_list(
                target_list = self.__cached_render_property_list,
                )
    

    def set_state_selected(self, set_value: bool) -> None:
        """
        Sets a new selected state for card object.

        Called by Gameshell's click card event, when player clicks or selects a card object in any
        other way. Selection sets the state to True, deselection sets the state to False.

        Automatically clears related cached property cache.

        :param bool set_value: New selected state for card object. True, if card suit is currently 
            selected by the player. False otherwise.

        :raise AssertionError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected boolean).
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )

        # Updating attribute:
        if self.state_selected != set_value:
            self.__state_selected: bool = set_value

            # Clearing cache (state):
            self.__clear_cached_property(
                target_attribute = "state_selected",
                )

            # Clearing cache (render):
            self.__clear_cached_property_list(
                target_list = self.__cached_render_property_list
                )
    

    def set_state_hovered(self, set_value: bool) -> None:
        """
        Sets a new hovered state for card object.

        Called by Gameshell's hover card event, when player hovers over or moves cursor away from 
        a (hovered) card object. Hover event sets the state to True, moving cursour away from 
        previously hovered over card sets the state to False.

        Automatically clears related cached property cache.

        :param bool set_value: New hovered state for card object. True, if card suit is currently 
            hovered over by the player. False otherwise.

        :raise AssertionError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected boolean).
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )

        # Updating attribute:
        if self.state_hovered != set_value:
            self.__state_hovered: bool = set_value

            # Clearing cache (state):
            self.__clear_cached_property(
                target_attribute = "state_hovered",
                )

            # Clearing cache (render):
            self.__clear_cached_property_list(
                target_list = self.__cached_render_property_list
                )
                
    
    def reset_state(self) -> None:
        """
        Resets event-based states such as selected, hovered and playable, by setting them to their
        default values - False.

        Used when active state changes within PlayerController by calling this method on all cards
        in its hand container (if any) to restrict the player from playing or otherwise interacting
        with cards during opponent's turn.

        Automatically clears all related cached properties.
        """

        # Resetting all states, except for revealed and trump:
        self.__state_selected: bool = False
        self.__state_hovered:  bool = False
        self.__state_playable: bool = False

        # Clearing cache (state):
        self.__clear_cached_property_list(
            target_list = self.__cached_state_property_list
            )


        # Clearing cache (render):
        self.__clear_cached_property_list(
            target_list = self.__cached_render_property_list
            )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    TEXTURE METHODS AND PROPERTIES BLOCK
    
    Texture cached properties and methods set and store all things related to card object's front 
    and cover texture filenames, filepaths, as well as texture objects (arcade.Texture type).

    Front texture image filenames follow the pattern of {card_suit_repr}_{card_type_repr}.png, e.g.
    "hearts_six.png" or "clubs_king.png", while cover is always "cover.png". Different texture 
    packs provide different textures, but the default pack is stored under default folder in 
    textures/card directory and is loaded when the card is created to ensure that there is no 
    IOError when attempting to read a file or locate a file.

    Textures images are larger than displayed in game, and are scaled appropriately with scale 
    modifiers based on card object's state. Scale mods are found in settings.py script.
    
    """

    
    @cached_property
    def texture_pack(self) -> str:
        """
        Texture pack default string value as is in variables.py script (not default pack, but
        default formatting), e.g. "CARD_TEXTURE_PACK_DEFAULT".
        
        Used to create a filepath to locate and load a texture from different packs within folder
        ../textures/card/; and to create a repr (or display) version of the card's suit by 
        removing the variable tag and formatting string, e.g. "Default". 
        
        Cached.

        :return str: Texture pack default string value as is in variables.py script (not default 
            pack, but default formatting), e.g. "CARD_TEXTURE_PACK_DEFAULT".
        """

        # Returning:
        return self.__texture_pack
    

    @cached_property
    def texture_pack_repr(self) -> str:
        """
        Texture pack formatted string value, e.g. "Default".

        Used to display card object's suit pack name in-game in a readable format. Uses class's 
        misc method __convert_to_repr() to remove tag from its default string value and return as
        a formatted string, e.g. "CARD_TEXTURE_PACK_DEFAULT" -> "Default".

        Cached.

        :return str: Texture pack formatted string value, e.g. "Default".
        """

        # Formatting string:
        repr_string_formatted: str = self.__convert_to_repr(
            attribute_string = self.texture_pack,
            )
        
        # Returning:
        return repr_string_formatted


    @cached_property
    def texture_cover_filename(self) -> str:
        """
        Card object's cover texture filename, e.g. "cover.png".

        Used to quickly access filename attribute when comparing different textures to determine
        if an update is required.

        Cached.

        :return str: Cover texture filename string.
        """

        # Returning:
        return self.__texture_cover_filename
    

    @cached_property
    def texture_cover_filepath(self) -> str:
        """
        Card object's cover texture filepath, e.g. "./textures/card/default/cover.png". 

        Used to quickly access filepatch attribute when comparing different textures to determine
        if an update is required.

        Cached.

        :return str: Cover texture filepath string.
        """

        # Returning:
        return self.__texture_cover_filepath
    

    @cached_property
    def texture_cover_object(self) -> arcade.Texture:
        """
        Card object's cover texture object (arcade.Texture class type).

        Used to render card object's texture on the screen in game. Texture is applied over a Rect
        object (arcade.Rect), generated as a property in __render_rect.

        Cached.

        :return arcade.Texture: Cover texture object
        """

        # Returning:
        return self.__texture_cover_object
    

    @cached_property
    def texture_front_filename(self) -> str:
        """
        Front object's cover texture filename, e.g. "hearts_six.png".

        Used to quickly access filename attribute when comparing different textures to determine
        if an update is required.

        Cached.

        :return str: Front texture filename string.
        """

        # Returning:
        return self.__texture_front_filename
    

    @cached_property
    def texture_front_filepath(self) -> str:
        """
        Card object's front texture filepath, e.g. "./textures/card/default/hearts_six.png". 

        Used to quickly access filepatch attribute when comparing different textures to determine
        if an update is required.

        Cached.

        :return str: Front texture filepath string.
        """

        # Returning:
        return self.__texture_front_filepath
    

    @cached_property
    def texture_front_object(self) -> Texture:
        """
        Card object's front texture object (arcade.Texture class type).

        Used to render card object's texture on the screen in game. Texture is applied over a Rect
        object (arcade.Rect), generated as a property in __render_rect.

        Cached.

        :return arcade.Texture: Front texture object
        """

        # Returning:
        return self.__texture_front_object
    

    def __update_texture_front(self) -> None:
        """
        Updates front texture related attributes such as front texture filename, filepath and 
        texture object by generating filename based on card object's suit and type, and filepath
        following the directories stored in settings.py.

        Called by set_texture_pack() method.
        """
        
        # Generating filename:
        texture_filename: str = "{suit}_{type}.{extension}".format(
            suit = self.card_suit_repr.lower(),
            type = self.card_type_repr.lower(),
            extension = CARD_TEXTURE_EXTENSION
            )
        
        # Generating filepath:
        texture_pack_name: str = self.texture_pack_repr.lower()
        texture_pack_path: str = os.path.join(                      # -> ../textures/card/pack
            DIR_TEXTURES_CARD_PATH, 
            texture_pack_name
            )
        texture_filepath: str = os.path.join(                       # -> ../textures/card/pack/clubs_ten.png
            texture_pack_path, 
            texture_filename
            )
        
        # Loading texture object:
        texture_object: Texture = arcade.load_texture(
            file_path = texture_filepath,
            )
        
        # Updating attributes:
        self.__texture_front_filename: str = texture_filename
        self.__texture_front_filepath: str = texture_filepath
        self.__texture_front_object: Texture = texture_object


    def __update_texture_cover(self) -> None:
        """
        Updates front texture related attributes such as cover texture filename, filepath and 
        texture object by generating filename based on current texture pack set, and following 
        the directories stored in settings.py.

        Called by set_texture_pack() method.
        """
        
        # Generating filename:
        texture_filename: str = "cover.{extension}".format(
            extension = CARD_TEXTURE_EXTENSION
            )
        
        # Generating filepath:
        texture_pack_name: str = self.texture_pack_repr.lower()
        texture_pack_path: str = os.path.join(                      # -> ../textures/card/pack
            DIR_TEXTURES_CARD_PATH, 
            texture_pack_name
            )
        texture_filepath: str = os.path.join(                       # -> ../textures/card/pack/cover.png
            texture_pack_path, 
            texture_filename
            )
        
        # Loading texture object:
        texture_object: Texture = arcade.load_texture(
            file_path = texture_filepath,
            )
        
        # Updating attributes:
        self.__texture_cover_filename: str = texture_filename
        self.__texture_cover_filepath: str = texture_filepath
        self.__texture_cover_object: Texture = texture_object


    def set_texture_pack(self, set_value: str) -> None:
        """
        Sets a new texture pack for the card object, and updates texture related attributes, such
        as front and cover texture filenames, filepaths and texture objects by generating filename
        based on card object's suit and type, and filepath following the directories stored in 
        settings.py for each.

        :param str set_value: Texture pack string value in its default form, as in variables.py
            script, e.g. "CARD_TEXTURE_PACK_DEFAULT".

        :raise AssertingError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected string), or parameter value not in default list.
        """
        
        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = str
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default:
            valid_list: tuple[str, ...] = (
                VAR_CARD_TEXTURE_PACK_DEFAULT,      # <- Used by default on card creation
                )
            assert_value_is_default(
                check_value = set_value,
                valid_list  = valid_list,
                raise_error = True,
                )

        # Updating attributes:
        if self.texture_pack != set_value:
            self.__texture_pack = set_value

            # Clearing cache:
            self.__clear_cached_property_list(
                target_list = self.__cached_texture_property_list
                )
            
            # Updating textures:
            self.__update_texture_front()
            self.__update_texture_cover()
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    COORDINATES METHODS AND PROPERTIES BLOCK
    
    Coordinates methods and properties update, store and calculate card object's coordinates, their
    expected coordinates based on state and event, as well as boundaries in game helping to resulve
    event checks when card is being hovered over or selected by a cursor click.

    Coordinates x and y setters are primarily used by other controllers update methods (when 
    changing card's position/location) and native methods like slide when card's coordinates are to
    be adjusted per update by CARD_SLIDE_SPEED variables in settings.py script.

    All coordinates properties are chached and cleared once new values are introduced. To ensure 
    the validity of new coordinate values, setters are equiped (and encouraged) to assert param
    type validity and (not implemented yet) coordinate values ranges.

    """


    @cached_property
    def coordinate_x(self) -> int:
        """
        Card object's coordinate x integer value.

        Used to render card object's texture at a certain position on screen; to calculate texture
        boundaries on screen; and to move the texture object on screen with one of dedicated slide
        methods by adjusting coordinate value.

        Cached.

        :return int: Card object's coordinate x integer value.
        """

        # Returning:
        return self.__coordinate_x
    

    @cached_property
    def coordinate_y(self) -> int:
        """
        Card object's coordinate y integer value.

        Used to render card object's texture at a certain position on screen; to calculate texture
        boundaries on screen; and to move the texture object on screen with one of dedicated slide
        methods by adjusting coordinate value.

        Cached.

        :return int: Card object's coordinate y integer value.
        """

        # Returning:
        return self.__coordinate_y
    

    @cached_property
    def coordinate_y_hand(self) -> int:
        """
        Card object's default coordinate y integer value when card is in hand (PlayerController's
        container). Returns one of two values based on card object's coordinate y value, e.g.
        CARD_COORDINATE_Y_HAND_PLAYER or CARD_COORDINATE_Y_HAND_OPPONENT as stored in settings.py
        script.

        Used to render card object's texture at a certain position on screen; and to move the 
        texture object on screen with slide_hand() method by adjusting coordinate value.

        Cached.

        :return int: Card object's expected coordinate y integer value when card is in hand and is 
            not hovered over. 
        """

        # Checking if card is below or above the middle of the table:
        coordinate_y: int = CARD_COORDINATE_Y_HAND_PLAYER
        if self.coordinate_y > CARD_COORDINATE_Y_TABLE:
            coordinate_y: int = CARD_COORDINATE_Y_HAND_OPPONENT

        # Returning:
        return coordinate_y
    

    @cached_property
    def coordinate_y_hand_hover(self) -> int:
        """
        Card object's default coordinate y integer value when card is in hand (PlayerController's
        container) and is hovered. Calculates and returns one of two values based on card object's 
        coordinate y value, e.g. CARD_COORDINATE_Y_HAND_PLAYER or CARD_COORDINATE_Y_HAND_OPPONENT 
        as stored in settings.py script with added CARD_SLIDE_DISTANCE_HOVER_HAND value.

        Used to render card object's texture at a certain position on screen; and to move the 
        texture object on screen with slide_hand() method by adjusting coordinate value.

        Cached.

        :return int: Card object's expected coordinate y (to be) integer value when card is in hand
            and is hovered.
        """

        # Checking if card is below or above the middle of the table:
        coordinate_y: int = self.coordinate_y_hand + CARD_SLIDE_DISTANCE_HOVER_HAND
        if self.coordinate_y > CARD_COORDINATE_Y_TABLE:
            coordinate_y: int = int(self.coordinate_y_hand - CARD_SLIDE_DISTANCE_HOVER_HAND / 2)

        # Returning:
        return coordinate_y


    @cached_property
    def coordinates(self) -> int:
        """
        Tuple container with card object's coordinates x and y integer values.

        Used for script conversions, and displaying in game in debug mode. 

        Cached.

        :return tuple[int, int]: Tuple container with card object's coordinates x and y integer values.
        """

        # Packing:
        coordinates_container: tuple[int, int] = (
            self.coordinate_x,
            self.coordinate_y
            )

        # Returning:
        return coordinates_container
    

    def set_coordinate_x(self, 
                         set_value: int, 
                         ignore_assertion: bool = False, 
                         clear_cache: bool = True
                         ) -> None:
        """
        Sets a new coordinate x value for card object.

        Used by Gameshell (arcade.Window) controller on card dragging event, during card position
        update (both as attribute and on screen), and during slide() methods call.

        Automatically updates coordinates- and boundary-related cached properties. 
        
        :param int set_value: A new coordinate x integer value.
        :param bool ignore_assertion: Flag to ignore assertion control.
        :param bool clear_cache: Flag to force clear related cache. 

        :raise AssertionError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected integer).
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )

        # Updating attribute:
        if self.coordinate_x != set_value:
            self.__coordinate_x: int = set_value

            # Clearing cache:
            if clear_cache:

                # Clearing cache (coordinates):
                self.__clear_cached_property(
                    target_attribute = "coordinate_x"
                    )
                
                # Clearing cache (boundary):
                self.__clear_cached_property_list(
                    target_list = self.__cached_boundary_property_list,
                    )
                

    def set_coordinate_y(self, 
                         set_value: int, 
                         ignore_assertion: bool = False, 
                         clear_cache: bool = True
                         ) -> None:
        """
        Sets a new coordinate y value for card object.

        Used by Gameshell (arcade.Window) controller on card dragging event, during card position
        update (both as attribute and on screen), and during slide() methods call.

        Automatically updates coordinates- and boundary-related cached properties. 
        
        :param int set_value: A new coordinate y integer value.
        :param bool ignore_assertion: Flag to ignore assertion control.
        :param bool clear_cache: Flag to force clear related cache. 

        :raise AssertionError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected integer).
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )

        # Updating attribute:
        if self.coordinate_y != set_value:
            self.__coordinate_y: int = set_value

            # Clearing cache:
            if clear_cache:

                # Clearing cache (coordinates):
                self.__clear_cached_property(
                    target_attribute = "coordinate_y"
                    )
                
                # Clearing cache (boundary):
                self.__clear_cached_property_list(
                    target_list = self.__cached_boundary_property_list,
                    )
                
    
    def set_coordinates(self, set_value: tuple[int, int]) -> None:
        """
        Sets new coordinates x and y for card object.

        Unpacks tuple container and calls methods set_coordinate_x() and set_coordinate_y() to set
        new coordinates values. 

        Automatically updates coordinates- and boundary-related cached properties.

        :param tuple[int, int] set_value: Tuple container with coordinates x and y integer values.

        :raise AssertionError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected tuple); if tuple container items value type is invalid (expected both 
            to be integers).
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = tuple
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )

            # Asserting container items are valid type:        
            for coordinate_value in set_value:
                valid_type: type = int
                assert_value_is_valid_type(
                    check_value = coordinate_value,
                    valid_type  = valid_type,
                    raise_error = True
                    )

        # Unpacking container:
        coordinate_x, coordinate_y = set_value

        # Updating:
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
        
        # Clearing cache (coordinates):
        self.__clear_cached_property_list(
            target_list = self.__cached_coordinates_property_list
            )
            
        # Clearing cache (boundary):
        self.__clear_cached_property_list(
            target_list = self.__cached_boundary_property_list
            )
            
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    BOUNDARIES PROPERTIES BLOCK
    
    Boundary properties calculate and return texture object's boundaries on both horizontal and 
    vertical axises, as well as put those values together to create ranges.

    Their coordinates are calculated by adding or subtracting texture scaled width and height from
    the center coordinates x and y respectively and rounding it down to an integer.

    These boundary ranges are used in events of cursor hovering a card object in game, or clicking
    it by checking whether or not cursor's coordinates x and y at the time are within the boundary
    ranges.

    Out of all the boundary properties, boundary_left cached property is used to calculate the 
    proximity of cursor and itself against other card objects to determine the priority object to
    set state hovered (e.g. when cards overlap it is possible to be triggering hover even over
    more than one card, but with the proximity check only one card will be set to hover).

    """


    @cached_property
    def boundary_left(self) -> int:
        """
        Texture object's left-most coordinate x (boundary) integer value.

        Calculates and returns left-most coordinate x by subtracting half of texture width scaled
        value (CARD_TEXTURE_WIDTH_SCALED variable stored in settings.py script), rounded down.

        Used to construct texture object's horizontal boundary range; to check the proximity of the
        user's cursor to the left-most coordinate x of the card when choosing a priority hover 
        target.

        Cached.

        :return int: Texture object's left-most coordinate x (boundary) integer value.
        """

        # Calculating boundary coordinate:
        boundary_coordinate_x: int = int(self.coordinate_x - CARD_TEXTURE_WIDTH_SCALED / 2)

        # Returning:
        return boundary_coordinate_x
    

    @cached_property
    def boundary_right(self) -> int:
        """
        Texture object's right-most coordinate x (boundary) integer value.

        Calculates and returns right-most coordinate x by adding half of texture width scaled value 
        (CARD_TEXTURE_WIDTH_SCALED variable stored in settings.py script), rounded down.

        Used to construct texture object's horizontal boundary range.

        Cached.

        :return int: Texture object's right-most coordinate x (boundary) integer value.
        """

        # Calculating boundary coordinate:
        boundary_coordinate_x: int = int(self.coordinate_x + CARD_TEXTURE_WIDTH_SCALED / 2)

        # Returning:
        return boundary_coordinate_x
    

    @cached_property
    def boundary_bottom(self) -> int:
        """
        Texture object's bottom-most coordinate y (boundary) integer value.

        Calculates and returns bottom-most coordinate y by subtractig half of texture height scaled
        value (CARD_TEXTURE_HEIGHT_SCALED variable stored in settings.py script), rounded down.

        Used to construct texture object's vertical boundary range.

        Cached.

        :return int: Texture object's bottom-most coordinate y (boundary) integer value.
        """

        # Calculating boundary coordinate:
        boundary_coordinate_y: int = int(self.coordinate_y - CARD_TEXTURE_HEIGHT_SCALED / 2)

        # Returning:
        return boundary_coordinate_y
    

    @cached_property
    def boundary_top(self) -> int:
        """
        Texture object's top-most coordinate y (boundary) integer value.

        Calculates and returns top-most coordinate y by adding half of texture height scaled 
        value (CARD_TEXTURE_HEIGHT_SCALED variable stored in settings.py script), rounded down.

        Used to construct texture object's vertical boundary range.

        Cached.

        :return int: Texture object's top-most coordinate y (boundary) integer value.
        """

        # Calculating boundary coordinate:
        boundary_coordinate_y: int = int(self.coordinate_y + CARD_TEXTURE_WIDTH_SCALED / 2)

        # Returning:
        return boundary_coordinate_y
    

    @cached_property
    def boundary_range_horizontal(self) -> range:
        """
        Texture object's horizontal boundary range (from left-most to the right-most coordinates x).

        Takes boundary_left and boundary_right cached properties and puts them together in a range.
        Used together with boundary_range_vertical cached property to determine whether a cursor is
        within the texture object's boundaries (when hovering over or clicking).

        Cached.

        :return range: Texture object's horizontal boundary range (from left-most to the right-most 
            coordinates x).
        """

        # Generating boundary range:
        boundary_range_horizontal: range = range(
            self.boundary_left,
            self.boundary_right
            )
        
        # Returning:
        return boundary_range_horizontal
    

    @cached_property
    def boundary_range_vertical(self) -> range:
        """
        Texture object's vertical boundary range (from bottom-most to the top-most coordinates y).

        Takes boundary_bottom and boundary_rop cached properties and puts them together in a range.
        Used together with boundary_range_horizontal cached property to determine whether a cursor 
        is within the texture object's boundaries (when hovering over or clicking).

        Cached.

        :return range: Texture object's vertical boundary range (from bottom-most to the top-most 
            coordinates y).
        """

        # Generating boundary range:
        boundary_range_vertical: range = range(
            self.boundary_bottom,
            self.boundary_top
            )
        
        # Returning:
        return boundary_range_vertical
    
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    RENDER METHODS AND PROPERTIES BLOCK
    
    Render methods and properties allow the card object to be rendered on screen and be responsive 
    to their current state in game. 
    
    Cached render properties choose scale modifier, generate a  random rotation angle, calculate 
    texture width and height (applied to arcade.Rect object first) and select a correct texture 
    object to render.

    Main render() method uses arcade library's native method draw_texture_rect() to display the 
    selected texture over an arcade.Rect object generated in __render_rect property in the set
    card object's coordinates x and y.

    """


    @cached_property
    def render_scale(self) -> float:
        """
        Texture object's scale float value.

        Selected based on card object's selected state by choosing between its default value and 
        selected value set in settings.py script.

        Used to apply a scale modifier when calculating texture width and height properties.

        Cached.

        :return float: Texture object's scale float value. CARD_RENDER_SCALE_DEFAULT value by 
            default if not selected, or CARD_RENDER_SCALE_SELECTED value otherwise.
        """

        # Selecting a larger render scale value if card is selected:
        if self.state_selected:
            render_scale_selected: float = CARD_RENDER_SCALE_SELECTED

        # Selecting a default render scale value:
        else:
            render_scale_selected: float = CARD_RENDER_SCALE_DEFAULT

        # Retutrning:
        return render_scale_selected
    

    @cached_property
    def render_angle(self) -> int:
        """
        Texture object's rotate angle integer value.

        Calculated based on card object's selected state by choosing a random axis (-1 to rotate
        counter clockwise, or +1 to rotate clockwise), and a random angle from range of minimal 
        angle and maximum angle set in settings.py script. Default rotation angle is set to 0 if 
        card object is not selected. Uses random library.

        Used to apply a rotation angle to rendered texture on screen based on card object's state
        in game.

        Cached.

        :return int: Texture object's rotate angle integer value, 0 by default, random between 
            CARD_RENDER_ANGLE_MIN and CARD_RENDER_ANGLE_MAX (settings.py script) which can be 
            positive or negative.
        """

        # Generating a random render angle if card is selected:
        if self.state_selected:
            render_angle_axis: int = random.choice(CARD_RENDER_ANGLE_AXIS_LIST)
            render_angle_random: int = random.randint(
                a = CARD_RENDER_ANGLE_MIN,
                b = CARD_RENDER_ANGLE_MAX
                )
            render_angle_selected: int = render_angle_random * render_angle_axis

        # Selecting a default render angle:
        else:
            render_angle_selected: int = CARD_RENDER_ANGLE_DEFAULT

        # Returning:
        return render_angle_selected
    

    @cached_property
    def render_width(self) -> int:
        """
        Texture object's width integer value. 
        
        Calculated using other cached property render_scale. Used to create an arcade.Rect object
        to draw texture in with main render() method. 

        Cached.

        :return int: Texture object's width integer value.
        """

        # Calculating:
        render_width: int = CARD_TEXTURE_WIDTH_SCALED * self.render_scale

        # Returning:
        return render_width
    

    @cached_property
    def render_height(self) -> int:
        """
        Texture object's height integer value. 
        
        Calculated using other cached property render_scale. Used to create an arcade.Rect object
        to draw texture in with main render() method. 

        Cached.

        :return int: Texture object's height integer value.
        """

        # Calculating:
        render_height: int = CARD_TEXTURE_HEIGHT_SCALED * self.render_scale

        # Returning:
        return render_height
    

    @cached_property
    def render_texture(self) -> arcade.Texture:
        """
        Arcade library's Texture object selected to render..

        Used to select correct texture object: front of cover of the card, based on its revealed
        state. If card is revealed, this property will return the front texture, otherwise it will
        always return the cover (universal to all cards of the same texture pack).

        Cached.

        :return arcade.Texture: Arcade library's Texture object selected to render.
        """

        # Selecting front card texture object if card is revealed:
        if self.state_revealed:
            render_texture: Texture = self.__texture_front_object
        
        # Selecting cover card texture object if card is not revealed:
        else:
            render_texture: Texture = self.__texture_cover_object

        # Returning:
        return render_texture


    @property
    def __render_rect(self) -> arcade.Rect:
        """
        Arcade library's Rect class object at card object's coordinates x and y, and with width
        and height set as card texture width and height scaled down (set and adjusted in settings.py
        script).

        Used to render card object's texture over. In a way, this is a container that sets width,
        height and coordinates of the texture to fit in and be rendered at.

        :return arcade.Rect:Arcade library's Rect class object at card object's coordinates x and y, 
        and with width and height of scaled texture.
        """

        # Creating a new instance of arcade rectangle:
        render_rect: Rect = arcade.XYWH(
            x      = self.coordinate_x,
            y      = self.coordinate_y,
            width  = self.render_width,
            height = self.render_height
            )
        
        # Returning:
        return render_rect
    

    def render(self) -> None:
        """
        Main render method. Draws card object's selected texture on screen.

        Uses arcade library's draw_texture_rect() method to draw texture over this class private 
        property __render_rect (returns arcade.Rect) that sets the coordinates and dimensions of 
        the texture.
        """

        # Rendering:
        arcade.draw_texture_rect(
            texture = self.render_texture,
            rect    = self.__render_rect,
            angle   = self.render_angle
            )
        
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    SLIDE METHODS BLOCK
    
    Slide methods provide interaction between player's mouse movement and the card objects active
    on the screen. Slide (as a generic method) simply shifts the card object's coordinates by a set
    number of pixels based on CARD_SLIDE_SPEED value stored in settings.py depending on its current
    position on the screen and its hover state (for card hovering animation).

    These methods on their own call on coordinates setter methods if they determine that their card 
    object's coordinates x and/or y do not match the destination (either given as a parameter or 
    set in cached properties and based on settings.py script variable, e.g. coordinate y of the 
    center coordinate y poisition of player's hand position - CARD_COORDINATE_Y_HAND_PLAYER).

    """


    def __slide(self, coordinates_end: tuple[int, int], slide_speed_modifier: float) -> None:
        """
        Adjusts card object's coordinates x and y depending on any existing differences between
        card object's current coordinates and parameter coordinates_end. General purpose private 
        method, called by specific slide methods, e.g. slide_stack() or slide_hand().

        Calculates card object's next position one each step of applying CARD_SLIDE_SPEED value
        to current coordinates and sets new coordinates via coordinates setter methods if they do
        not match yet. If coordinates "slided over", uses coordinates setter methods to set card 
        object's current coordinates directly to end coordinates.

        Autmatically clears coordinates related cache properties via coordinate setter methods.

        :param tuple[int, int] coordinates_end: Tuple container with coordinates x and y integer
            values to navigate card object's movement.
        :param float slide_speed_modifier: Float value modifier that is used to multiply default
            slide speed CARD_SLIDE_SPEED defined and stored in settings.py. 
        """

        # Calculating speed:
        slide_speed: int = int(CARD_SLIDE_SPEED * slide_speed_modifier)

        # Unpacking end coordinates:
        coordinate_x_end, coordinate_y_end = coordinates_end

        # Calculating coordinate x slide:
        slide_axis_x: int = +1
        if self.coordinate_x > coordinate_x_end:
            slide_axis_x: int = -1
        coordinate_x_next: int = int(self.coordinate_x + slide_speed * slide_axis_x)
        slide_over: bool = bool(
            coordinate_x_next < coordinate_x_end and slide_axis_x == - 1 or
            coordinate_x_next > coordinate_x_end and slide_axis_x == + 1
            )
        if slide_over:
            coordinate_x_next: int = coordinate_x_end

        # Calculating coordinate x slide:
        slide_axis_y: int = +1
        if self.coordinate_y > coordinate_y_end:
            slide_axis_y: int = -1
        coordinate_y_next: int = int(self.coordinate_y + slide_speed * slide_axis_y)
        slide_over: bool = bool(
            coordinate_y_next < coordinate_y_end and slide_axis_y == - 1 or
            coordinate_y_next > coordinate_y_end and slide_axis_y == + 1
            )
        if slide_over:
            coordinate_y_next: int = coordinate_y_end

        # Packing:
        coordinates_next: tuple[int, int] = (
            coordinate_x_next, 
            coordinate_y_next
            )

        # Updating coordinates:
        self.set_coordinates(
            set_value = coordinates_next,
            )
        

    def slide_hand(self) -> None:
        """
        Slides the card object vertically if card is in a hand depending on its current coordinate y
        and state hovered.

        If hovered, but not at the hand hover coordinate, will slide the card slightly to the top 
        to highlight it. If not hovered, but not at default hand coordinate y, will slide the card 
        back to its position. Slide speed depends on slide direction.

        Relies on cached methods' calculated coordinate_y_hand and coordinate_y_hand_hover.

        :raise AssertionError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected integer).
        """

        # Checking card's location:
        if self.location == VAR_CARD_LOCATION_HAND:
            slide_required: bool = False

            # If card's current state is hovered:
            if self.state_hovered:
                if self.coordinate_y != self.coordinate_y_hand_hover:
                    slide_required: bool = True
                    slide_speed_modifier: float = CARD_SLIDE_SPEED_MOD_INCREASED
                    coordinates_end: tuple[int, int] = (
                        self.coordinate_x,
                        self.coordinate_y_hand_hover
                        )

            # If card's current state is NOT hovered:
            else:
                if self.coordinate_y != self.coordinate_y_hand:
                    slide_required: bool = True
                    slide_speed_modifier: float = CARD_SLIDE_SPEED_MOD_DEFAULT
                    coordinates_end: tuple[int, int] = (
                        self.coordinate_x,
                        self.coordinate_y_hand
                        )
            
            # Sliding to the correct position:
            if slide_required:
                self.__slide(
                    coordinates_end = coordinates_end,
                    slide_speed_modifier = slide_speed_modifier
                    )
                
    
    def slide_stack(self, coordinate_x_spot: int) -> None:
        """
        Slides the card object horizontally if card is on the table as in on the top stack position,
        depending on its current coordinate x and state hovered.

        If hovered, but not at the stack hover coordinate, will slide the card slightly to the 
        right to reveal the card underneath it. If not hovered, but not at default stack coordinate,
        will slide the card back to its position. Slide speed depends on slide direction.

        :param int coordinate_x_spot: Coordinate x integer value of the card object's default 
            position on table based on its position_table idnex value. Calculated by DeckController
            object and fed into the method.

        :raise AssertionError: (If enabled) Raises AssertionError if parameter value type is 
            invalid (expected integer).
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting set value is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = coordinate_x_spot,
                valid_type = valid_type,
                raise_error = True
                )

        # Checking card's location:
        if self.location == VAR_CARD_LOCATION_TABLE:
            slide_required: bool = False

            # If card's stack index is top:
            if self.position_stack == TABLE_STACK_TOP_INDEX:

                # If card's current state is hovered:
                if self.state_hovered:
                    coordinate_x_end: int = coordinate_x_spot + CARD_SLIDE_DISTANCE_HOVER_STACK,
                    if self.coordinate_x != coordinate_x_end:
                        slide_required: bool = True
                        slide_speed_modifier: float = CARD_SLIDE_SPEED_MOD_INCREASED
                        coordinates_end: tuple[int, int] = (
                            coordinate_x_end,
                            CARD_COORDINATE_Y_TABLE
                            )
                
                # If card's current state is NOT hovered:
                else:
                    if self.coordinate_x != coordinate_x_spot:
                        slide_required: bool = True
                        slide_speed_modifier: float = CARD_SLIDE_SPEED_MOD_DEFAULT
                        coordinates_end: tuple[int, int] = (
                            coordinate_x_spot,
                            CARD_COORDINATE_Y_TABLE
                            )
                        
            # Sliding to the correct position:
            if slide_required:
                self.__slide(
                    coordinates_end = coordinates_end,
                    slide_speed_modifier = slide_speed_modifier
                    )
