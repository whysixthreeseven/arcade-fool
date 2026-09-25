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


class Discard:
    
    def __init__(self) -> None:
        
        # Core attributes:
        self.__card_list: list[Card] = []       # Current deck container
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_cards_attributes(self) -> tuple[str, ...]:
        """
        Cards attributes-related cached properties list.
        
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
            "cards",
            "cards_count",
            "cards_value"
            )
        
        # Returning:
        return cached_property_list
    
    
    def clear_cached_cards_attributes(self) -> None:
        """
        Clears all public cached core properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear texturepack properties of this card object.
        """
    
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_cards_attributes
            )
        
    
    def clear_cached_attributes(self) -> None:
        """
        Clears all public cached properties of this card object.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and all property lists available to
        clear all cached properties of this card object in a single loop through lists collection.
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
        CARDS CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def cards(self) -> tuple[Card, ...]:
        
        # Converting list to tuple:
        card_list: tuple[Card, ...] = tuple(
            card_object for card_object 
            in self.__card_list
            )

        # Returning:
        return card_list
    
    
    @cached_property
    def cards_count(self) -> int:
        
        # Counting:
        cards_count: int = len(self.cards)
        
        # Returing:
        return cards_count
    
    
    @cached_property
    def cards_value(self) -> int:
        
        # Calculating:
        cards_value: int = sum(
            card.value for card 
            in self.cards
            )
        
        # Returning:
        return cards_value
    
    
    def add_card(self, card_object: Card, update_location_index: bool = True, update_card: bool = True,
                       ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_object(
                validate_value = card_object
                )
            
        # Checking if card is already added to the list:
        if card_object in self.cards:
            error_message: str = f"Card {card_object} appears to be in the deck card container!"
            raise IndexError(error_message)
            
        # Adding card to the list:
        self.__card_list.append(card_object)
        
        # Updating card's attributes:
        if update_card:
            
            # Updating location and location index attributes:
            location_index: int = self.__card_list.index(card_object)
            set_location: context.Location = (
                context.CARD_LOCATION.DISCARD, 
                location_index,
                )
            card_object.set_location(
                set_value = set_location,
                ignore_assertion = True,
                clear_cache = True
                )
            
            # Updating card tilt:
            card_object.set_render_tilt_random(
                clear_cache = True,
                )
            
            # Updating card states:
            card_object.reset_state_global(
                clear_cache = True
                )
            card_object.set_state_visible(
                set_value = True,
                ignore_assertion = True,
                clear_cache = True,
                )
            card_object.set_state_revealed(
                set_value = True,
                ignore_assertion = True,
                clear_cache = True,
                )
            
            # Updating coordinates based on precalculated position:
            card_object.update_coordinates_location(
                calculated_coordinates = None,
                clear_cache = True,
                )
        
        # Updating index:
        if update_location_index:
            self.update_location_index()
        
        # Clearing cache:
        if clear_cache:
            self.clear_cached_cards_attributes()
            
            
    def remove_card(self, card_object: Card, update_location_index: bool = True, 
                          ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_object(
                validate_value = card_object
                )
            
        # Checking if card is in the list:
        if card_object not in self.cards:
            error_message: str = f"Card {card_object} appears to be not in the deck card container!"
            raise IndexError(error_message)

        # Removing card from the list:
        self.__card_list.remove(card_object)
        
        # Updating index:
        if update_location_index:
            self.update_location_index()

        # Clearing cache:
        if clear_cache:
            self.clear_cached_cards_attributes()
            
            
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
        if self.cards_count > 0:
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
        if self.cards_count > 0:
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
            
            
    def update_location_index(self, clear_cache: bool = True) -> None:
        
        # Updating location index for all cards:
        card_count: int = len(self.__card_list)
        if card_count > 0:
            for card_object in self.__card_list:
                location_index: int = self.__card_list.index(card_object)
                card_object.set_location_index(
                    set_value = location_index,
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
        DISPLAY INFO CACHED PROPERTIES AND METHODS
    
    """
    
    
    def display_info(self, display_coordinates: context.Coordinates, ignore_assertion: bool = False) -> None:
        """
        THIS METHOD HAS NOT BEEN PROPERLY IMPLEMENTED AND IS FOR TEST USES ONLY!        
        """
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            ...     # TODO: Implement
            
        # Unpacking coordinates:
        coordinate_x, coordinate_y = display_coordinates
        
        # Creating text object:
        render_text: arcade.Text = arcade.Text(
            text = "{num} {literal}".format(
                num = self.cards_count,
                literal = "cards" if self.cards_count > 1 or self.cards_count == 0 else "card"
                ),
            x = coordinate_x,
            y = coordinate_y,
            color = arcade.color.WHITE,
            font_size = 24,
            anchor_x = "center",
            anchor_y = "center"
            )
        
        # Displaying text:
        render_text.draw()
    
    