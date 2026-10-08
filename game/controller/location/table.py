# Card class object:
from game.controller.card import CardController as Card

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
from game.utilities.scripts import validate


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    TABLE CONTROLLER CLASS OBJECT CONSTRUCTOR
    
"""


class TableController:
    
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
        
    
    def clear_cached_attributes(self) -> None:
        """
        Clears all public cached properties of this table object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and all property lists available to
        clear all cached properties of this table object in a single loop through lists collection.
        """
            
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_cards_attributes,
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
        
        # Setting card's owner:
        card_object.set_owner(
            set_value = self.owner,
            update_previous = True,
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
        UPDATE METHODS
    
    """
    
    
    def update_texturepack_front(self, texturepack_object: texturepack.TexturePack, 
                                       ignore_assertion: bool = False, clear_cache: bool = True) -> None:
    
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_texturepack(
                validate_value = texturepack_object
                )

        # Updating texture pack for all cards:
        for card_object in self.cards:
            card_object.set_texturepack_front(
                set_value = texturepack_object,
                update_texture = True,
                ignore_assertion = True,
                clear_cache = True
                )
                
        # Clearing cache:
        if clear_cache:
            cached_property: str = "cards"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def update_texturepack_back(self, texturepack_object: texturepack.TexturePack, 
                                        ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_texturepack(
                validate_value = texturepack_object
                )

        # Updating texture pack for all cards:
        for card_object in self.cards:
            card_object.set_texturepack_back(
                set_value = texturepack_object,
                update_texture = True,
                ignore_assertion = True,
                clear_cache = True
                )

        # Clearing cache:   
        if clear_cache:
            cached_property: str = "cards"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        RENDER CACHED PROPERTIES
    
    """
    
    
    @cached_property
    def __render_rect_collection(self) -> tuple[arcade.Rect, ...]:
        
        # Preparing variables:
        rect_width: int = SETTINGS.CARD_TEXTURE_WIDTH
        rect_height: int = SETTINGS.CARD_TEXTURE_HEIGHT
        
        # Populating collection list:
        render_rect_collection: list[arcade.Rect] = []
        for location_index, rect_coordinates in coordinates.LOCATION_TABLE_COORDINATES_INDEX.items():
            rect_coordinate_x, rect_coordinate_y = rect_coordinates
            
            # Creating arcade.Rect objects and adding to temp list:
            rect_object = arcade.XYWH(
                x = rect_coordinate_x,
                y = rect_coordinate_y,
                width = rect_width,
                height = rect_height,
                )
            render_rect_collection.append(
                rect_object,
                )
            
        # Converting list to tuple:
        render_rect_collection_conv: tuple[arcade.Rect, ...] = tuple(render_rect_collection)
        
        # Returning:
        return render_rect_collection_conv


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DISPLAY METHODS
    
    """
    
    
    def display(self) -> None:
        
        # Calling display() method on all card objects:
        for card_object in self.cards:
            card_object.display()
            
    
    def display_debug(self) -> None:
        
        for rect_object in self.__render_rect_collection:
            arcade.draw_rect_outline(
                rect = rect_object,
                color = SETTINGS.RECT_TABLE_COLOR_POSITION,
                border_width = 2
                )            
    