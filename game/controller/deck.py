# Card class object:
from game.controller.card import Card

# Random library:
import random

# Arcade library:
import arcade
from arcade import Rect, Text, Texture, XYWH

# Texture packs:
from game.utilities.texturepack import (
    TexturePack, 
    TEXTURE_PACK_FRONT, 
    TEXTURE_PACK_BACK
    )

# Settings and session instances:
from game.settings import SETTINGS
from game.session import SESSION

# Cache management:
from functools import cached_property
from game.utilities.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list,
    refresh_object,
    )

# Assertion scripts:
from game.utilities.scripts.assertion import (
    assert_setter_entry,
    assert_value_type,
    assert_value_default,
    assert_value_ge_zero,
    assert_value_not_empty,
    assert_value_in_range,
    )

# Context and other card variables:
from game.context import Location, Coordinates, RGB_Color
from game.context import (
    CARD_SUIT_LIST,
    CARD_NAME_LIST,
    CARD_LOCATION
    )


class Deck:
    
    
    def __init__(self) -> None:
        
        self.__card_list: list[Card] = []
        self.__card_gen_count: int = 0
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_cards_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "cards",
            "cards_count",
            "cards_value"
            )
        
        # Returning:
        return cached_property_list
    
    
    def clear_cached_cards_attributes(self) -> None:
    
        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_cards_attributes
            )
        
    
    def clear_cached_attributes(self) -> None:
            
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_cards_attributes,
            )
        
        # Looping throught the list and clearing cache:
        for cached_property_list in cached_property_list_collection:
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        VALIDATE METHODS
    
    """
    
    
    def __validate_card(self, validate_value: Card) -> None:
        
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = Card,
            raise_error = True,
            )
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARDS CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def cards(self) -> list[Card]:

        # Returning:
        return self.__card_list
    
    
    @cached_property
    def cards_count(self) -> int:
        
        # Counting:
        cards_count: int = len(self.cards)
        
        # Returing:
        return cards_count
    
    
    @cached_property
    def cards_value(self) -> int:
        
        # Calculating:
        cards_value: int = sum(card.value for card in self.cards)
        
        # Returning:
        return cards_value
    
    
    def add_card(self, card_object: Card, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_card(
                validate_value = card_object
                )
            
        # Checking if card is already added to the list:
        if card_object in self.cards:
            error_message: str = f"Card {card_object} appears to be in the deck card container!"
            raise IndexError(error_message)
            
        # Adding card to the list:
        self.__card_list.append(card_object)
        
        # Clearing cache:
        if clear_cache:
            self.clear_cached_cards_attributes()
        
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DECK GENERATOR CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def __sealed(self) -> tuple[Card, ...]:
        
        # Creating container:
        card_list: list[Card] = []
        
        # Looping through card suits and names:
        for card_suit in CARD_SUIT_LIST:
            for card_name in CARD_NAME_LIST:
                
                # Updating card generated list:
                self.__card_gen_count += 1          # TODO: Replace with method
                
                # Creating card object:
                card_location: Location = (CARD_LOCATION.DECK, len(card_list))
                card_object: Card = Card.generate(
                    init_id = self.__card_gen_count,
                    init_suit = card_suit,
                    init_name = card_name,
                    init_location = card_location
                    )
                
                # Updating location:
                card_object.set_location(
                    set_value = CARD_LOCATION.DECK,
                    ignore_assertion = True,
                    clear_cache = True
                    )
                
                # Updating coordinates:
                card_object.update_coordinates_location(
                    calculated_coordinates = None,
                    clear_cache = True,
                    )
                card_object.set_coordinates(
                    set_value = card_object.coordinates_position,
                    ignore_assertion = True,
                    clear_cache = True
                    )
                
                # Updating textures:
                card_object.set_texture_pack_front(
                    texture_pack_object = SESSION.TEXTURE_PACK_FRONT_SELECTED,
                    update_texture = True,
                    ignore_assertion = True,
                    clear_cache = True,
                    )
                card_object.set_texture_pack_back(
                    texture_pack_object = SESSION.TEXTURE_PACK_BACK_SELECTED,
                    update_texture = True,
                    ignore_assertion = True,
                    clear_cache = True,
                    )
                
                # Resetting states to False:
                card_object.reset_state_global(
                    clear_cache = True
                    )
                card_object.set_state_revealed(
                    set_value = False,
                    ignore_assertion = True,
                    clear_cache = True
                    )
                
                
                
    
    @property
    def __sealed_shuffled(self) -> tuple[Card, ...]:
        
        # Creating a copy
        deck_copy: tuple[Card, ...] = tuple(
            card_object for card_object
            in self.__sealed
            )
        
        # Shuffling
        random.shuffle(deck_copy)
        
        # Updating cards' positions:
        for card_object in deck_copy:
            location_index: int = deck_copy.index(card_object)
            card_object.set_location_index(
                set_value = location_index,
                ignore_assertion = True,
                clear_cache = True
                )

        # Returning:
        return deck_copy
    
        
    