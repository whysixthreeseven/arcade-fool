# Typing and annotation import:
from typing import Literal

# Cache-related modules and scripts import:
from game.scripts import clear_cached_property
from functools import cached_property

# Settings and variables import list:
from game.variables import *
from game.settings import *

# Assertion functions import:
from game.scripts import (
    assert_value_is_default,
    assert_value_is_valid_type,
    assert_value_in_valid_range,
    )


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
SESSION CONTROLLER BLOCK

"""


# GLOBALLY AVAILABLE developer session flags:
DEV_ENABLE_ASSERTION: bool = False
DEV_ENABLE_ECHO: bool = True
DEV_ENABLE_DEBUG_RENDER: bool = True


class SessionController:

    # Sort method available list:
    SESSION_SORT_METHOD_LIST: tuple[str, ...] = (
        VAR_SESSION_SORT_METHOD_SUIT,
        VAR_SESSION_SORT_METHOD_VALUE,
        VAR_SESSION_SORT_METHOD_VALUE_CLEAN,
        VAR_SESSION_SORT_METHOD_ADDED
        )

    def __init__(self):

        # User settings:
        self.__user_name: str = VAR_PLAYER_NAME_ONE_DEFAULT
        
        # Menu selections:
        self.__sort_method:  str = VAR_SESSION_SORT_METHOD_SUIT
        self.__texture_pack: str = VAR_CARD_TEXTURE_PACK_DEFAULT

        # Game settings:
        self.__enable_hint:          bool = False
        self.__enable_reverse:       bool = False
        self.__enable_swap_trump:    bool = False
        self.__enable_click_to_play: bool = False


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    MISC METHODS BLOCK
    
    Miscellaneous private methods related to controller designed to reduce code repetition and 
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
    their block's cachced property lists (e.g. __cached_sort_method_property_list would return all 
    the cached property (attribute) string value names to clear via a different clear cache 
    function).

    These tuple containers are stored as cached properties within the class and not made as 
    wrappers due to some of the setter methods optional cache clearing policy and other methods 
    aiming to clear only one (or two) cached property (attribute) at a time, but not the whole 
    block, e.g. set_coordinate_x will only clear a coordinate_x cached property (and other within
    a different block).

    """


    @cached_property
    def __cached_sort_method_property_list(self) -> tuple[str, ...]:
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
            "sort_method_current",
            "sort_method_next",
            "sort_method_previous",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_texture_pack_property_list(self) -> tuple[str, ...]:
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
            "texture_pack_current",
            "texture_pack_next",
            "texture_pack_previous",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_enable_flags_property_list(self) -> tuple[str, ...]:
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
            "enable_hint",
            "enable_reverse",
            "enable_swap_trump",
            "enable_click_to_play",
            )
        
        # Returning:
        return cached_property_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    USER METHODS & PROPERTIES BLOCK

    """


    @cached_property
    def user_name(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__user_name
    

    def set_user_name(self, set_value: str) -> None:
        """
        TODO: Create a docstring.
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

        # Updating attribute:
        if self.user_name != set_value:
            self.__user_name: str = set_value

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "user_name"
                )
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    SORT METHODS & PROPERTIES BLOCK

    """


    @cached_property
    def sort_method_current(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__sort_method
    

    @cached_property
    def sort_method_default(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return VAR_SESSION_SORT_METHOD_SUIT
    

    @cached_property
    def sort_method_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.

        Cached. Cannot be removed.
        """

        # Returning:
        return self.SESSION_SORT_METHOD_LIST
    

    @cached_property
    def __sort_method_count(self) -> int:
        """
        TODO: Create a docstring.

        Cached. Cannot be removed.
        """

        # Calculating:
        sort_method_count: int = len(self.sort_method_list)

        # Returning:
        return sort_method_count
    

    @cached_property
    def sort_method_next(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Getting index:
        index_current: int = self.sort_method_list.index(
            self.sort_method_current
            )
        index_next: int = index_current + 1
        if index_next >= self.__sort_method_count:
            index_next: int = 0
        
        # Getting sort method:
        sort_method: str = self.sort_method_list[index_next]

        # Returning:
        return sort_method


    @cached_property
    def sort_method_previous(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Getting index:
        index_current: int = self.sort_method_list.index(
            self.sort_method_current
            )
        index_previous: int = index_current - 1
        if index_previous < 0:
            index_previous: int = -1        # Redundant, but safe.

        # Getting sort method:
        sort_method: str = self.sort_method_list[index_previous]

        # Returning:
        return sort_method


    def set_sort_method(self, 
                        set_value: str, 
                        ignore_assertion: bool = False,
                        clear_cache: bool = True
                        ) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = str
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default:
            valid_list: tuple[str, ...] = self.sort_method_list
            assert_value_is_default(
                check_value = set_value,
                valid_list  = valid_list,
                raise_error = True
                )

        # Updating attribute:
        if self.sort_method_current != set_value:
            self.__sort_method: str = set_value

            # Clearing cache:
            if clear_cache:
                self.__clear_cached_property_list(
                    target_list = self.__cached_sort_method_property_list
                    )
        
    
    def set_sort_method_default(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        self.__sort_method: str = self.set_sort_method(
            set_value = self.sort_method_default,
            ignore_assertion = True,
            clear_cache = True,
            )
    

    def switch_sort_method(self, switch_axis: Literal[-1, +1] = 1) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = switch_axis,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default:
            valid_list: tuple[str, ...] = (
                VAR_SESSION_ITEM_PREV,
                VAR_SESSION_ITEM_NEXT
                )
            assert_value_is_default(
                check_value = switch_axis,
                valid_list  = valid_list,
                raise_error = True
                )

        # Getting sort method:
        sort_method_selected: str = str(
            self.sort_method_next if switch_axis == VAR_SESSION_ITEM_NEXT else
            self.sort_method_previous
            )
        
        # Updating attribute:
        self.__sort_method: str = self.set_sort_method(
            set_value = sort_method_selected,
            ignore_assertion = True,
            clear_cache = True
            )
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    TEXTURE PACK METHODS & PROPERTIES BLOCK

    """


    @cached_property
    def texture_pack_current(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__texture_pack
    

    @cached_property
    def texture_pack_default(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return VAR_CARD_TEXTURE_PACK_DEFAULT
    

    @cached_property
    def texture_pack_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating list (temp):
        texture_pack_list: tuple[str, ...] = (
            VAR_CARD_TEXTURE_PACK_DEFAULT,
            )
        
        # Returning:
        return texture_pack_list
    

    @cached_property
    def __texture_pack_count(self) -> int:
        """
        TODO: Create a docstring.

        Cached. Cannot be removed.
        """

        # Calculating:
        texture_pack_count: int = len(self.texture_pack_list)

        # Returning:
        return texture_pack_count
    

    @cached_property
    def texture_pack_next(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Getting index:
        index_current: int = self.texture_pack_list.index(
            self.texture_pack_current
            )
        index_next: int = index_current + 1
        if index_next >= self.__texture_pack_count:
            index_next: int = 0
        
        # Getting sort method:
        texture_pack: str = self.texture_pack_list[index_next]

        # Returning:
        return texture_pack


    @cached_property
    def texture_pack_previous(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Getting index:
        index_current: int = self.texture_pack_list.index(
            self.texture_pack_current
            )
        index_previous: int = index_current - 1
        if index_previous < 0:
            index_previous: int = -1        # Redundant, but safe.

        # Getting sort method:
        texture_pack: str = self.texture_pack_list[index_previous]

        # Returning:
        return texture_pack
    

    def set_texture_pack(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = str
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default:
            valid_list: tuple[str, ...] = self.texture_pack_list
            assert_value_is_default(
                check_value = set_value,
                valid_list  = valid_list,
                raise_error = True
                )

        # Updating attribute:
        if self.texture_pack_current != set_value:
            self.__texture_pack: str = set_value

            # Clearing cache:
            self.__clear_cached_property_list(
                target_list = self.__cached_texture_pack_property_list
                )
        
    
    def set_texture_pack_default(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        self.set_texture_pack(
            set_value = self.texture_pack_default,
            ignore_assertion = True,
            clear_cache = True,
            )
    

    def switch_texture_pack(self, switch_axis: Literal[-1, +1] = 1) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = int
            assert_value_is_valid_type(
                check_value = switch_axis,
                valid_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default:
            valid_list: tuple[str, ...] = (
                VAR_SESSION_ITEM_PREV,
                VAR_SESSION_ITEM_NEXT
                )
            assert_value_is_default(
                check_value = switch_axis,
                valid_list  = valid_list,
                raise_error = True
                )

        # Getting sort method:
        texture_pack_selected: str = str(
            self.texture_pack_next if switch_axis == VAR_SESSION_ITEM_NEXT else
            self.texture_pack_previous
            )
        
        # Updating attribute:
        self.set_sort_method(
            set_value = texture_pack_selected,
            ignore_assertion = True,
            clear_cache = True
            )
        
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ENABLE FLAGS METHODS & PROPERTIES BLOCK

    """

    
    @cached_property
    def enable_hint(self) -> bool:
        """
        TODO: Create docstring
        """

        # Returning:
        return self.__enable_hint
    

    @cached_property
    def enable_reverse(self) -> bool:
        """
        TODO: Create docstring
        """

        # Returning:
        return self.__enable_reverse
    

    @cached_property
    def enable_swap_trump(self) -> bool:
        """
        TODO: Create docstring
        """

        # Returning:
        return self.__enable_swap_trump
    

    @cached_property
    def enable_click_to_play(self) -> bool: 
        """
        TODO: Create docstring
        """

        # Returning:
        return self.__enable_click_to_play
    

    def reset_enable_flags(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attributes:
        self.__enable_hint:          bool = False
        self.__enable_reverse:       bool = False
        self.__enable_swap_trump:    bool = False
        self.__enable_click_to_play: bool = False

        # Clearing cache:
        self.__clear_cached_property_list(
            target_list = self.__cached_enable_flags_property_list
            )
    

    def set_enable_hint(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )
        
        # Updating attribute:
        if self.enable_hint != set_value:
            self.__enable_hint: bool = set_value

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "enable_hint"
                )
    

    def switch_enable_hint(self) -> None:
        """
        TODO: Create a dictring.
        """

        # Switching flag value:
        switch_value: bool = True if not self.enable_hint else False
        self.set_enable_hint(
            set_value = switch_value,
            ignore_assertion = True,
            )
        
    
    def set_enable_reverse(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )
        
        # Updating attribute:
        if self.enable_reverse != set_value:
            self.__enable_reverse: bool = set_value

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "enable_reverse"
                )
    

    def switch_enable_reverse(self) -> None:
        """
        TODO: Create a dictring.
        """

        # Switching flag value:
        switch_value: bool = True if not self.enable_reverse else False
        self.set_enable_reverse(
            set_value = switch_value,
            ignore_assertion = True,
            )


    def set_enable_swap_trump(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )
        
        # Updating attribute:
        if self.enable_swap_trump != set_value:
            self.__enable_swap_trump: bool = set_value

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "enable_swap_trump"
                )
    

    def switch_enable_swap_trump(self) -> None:
        """
        TODO: Create a dictring.
        """

        # Switching flag value:
        switch_value: bool = True if not self.enable_swap_trump else False
        self.set_enable_swap_trump(
            set_value = switch_value,
            ignore_assertion = True,
            )

    
    def set_enable_click_to_play(self, set_value: bool, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )
        
        # Updating attribute:
        if self.enable_click_to_play != set_value:
            self.__enable_click_to_play: bool = set_value

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "enable_click_to_play"
                )
    

    def switch_enable_click_to_play(self) -> None:
        """
        TODO: Create a dictring.
        """

        # Switching flag value:
        switch_value: bool = True if not self.enable_click_to_play else False
        self.set_enable_click_to_play(
            set_value = switch_value,
            ignore_assertion = True,
            )
