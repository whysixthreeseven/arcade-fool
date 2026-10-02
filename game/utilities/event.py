# Typing and annotations:
from __future__ import annotations

# External libraries:
import random
import arcade

# Settings, session and context:
from game.settings import SETTINGS
from game.session import SESSION
from game import context

# Cache management:
from functools import cached_property
from game.utilities.scripts import cache

# Various utilities:
from game.utilities import coordinates, texturepack
from game.utilities.scripts import assertion, validate


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    EVENT CLASS OBJECT CONSTRUCTOR

"""


class Event:
    
    def __init__(self) -> None:
        
        # Core attributes:
        self.__type: str = None
        self.__name: str = None
        self.__description: str = None
        self.__condition: str = None
            
        # Status attributes:
        self.__ongoing: bool = False
        self.__wait: bool = False
        self.__finished: bool = False
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CLASS METHODS
    
    """
    
    
    @classmethod
    def generate(cls, init_name: str, init_type: str, init_description: str, init_condition: str,
                      ignore_assertion: bool = False) -> Event:
        
        # Creating event class object:
        event_object: Event = Event()
        
        # Setting core attributes:
        event_object.set_name(
            set_value = init_name,
            ignore_assertion = ignore_assertion,
            clear_cache = True,
            )
        event_object.set_type(
            set_value = init_type,
            ignore_assertion = ignore_assertion,
            clear_cache = True,
            )
        event_object.set_description(
            set_value = init_description,
            ignore_assertion = ignore_assertion,
            clear_cache = True,
            )
        event_object.set_condition(
            set_value = init_condition,
            ignore_assertion = ignore_assertion,
            clear_cache = True,
            )
        
        # Returning:
        return event_object
    
    
    @classmethod
    def generate_predefined(cls, event_name: str, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = event_name,
                check_type = str,
                raise_error = True,
                )
            assertion.assert_value_default(
                check_value = event_name,
                check_list = context.EVENT_NAME_LIST,
                )
            
        # Selecting correct values:
        event_type: str = context.EVENT_TYPE_INDEX[event_name]
        event_description: str = context.EVENT_DESCRIPTION_INDEX[event_name]
        event_condition: str = context.EVENT_CONDITION_INDEX[event_name]

        # Generating event:
        event_object: Event = Event.generate(
            init_name = event_name,
            init_type = event_type,
            init_description = event_description,
            init_condition = event_condition,
            ignore_assertion = ignore_assertion,
            )
        
        # Returning:
        return event_object
        
    
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
            "type",
            "name",
            "description",
            "condition",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_status_attributes(self) -> tuple[str, ...]:
        """
        Status attributes-related cached properties list.
        
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
            "ongoing",
            "wait",
            "finished",
            )
        
        # Returning:
        return cached_property_list
    
    
    def clear_cached_status_attributes(self) -> None:
        """
        Clears all public cached status properties of this event object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear texturepack properties of this card object.
        """

        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_status_attributes
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
            self.__cached_status_attributes,
            )
        
        # Looping throught the list and clearing cache:
        for cached_property_list in cached_property_list_collection:
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CORE CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def type(self) -> str:
        
        # Returning:
        return self.__type
    
    
    @cached_property
    def name(self) -> str:

        # Returning:
        return self.__name


    @cached_property
    def description(self) -> str:

        # Returning:
        return self.__description


    @cached_property
    def condition(self) -> str:

        # Returning:
        return self.__condition
    
    
    def set_type(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = str,
                raise_error = True,
                )
            assertion.assert_value_default(
                check_value = set_value,
                check_list = context.EVENT_NAME_LIST,
                )
            
        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "type",
                sentinel_value = None,
                raise_error = True
                )
            
        # Updating attribute:
        self.__type = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "type"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            

    def set_name(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = str,
                raise_error = True,
                )
            assertion.assert_value_default(
                check_value = set_value,
                check_list = context.EVENT_NAME_LIST,
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
            cached_property: str = "name"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
                
    
    def set_description(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = str,
                raise_error = True,
                )
            assertion.assert_value_default(
                check_value = set_value,
                check_list = context.EVENT_DESCRIPTION_LIST,
                raise_error = True
                )

        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "description",
                sentinel_value = None,
                raise_error = True
                )

        # Updating attribute:
        self.__description = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "description"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_condition(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = str,
                raise_error = True,
                )
            assertion.assert_value_default(
                check_value = set_value,
                check_list = context.EVENT_CONDITION_LIST,
                raise_error = True
                )

        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "condition",
                sentinel_value = None,
                raise_error = True
                )

        # Updating attribute:
        self.__condition = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "condition"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        STATUS CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def ongoing(self) -> bool:
        
        # Returning:
        return self.__ongoing


    @cached_property
    def wait(self) -> bool:

        # Returning:
        return self.__wait
    
    
    @cached_property
    def finished(self) -> bool:

        # Returning:
        return self.__finished
    
    
    def set_ongoing(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )
            
        # Updating attribute:
        self.__ongoing = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "ongoing"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )


    def switch_ongoing(self, clear_cache: bool = True) -> None:
        
        # Switching:
        self.set_ongoing(
            set_value = not self.ongoing,
            clear_cache = clear_cache
            )
        
    
    def set_wait(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )
            
        # Updating attribute:
        self.__wait = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "wait"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def switch_wait(self, clear_cache: bool = True) -> None:

        # Switching:
        self.set_wait(
            set_value = not self.wait,
            clear_cache = clear_cache
            )

    
    def set_finished(self, set_value: bool, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__finished = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "finished"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    
    
    def switch_finished(self, clear_cache: bool = True) -> None:

        # Switching:
        self.set_finished(
            set_value = not self.finished,
            clear_cache = clear_cache
            )
    

""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    EVENT CLASS OBJECTS COLLECTION
    
"""


EVENT_DRAW_CARDS: Event = Event.generate_predefined(
    event_name = context.EVENT_NAME.DRAW,
    ignore_assertion = False,
    )

