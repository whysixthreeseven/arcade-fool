# Card class object:
from game.controller.card import Card

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
from game.utilities import texturepack
from game.utilities.scripts import validate


class Table:
    
    def __init__(self) -> None:
        
        # Core attributes:
        self.__cards_index: dict[int, Card | None] = {
            location_index: None for location_index in range(0, 12)
            }
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_cards_attributes(self) -> tuple[str, ...]:
        """
        Cards attributes-related cached properties list.
        
        Collects and returns all properties of this table object decorated with `functools` library's `cached_property` wrapper.
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
            "cards",
            "cards_index",
            "cards_count",
            "cards_value",
            "cards_playable",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_position_attributes(self) -> tuple[str, ...]:
        """
        Position-related cached properties list.
        
        Collects and returns all properties of this table object decorated with `functools` library's `cached_property` wrapper.
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
            "position_attack_list",
            "position_defence_list",
            )
        
        # Returning:
        return cached_property_list
    
    
    def clear_cached_cards_attributes(self) -> None:
        """
        Clears all public cached card properties of this table object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear texturepack properties of this table object.
        """
    
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_cards_attributes
            )
        
    
    def clear_cached_position_attributes(self) -> None:
        """
        Clears all public cached position properties of this table object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear texturepack properties of this table object.
        """
    
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_position_attributes
            )
        
    
    def clear_cached_attributes(self) -> None:
        """
        Clears all public cached properties of this table object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and all property lists available to
        clear all cached properties of this table object in a single loop through lists collection.
        """
            
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_cards_attributes,
            self.__cached_position_attributes,
            )
        
        # Looping throught the list and clearing cache:
        for cached_property_list in cached_property_list_collection:
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
            
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SETUP METHODS
    
    """
    
    
    def __create_index(self) -> dict[int, Card | None]:
        
        # Creating new cards index dictionary:
        cards_index: dict[int, Card | None] = {
            card_location_index: None for card_location_index in range(0, 12)
            }
        
        # Returning:
        return cards_index
        
    
    def setup(self) -> None:
        
        # Creating new cards index dictionary:
        cards_index: dict[int, Card | None] = self.__create_index()
        
        # Updating attribute:
        self.__cards_index = cards_index
        
        # Clearing cache:
        self.clear_cached_attributes()
        
        
    def reset(self) -> None:
        
        # Creating new cards index dictionary:
        cards_index: dict[int, Card | None] = self.__create_index()
        
        # Updating attribute:
        self.__cards_index = cards_index
        
        # Clearing cache:
        self.clear_cached_attributes()
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARDS CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def cards(self) -> tuple[Card, ...]:
        
        # Converting list to tuple:
        card_list: tuple[Card, ...] = tuple(
            card_object for card_location_index, card_object in self.cards_index.items()
            if card_object is not None
            )

        # Returning:
        return card_list
    
    
    @cached_property
    def cards_index(self) -> dict[int, Card | None]:
        
        # Returning:
        return self.__cards_index


    @cached_property
    def cards_count(self) -> int:
        
        # Calculating:
        cards_count: int = len(self.cards)

        # Returning:
        return cards_count


    @cached_property
    def cards_value(self) -> int:
        
        # Calculating:
        cards_value: int = sum(card_object.value for card_object in self.cards)

        # Returning:
        return cards_value
    
    
    @cached_property
    def cards_playable(self) -> tuple[str, ...]:
        
        # Collecting all card names:
        card_name_list: tuple[str, ...] = tuple(
            card_object.name for card_object in self.cards
            )
        
        # Returning:
        return card_name_list
    
    
    def add_card(self, card_object: Card, location_index: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_object(
                validate_value = card_object
                )
            validate.validate_card_location_index(
                validate_value = location_index
                )
        
        # Raising error, if card already exists on table:
        cards_list: tuple[Card, ...] = tuple(
            card_object for card_location_index, card_object in self.__cards_index.items()
                if card_object is not None
            )
        card_exists: bool = bool(
            self.__cards_index[location_index] is not None 
                and card_object not in cards_list
            )
        if card_exists:
            error_message: str = f"Card exists on table @{location_index}!"
            raise IndexError(error_message)
        
        # Adding card:
        self.__cards_index[location_index] = card_object
        
        # Updating card added index:
        card_object.set_added_index(
            set_value = location_index,
            ignore_assertion = True,
            clear_cache = True
            )
        
        # Updatin card's tilt:
        card_object.set_render_tilt(
            set_value = card_object.render_tilt_default,
            ignore_assertion = True,
            clear_cache = True
            )
        
        # Updating card's location:
        location: context.Location = (
            context.CARD_LOCATION.DISCARD,
            location_index
            )
        card_object.set_location(
            set_value = location,
            ignore_assertion = True,
            clear_cache = True
            )
        
        # Updating known state (before resetting other states):
        if card_object.state_revealed and not card_object.state_known:
            card_object.set_state_known(
                set_value = True,
                ignore_assertion = True,
                clear_cache = True
                )
            
        # Updating card's states:
        card_object.set_state_location(
            clear_cache = True
            )
        
        # Updating card's coordinates:
        card_object.update_coordinates_location(
            calculated_coordinates = None,
            clear_cache = True,
            )
        card_object.set_coordinates_expected(
            set_value = card_object.coordinates_position,
            ignore_assertion = True,
            clear_cache = True,
            )
        
        # Clearing cache:
        if clear_cache:
            self.clear_cached_cards_attributes()
            self.clear_cached_position_attributes()
            
            
    def remove_card(self, card_object: Card, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_object(
                validate_value = card_object
                )
            
        # Locating and removing card:
        for stack_index, card_stored in self.__cards_index.items():
            if card_stored == card_object:
                self.cards_index[stack_index] = None
                break
            
        # Raising error, if card is not found:
        else:
            error_message: str = f"Card <{card_object}> not found on table!"
            raise IndexError(error_message)

        # Clearing cache, if required:
        if clear_cache:
            self.clear_cached_cards_attributes()
            self.clear_cached_position_attributes()
            
    
    def sweep(self, clear_cache: bool = True) -> tuple[Card, ...]:
        
        # Collecting all cards:
        cards_pending_removal: tuple[Card, ...] = self.cards
        for card_object in cards_pending_removal:
            self.remove_card(
                card_object = card_object,
                clear_cache = False
                )
    
        # Cleaning cache, if required:
        if clear_cache:
            self.clear_cached_cards_attributes()
            self.clear_cached_position_attributes()
        
        # Returning:
        return cards_pending_removal
        
            
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        POSITIONS CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def position_attack_list(self) -> tuple[int, ...]:
        
        # Searching for empty positions on bottom stack:
        position_list: tuple[int, ...] = tuple(
            position_index for position_index, card_object in self.cards_index.items()
                if position_index % 2 == 0 and card_object is not None      # Bottom stack is empty
            )
        
        # Returning:
        return position_list
    
    
    @cached_property
    def position_defence_list(self) -> tuple[int, ...]:
        
        # Searching for empty positions on top stack:
        position_list: tuple[int, ...] = tuple(
            position_index for position_index, card_object in self.cards_index.items()
                if position_index % 2 == 0 and card_object is not None      # Bottom stack has cards
                    and self.cards_index[position_index + 1] is None        # Top stack is empty
            )
        
        # Returning:
        return position_list
    
    
    def get_position_attack(self, card_object: Card, ignore_assertion: bool = False) -> int | None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_object(
                validate_value = card_object
                )

        # Returning empty bottom stack position:
        if self.position_defence_list:
            return self.position_defence_list[0]
        
        # Returning None, if not available:
        else:
            return None
        
    
    def get_position_defence(self, card_object: Card, ignore_assertion: bool = False) -> int | None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_object(
                validate_value = card_object
                )
        
        # Searching for position:
        position_defence: int | None = None
        if self.position_defence_list:
            for card_location_index in self.position_defence_list:
                card_attacking: Card | None = self.cards_index[card_location_index]
                
                # Checking if card is attacking and can be defended against:
                if card_attacking is not None and card_object > card_attacking:
                    position_defence: int = card_location_index
                    break
        
        # Returning:
        return position_defence


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DISPLAY METHODS
    
    """
    
    
    def display(self) -> None:
        
        # Calling display() method on all card objects:
        for card_object in self.cards:
            card_object.display()
            
    