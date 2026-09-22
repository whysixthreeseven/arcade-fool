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
    TEXTURE_PACK_FRONT_INDEX,
    TEXTURE_PACK_BACK,
    TEXTURE_PACK_BACK_INDEX,
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
    CARD_NAME,
    CARD_NAME_LIST,
    CARD_LOCATION
    )


class Deck:
    
    
    def __init__(self) -> None:
        
        # Core attributes:
        self.__card_list: tuple[Card, ...] = ()
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
        
        
    def __validate_texture_pack(self, validate_value: TexturePack) -> None:
                
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = TexturePack,
            raise_error = True
            )
        
        # Selecting default value list:
        texture_pack = validate_value
        if texture_pack.type == "Front":
            texture_pack_list: tuple[TexturePack, ...] = TEXTURE_PACK_FRONT_INDEX
        elif texture_pack.type == "Back":
            texture_pack_list: tuple[TexturePack, ...] = TEXTURE_PACK_BACK_INDEX
        else:
            error_message: str = f"Invalid texture pack type: {texture_pack.type}."
            raise AssertionError(error_message)

        # Asserting value is default:
        assert_value_default(
            check_value = texture_pack,
            check_list = texture_pack_list,
            raise_error = True
            )
        
        
    def __validate_deck_size(self, validate_value: int) -> None:

        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = int,
            raise_error = True
            )

        # Asserting value is default:
        default_list: tuple[int, int] = (
            SETTINGS.DECK_SIZE_MIN,
            SETTINGS.DECK_SIZE_MAX
            )
        assert_value_default(
            check_value = validate_value,
            check_list = default_list,
            raise_error = True
            )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        MAIN METHODS
    
    """
    
    
    def generate(self, trump_suit: str | None, deck_size: int | None) -> None:
        
        # Generating new deck:        
        deck = self.__generate(
            trump_suit = trump_suit,
            deck_size = deck_size
            )
        
        # Updating attributes:
        self.__card_list: list[Card] = deck
        
        # Clearing cache:
        self.clear_cached_cards_attributes()
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARDS CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def cards(self) -> tuple[Card, ...]:
        
        # Converting list to tuple:
        card_list: tuple[Card, ...] = tuple(card_object for card_object in self.__card_list)

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
        cards_value: int = sum(card.value for card in self.cards)
        
        # Returning:
        return cards_value
    
    
    def add_card(self, card_object: Card, update_location_index: bool = True, update_card: bool = True,
                       ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
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
        
        # Updating card's attributes:
        if update_card:
            
            # Updating location and location index attributes:
            set_location: Location = (CARD_LOCATION.DECK, self.__card_list.index(card_object))
            card_object.set_location(
                set_value = set_location,
                ignore_assertion = True,
                clear_cache = True
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
            self.__validate_card(
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
            
            
    def draw_card(self, clear_cache: bool = True) -> Card | None:
        
        # Returning None, if no more cards available:
        if self.cards_count == 0:
            return None
        
        # Popping a card from the list:
        else:
            card: Card = self.cards[-1]
            self.remove_card(
                card_object = card,
                clear_cache = False,
                )
            
            # Updating secret card, if it exists:
            card_count: int = len(self.__card_list)
            if card_count == 1 and SESSION.GAME_MODE_SECRET:
                card_secret = self.__card_list[0]
                card_secret.set_trump(
                    set_value = True,
                    ignore_assertion = True,
                    clear_cache = True
                    )
                card_secret.set_state_revealed(
                    set_value = True,
                    ignore_assertion = True,
                    clear_cache = True
                    )
            
            # Clearing cache:
            if clear_cache:
                self.clear_cached_cards_attributes()
            
            # Returning card object:
            return card
        
        
        
        
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        UPDATE METHODS
    
    """
    
    
    def update_texture_pack_front(self, texture_pack_object: TexturePack, 
                                        ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_texture_pack(
                validate_value = texture_pack_object
                )

        # Updating texture pack for all cards:
        if self.cards_count > 0:
            for card_object in self.cards:
                card_object.set_texture_pack_front(
                    set_value = texture_pack_object,
                    update_texture = True,
                    ignore_assertion = True,
                    clear_cache = True
                    )
                
        # Clearing cache:
        if clear_cache:
            cached_property: str = "cards"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def update_texture_pack_back(self, texture_pack_object: TexturePack, 
                                       ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_texture_pack(
                validate_value = texture_pack_object
                )

        # Updating texture pack for all cards:
        if self.cards_count > 0:
            for card_object in self.cards:
                card_object.set_texture_pack_back(
                    set_value = texture_pack_object,
                    update_texture = True,
                    ignore_assertion = True,
                    clear_cache = True
                    )

        # Clearing cache:   
        if clear_cache:
            cached_property: str = "cards"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
            
    def update_location_index(self, clear_cache: bool = True) -> None:
        
        # Updating location index for all cards:
        if self.cards_count > 0:
            for card_object in self.cards:
                location_index: int = self.cards.index(card_object)
                card_object.set_location_index(
                    set_value = location_index,
                    ignore_assertion = True,
                    clear_cache = True
                    )
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "cards"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DECK GENERATOR CACHED PROPERTIES AND METHODS
    
    """
    
    
    def __generate(self, deck_size: int, trump_suit: str | None) -> list[Card]:

        # Collecting restricted cards:
        restricted_card_list: tuple[str, ...] = ()
        if deck_size == SETTINGS.DECK_SIZE_MIN:        
            restricted_card_list: tuple[str, ...] = (
                CARD_NAME.TWO,
                CARD_NAME.THREE,
                CARD_NAME.FOUR,
                CARD_NAME.FIVE,
                )
        
        # Creating container:
        card_list_gen: list[Card] = []
        card_list_adjusted: list[Card] = []
        
        # Selecting trump suit:
        if trump_suit is None:
            trump_suit = random.choice(CARD_SUIT_LIST)
        
        # Looping through card suits and names:
        for card_suit in CARD_SUIT_LIST:
            for card_name in CARD_NAME_LIST:
                
                # Checking if card name is in restricted list:
                if card_name not in restricted_card_list:
                
                    # Updating card generated list:
                    self.__card_gen_count += 1          # TODO: Replace with method
                    
                    # Creating card object:
                    card_location: Location = (CARD_LOCATION.DECK, len(card_list_gen))
                    card_object: Card = Card.generate(
                        init_id = self.__card_gen_count,
                        init_suit = card_suit,
                        init_name = card_name,
                        init_location = card_location
                        )
                    
                    # Setting trump flag, if applicable:
                    if card_suit == trump_suit:
                        card_object.set_trump(
                            set_value = True,
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
                    card_object.set_state_revealed(
                        set_value = False,
                        ignore_assertion = True,
                        clear_cache = True
                        )
                    card_object.set_state_visible(
                        set_value = True,
                        ignore_assertion = True,
                        clear_cache = True,
                        )
                    
                    # Adding to the list:
                    card_list_gen.append(
                        card_object
                        )

        # Shuffling:
        self.__shuffle(
            deck_object = card_list_gen
            )
        
        # Collecting all trump cards and choosing a random one:
        trump_card_list: tuple[Card, ...] = tuple(
            card_object for card_object in card_list_gen
            if card_object.trump
            )
        trump_card: Card = random.choice(trump_card_list)
        
            
        # Selecting a secret card:
        secret_card: Card = random.choice(card_list_gen)
        while secret_card == trump_card:
            secret_card: Card = random.choice(card_list_gen)
            
        # Removing secret card from list:
        if SESSION.GAME_MODE_SECRET:
            card_list_gen.remove(secret_card)
            card_list_adjusted.append(
                secret_card
                )
            secret_card.set_render_tilt(
                set_value = secret_card.render_tilt_deck_bottom,
                ignore_assertion = True,
                clear_cache = True,
                )
            
        # Adding trump card to the list and updating it:
        card_list_gen.remove(
            trump_card
            )
        card_list_adjusted.append(
            trump_card
            )
        trump_card.set_render_tilt(
            set_value = trump_card.render_tilt_deck_bottom,
            ignore_assertion = True,
            clear_cache = True
            )
        trump_card.set_state_revealed(
            set_value = True,
            ignore_assertion = True,
            clear_cache = True
            )
        
        # Adding the rest of the cards:
        for card_remaining in card_list_gen:
            card_list_adjusted.append(
                card_remaining
                )
            
        # Updating all cards' location index and coordinates:
        for card_object in card_list_adjusted:
            location_index: int = card_list_adjusted.index(card_object)
            card_object.set_location_index(
                set_value = location_index,
                ignore_assertion = True,
                clear_cache = True
                )
            card_object.update_coordinates_location(
                calculated_coordinates = None,
                clear_cache = True
                )
            card_object.set_coordinates(
                set_value = card_object.coordinates_position,
                ignore_assertion = True,
                clear_cache = True,
                )
            
        # Sorting by index:
        card_list_sorted: list[Card] = self.__sort(
            deck_object = card_list_adjusted
            )

        # Returning:
        return card_list_sorted
    
    
    def __shuffle(self, deck_object: tuple[Card, ...]) -> tuple[Card, ...]:
            
        # Creating a copy
        deck_copy: tuple[Card, ...] = deck_object
        
        # Shuffling
        random.shuffle(deck_copy)
        
        # Returning:
        return deck_copy
    
    
    def __sort(self, deck_object: tuple[Card, ...] | list[Card]) -> list[Card]:
        
        # Returning:
        deck_sorted: list[Card] = list(
            sorted(
                deck_object,
                key = lambda card_object: card_object.location_index
                )
            )
        
        # Returning:
        return deck_sorted
    
    