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


class Hand:
    
    def __init__(self) -> None:
        
        # Owner attributes:
        self.__owner: str = None
        
        # Container attributes:
        self.__card_list: list = []
    
    
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
    
    
    def add_card(self, card_object: Card, sort_container: bool = True, update_card: bool = True,
                       ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_object(
                validate_value = card_object
                )
            
        # Checking if card is already added to the list:
        if card_object in self.cards:
            error_message: str = f"Card {card_object} appears to be in the hand card container!"
            raise IndexError(error_message)
            
        # Adding card to the list:
        self.__card_list.append(card_object)
        
        # Updating card's attributes:
        if update_card:
            
            # Updating location and location index attributes:
            location_index: int = self.__card_list.index(card_object)
            set_location: context.Location = (
                context.CARD_LOCATION.DECK, 
                location_index,
                )
            card_object.set_location(
                set_value = set_location,
                ignore_assertion = True,
                clear_cache = True
                )
            
            # Updating added index:
            added_index: int = self.cards_count + 1
            card_object.set_added_index(
                set_value = added_index,
                ignore_assertion = True,
                clear_cache = True
                )
            
            # Updating tilt:
            if self.__owner == context.PLAYER_TYPE.COMPUTER:
                card_object.set_render_tilt(
                    set_value = card_object.render_tilt_opp,
                    ignore_assertion = True,
                    clear_cache = True,
                    )
            
            # Updating states:
            card_object.reset_state_global(
                clear_cache = False,
                )
            card_object.set_state_visible(
                set_value = True,
                ignore_assertion = True,
                clear_cache = False,
                )
            if self.__owner == context.PLAYER_TYPE.HUMAN:
                card_object.set_state_revealed(
                    set_value = True,
                    ignore_assertion = True,
                    clear_cache = False,
                    )
            card_object.clear_cached_state_attributes()
            
            # Updating coordinates based on precalculated position:
            card_object.update_coordinates_location(
                calculated_coordinates = None,
                clear_cache = True,
                )
        
        # Sorting cards, if required
        if sort_container:
            self.sort_default(
                clear_cache = clear_cache,
                )
        
        # Clearing cache:
        if clear_cache:
            self.clear_cached_cards_attributes()
            
            
    def remove_card(self, card_object: Card, sort_container: bool = True, 
                          ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_object(
                validate_value = card_object
                )
            
        # Checking if card is in the list:
        if card_object not in self.cards:
            error_message: str = f"Card {card_object} appears to be not in the hand card container!"
            raise IndexError(error_message)

        # Removing card from the list:
        self.__card_list.remove(card_object)
        
        # Sorting cards, if required:
        if sort_container:
            self.sort_default(
                clear_cache = clear_cache,
                )

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
            
    
    def update_coordinates(self, clear_cache: bool = True) -> None:
        ...
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SORT METHODS
    
    """
    
    
    def __sort_added(self, sort_reverse: bool = False, clear_cache: bool = True) -> None:
        
        # Sorting cards:
        self.__card_list.sort(
            key = lambda card: card.added_index,
            reverse = sort_reverse,
            )
        
        # Clearing cache, if required:
        if clear_cache:
            self.clear_cached_cards_attributes()
        
        
    def __sort_value(self, sort_reverse: bool = False, clear_cache: bool = True) -> None:
        
        # Sorting cards:
        self.__card_list.sort(
            key = lambda card: card.value,
            reverse = sort_reverse,
            )
        
        # Clearing cache, if required:
        if clear_cache:
            self.clear_cached_cards_attributes()
        
        
    def __sort_suit(self, sort_reverse: bool = False, clear_cache: bool = True) -> None:
        
        # Creating a suit order dictionary index:
        suit_order: dict[str, int] = {
            suit: index
            for index, suit in enumerate(context.CARD_SUIT_LIST)
            }

        # Sorting cards:
        self.__card_list.sort(
            key = lambda card: (
                suit_order[card.suit],
                - card.value,
                ),
            reverse = sort_reverse,
            )   
        
        # Clearing cache, if required:
        if clear_cache:
            self.clear_cached_cards_attributes()
    
        
    def __sort_color(self, sort_reverse: bool = False, clear_cache: bool = True) -> None:
        
        # Creating a suit order dictionary index:
        color_order: dict[str, int] = {
            color: index
            for index, color in enumerate(context.CARD_SUIT_COLOR_LIST)
            }

        # Sorting cards:
        self.__card_list.sort(
            key = lambda card: (
                color_order[card.color],
                - card.value,
                ),
            reverse = sort_reverse,
            )
        
        # Clearing cache, if required:
        if clear_cache:
            self.clear_cached_cards_attributes()
        
        
    def __sort_default(self, sort_reverse: bool = False, clear_cache: bool = True) -> None:
        ...
        
    
    def sort(self, sort_seq: str, sort_reverse: bool = False, update_coordinates: bool = True,
                   ignore_assertion: bool = True, clear_cache: bool = True) -> None:
        
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_sort_sequence(
                validate_value = sort_seq
                )
            validate.validate_flag(
                validate_value = sort_reverse
                )
            
        # Creating sort sequence switch dictionary:
        sort_seq: dict[str, function] = {
            context.HAND_SORT_SEQ.ADDED: lambda: self.__sort_added(sort_reverse, clear_cache),
            context.HAND_SORT_SEQ.VALUE: lambda: self.__sort_value(sort_reverse, clear_cache),
            context.HAND_SORT_SEQ.SUIT: lambda: self.__sort_suit(sort_reverse, clear_cache),
            context.HAND_SORT_SEQ.COLOR: lambda: self.__sort_color(sort_reverse, clear_cache),
            }
        
        # Getting correct sorting sequence:
        sort_seq_func: function = sort_seq.get(
            sort_seq, 
            lambda: self.__sort_default(sort_reverse)
            )
        
        # Calling sorting sequence:
        sort_seq_func()
        
        # Updating coordinates, if required:
        if update_coordinates:
            self.update_coordinates(
                clear_cache = clear_cache
                )

        # Clearing cache:
        if clear_cache:
            self.clear_cached_cards_attributes()
                
        
    def sort_default(self, sort_reverse: bool = False, update_coordinates: bool = True, clear_cache: bool = True) -> None:
        
        # Calling default sorting sequence:
        self.sort(
            sort_seq = SESSION.HAND_SORT_SEQ_DEFAULT,
            sort_reverse = SESSION.HAND_SORT_SEQ_REVERSE,
            update_coordinates = update_coordinates,
            ignore_assertion = True,
            clear_cache = clear_cache
            )
        
    
    def sort_selected(self, sort_reverse: bool = False, update_coordinates: bool = True, clear_cache: bool = True) -> None:

        # Calling default sorting sequence:
        self.sort(
            sort_seq = SESSION.HAND_SORT_SEQ_SELECTED,
            sort_reverse = SESSION.HAND_SORT_SEQ_REVERSE,
            update_coordinates = update_coordinates,
            ignore_assertion = True,
            clear_cache = clear_cache
            )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DISPLAY METHODS
    
    """
    
    
    def display(self) -> None:
        ...
    
    