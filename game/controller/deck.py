# Card class object:
from game.controller.card import Card

# Random library:
import random

# Arcade library:
import arcade
from arcade import Rect, Text, Texture, XYWH

# Texture packs:
from game.utilities.texturepack import TexturePack, TEXTURE_PACK_FRONT, TEXTURE_PACK_BACK

# Settings and session instances:
from game.settings import SETTINGS
from game.session import SESSION

# Cache management:
from functools import cached_property
from game.utilities.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list
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
from game.context import *


class Deck:
    
    
    def __init__(self) -> None:
        
        self.__cards: tuple[Card, ...] = None
    
    
    @cached_property
    def current(self) -> tuple[Card, ...]:

        # Returning:
        return self.__cards
    
    
    @cached_property
    def __sealed(self) -> tuple[Card, ...]:
        
        # Looping through card suits and names:
        for card_suit in CARD_SUIT_LIST:
            for card_name in CARD_NAME_LIST:
                
                # Creating card object:
                card_object: Card = Card.generate(
                    init_suit = card_suit,
                    init_name = card_name,
                    )
                
                # Updating texture packs (default)
                card_object.set_texture_pack_front(
                    texture_pack_object = TEXTURE_PACK_FRONT
                )
                
                # Updating location:
                card_object.set_location(
                    set_value = CARD_LOCATION.DECK,
                    ignore_assertion = True,
                    clear_cache = True
                    )
                
                
        
        
    