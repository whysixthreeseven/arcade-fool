# Annotation import:
from __future__ import annotations

# Cache-related modules and scripts import:
from game.scripts import clear_cached_property
from functools import cached_property
from itertools import product

# Random library import:
import random

# Settings and variables import list:
from game.collections import CARD_INFO
from game.settings import *

# Developer session values:
from game.controllers.session import (
    DEV_ENABLE_ASSERTION,
    DEV_ENABLE_ECHO,
    )

# Collections import:
from game.controllers.card import CardObject


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DECK CONTROLLER BLOCK

"""


class DeckController:
    """
    Deck controller that manages deck container by creating and shuffling a deck, retrieving (and 
    removing) cards from the deck, and keeping track of cards remaining.
    """

    def __init__(self):
        
        # Core attributes:
        self.__deck_container: list[CardObject] = []
        self.__deck_trump_suit: str = CARD_INFO.SUIT_NOT_SET

    
    def __repr__(self):
        """
        Overwrites native __repr__ magic method.

        Constructs a string in format Deck (# card(s), % trump) -> "Deck (21 cards,♡ trump)".

        Used to print deck object to console when debugging or (not implemented yet) when rendering
        hints during hover events.

        :return str: Formatted string repr value in a readable format, e.g. Deck (# card(s), % trump) 
            -> "Deck (21 cards,♡ trump)".

        """
        
        # Generating a repr string:
        repr_string: str = "Deck ({card_count}, {card_suit_trump})".format(
            card_count = "{count} {card_f}".format(
                count = self.deck_count,
                card_f = "cards" if self.deck_count > 1 else "card"
                ),
            card_suit_trump = "{suit_unicode} trump".format(
                suit_unicode = CardObject.CARD_SUIT_UNICODE_INDEX[self.deck_trump_suit],
                )
            )
        
        # Returning:
        return repr_string
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE PROPERTIES BLOCK
    
    TODO: Create a docstring.

    """


    @cached_property
    def __cached_deck_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g.: for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "deck_container",
            "deck_count",
            "deck_trump_suit"
            )
        
        # Returning:
        return cached_property_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    DECK METHODS AND PROPERTIES BLOCK
    
    TODO: Create a docstring.

    """


    @cached_property
    def deck_container(self) -> list[CardObject]:
        """
        List container with all the card object items stored in it.

        Used to check Card count available and quickly access top card in the deck via cached copy
        of the attribute.

        Cached.

        :return list[Card]: List container with all the card object items stored in it.
        """

        # Returning:
        return self.__deck_container

    
    @cached_property
    def deck_sealed(self) -> list[CardObject]:
        """
        A list container with all 36 Card class type objects generated, set up and ready to use.
        This cached property is generated once and can be used multiple times without costing much
        of operation time due to its cached nature. 

        Used to create a new deck container. All card objects' positions are indexed as they are
        created. This list is not shuffled, thus a shuffle_deck() 
        method should be called after.

        Cached. Cannot be cleared.

        :return list[Card]: A deck list container with 36 card class type objects generated, set up
            and ready to use. Not shuffled.
        """


        def create_card_object(init_suit: CARD_INFO, 
                               init_type: CARD_INFO, 
                               position_index: int
                               ) -> CardObject:
            """
            Generates a card object via Card class's staticmethod and sets a new position in deck.
            This function is used to quickly populate (generate) a list of Cards via generator and 
            itertools' product function within this cached_property.

            :param str init_suit: Suit string value, must be a default value, e.g.: 
                "CARD_SUIT_HEARTS", or "CARD_SUIT_CLUBS"
            :param str init_type: Suit string value, must be a default value, e.g.: 
                "CARD_TYPE_SIX", or "CARD_TYPE_QUEEN".
            :param int position_index: Card object's position within the deck container, where 
                position index 0 is the last (bottom) card, and position index 35 is the first 
                (top) card.

            :raise AssertionError: (If enabled) May raise AssertionError if card's setter methods
                fail to assert validity of parameters. For more check Card class's set_card_suit(),
                set_card_type(), and set_position_deck() methods.

            :return Card: Card class-type object.
            """

            # Creating card:
            card_object: CardObject = CardObject.create_card_object(
                init_suit = init_suit,
                init_type = init_type,
                )
            
            # Updating position in deck and location:
            card_object.set_position_deck(
                position_index = position_index,
                update_related = False
                )
            
            # Returning:
            return card_object


        # Creating a deck container:
        deck_sealed: list[CardObject] = list(
            create_card_object(init_suit, init_type, position_index) 
            for position_index, (init_suit, init_type) in enumerate(
                product(CardObject.CARD_SUIT_LIST, CardObject.CARD_TYPE_LIST)
                )
            )

        # Returning:
        return deck_sealed
    

    @cached_property
    def deck_count(self) -> int:
        """
        Number of card objects remaining in deck container in integer format. 
        
        Cached.

        :return int: Integer value of number of card objects remaining in deck container.
        """

        # Counting cards remaining in deck:
        deck_count: int = len(self.deck_container)

        # Returning:
        return deck_count
    

    @cached_property
    def deck_trump_suit(self) -> str:
        """
        Suit string representing deck's chosen trump suit in its default state as in variables.py, 
        e.g. "CARD_SUIT_HEARTS". Used to check if card object's trump state is accurate based on 
        its suit value, and to set card object's state trump when setting or changing deck's trump
        suit. 
        
        Cached.

        :return str: Suit value as is in variables.py script, e.g. "CARD_SUIT_HEARTS"
        """

        # Returning:
        return self.__deck_trump_suit


    def create_deck(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Getting a new deck and shuffling:
        self.__deck_container: list[CardObject] = self.deck_sealed

        # Selecting a new trump suit:
        trump_suit: str = random.choice(CardObject.CARD_SUIT_LIST)
        print(trump_suit) # DEBUG
        self.set_deck_trump(
            set_value = trump_suit,
            clear_cache = False
            )
        
        # Updating trump cards:
        for card_object in self.__deck_container:
            if card_object.suit == trump_suit:
                card_object.set_state_trump(
                    set_value = True
                    )

        # Clearing cache:
        for cached_property in self.__cached_deck_property_list:
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )


    def shuffle_deck(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Shuffling:
        if self.deck_count > 1:
            random.shuffle(self.__deck_container)

            # Clearing cache:
            for cached_property in self.__cached_deck_property_list:
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )

            # Updating card's positions:
            for position_index, card_object in enumerate(reversed(self.deck_container)):
                card_object.set_position_deck(
                    position_index = position_index,
                    update_related = False
                    )
                
    
    def clear_deck(self) -> None:
        """
        TODO: Createa a docstring.
        """

        # Resetting deck container list:
        self.__deck_container: list[CardObject] = []

        # Clearing cache:
        for cached_property in self.__cached_deck_property_list:
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_deck_trump(self, set_value: CARD_INFO, clear_cache: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        ...

        # Updating attribute:
        if self.__deck_trump_suit != set_value:
            self.__deck_trump_suit: str = set_value

            # Updating card objects:
            if self.deck_count > 0:
                for card_object in self.__deck_container:
                    if card_object.suit == set_value:
                        card_object.set_state_trump(
                            set_value = True
                            )
            
            # Clearing cache:
            if clear_cache:
                for cached_property in self.__cached_deck_property_list:
                    clear_cached_property(
                        target_object = self,
                        target_attribute = cached_property,
                        )
                
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    DRAW/REMOVE CARD METHODS BLOCK
    
    TODO: Create a docstring.

    """


    def draw_card(self) -> CardObject:
        """
        TODO: Create a docstring.
        
        :return CardObject: ...
        """

        # Checking if there are any cards left to draw:
        if self.deck_count >= 1:

            # Getting card object and removing it from the deck:
            card_object: CardObject = self.deck_container[0]
            self.__remove_card(
                card_object = card_object,
                clear_cache = False
                )
            
            # Updating card object:
            card_object.reset_position()        # <- Resets all positions to None
            
            # Clearing cache:
            for cached_property in self.__cached_deck_property_list:
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )
            
            # Returning:
            return card_object


    def __remove_card(self, card_object: CardObject, clear_cache: bool = False) -> None:
        """
        TODO: Create a docstring.
        """

        # Removing card object from deck if it exists:
        if card_object in self.deck_container:
            self.__deck_container.remove(
                card_object
                )
        
        # Clearing cache:
        if clear_cache:
            for cached_property in self.__cached_deck_property_list:
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )

