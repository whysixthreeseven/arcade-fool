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
from game.utilities import texturepack
from game.utilities.scripts import validate


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    DECK CONTROLLER CLASS OBJECT CONSTRUCTOR
    
"""


class DeckController:
    
    def __init__(self) -> None:
        
        # Core attributes:
        self.__cards_list: list[Card] = []       # Current deck container
        self.__cards_gen_count: int = 0          # Cards generated count (global)
        
        # Trump suit selector:
        self.__trump_suit: str = None
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_cards_attributes(self) -> tuple[str, ...]:
        """
        Cards attributes-related cached properties list.
        
        Collects and returns all properties of this deck controller decorated with `functools` library's `cached_property` wrapper.
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
    
    
    @cached_property
    def __cached_hints_attributes(self) -> tuple[str, ...]:
        """
        Hints attributes-related cached properties list.
        
        Collects and returns all properties of this deck controller decorated with `functools` library's `cached_property` wrapper.
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
            "hint_text_cards_count",
            "hint_text_trump_suit",
            )
        
        # Returning:
        return cached_property_list
    
    
    def clear_cached_cards_attributes(self) -> None:
        """
        Clears all public cached core properties of this deck controller.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear texturepack properties of this deck controller.
        """
    
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_cards_attributes
            )
        
    
    def clear_cached_hints_attributes(self) -> None:
        """
        Clears all public cached core properties of this deck controller.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and related property list available to
        clear texturepack properties of this deck controller.
        """

        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_hints_attributes
            )
        
    
    def clear_cached_attributes(self) -> None:
        """
        Clears all public cached properties of this deck controller.
        
        Uses `utilities.scripts.cache` module's `clear_cached_property_list` function and all property lists available to
        clear all cached properties of this deck controller in a single loop through lists collection.
        """
            
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_cards_attributes,
            self.__cached_hints_attributes,
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
    
    
    def setup(self, trump_suit: str | None = None) -> None:
        
        # Generating new deck:        
        deck = self.__generate(
            trump_suit = trump_suit,
            deck_size = SESSION.DECK_SIZE_SELECTED,
            )
        
        # Updating attributes:
        self.__cards_list: list[Card] = deck
        
        # Clearing cache:
        self.clear_cached_attributes()
        
        
    def reset(self) -> None:
        
        # Calling setup method:
        self.setup(
            trump_suit = None,
            )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARDS CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def cards(self) -> tuple[Card, ...]:
        
        # Converting list to tuple:
        card_list: tuple[Card, ...] = tuple(
            card_object for card_object 
            in self.__cards_list
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
    
    
    def draw_card(self, clear_cache: bool = True) -> Card | None:
        
        # Returning None, if no more cards available:
        if self.cards_count == 0:
            return None
        
        # Popping a card from the list:
        else:
            
            # Acquiring card from top and removing it from the deck:
            card: Card = self.cards[-1]
            self.__cards_list.remove(card)
            
            # Updating secret card, if it exists:
            card_count: int = len(self.__cards_list)
            if card_count == 1 and SESSION.GAME_MODE_SECRET:
                card_secret = self.__cards_list[0]
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
                card_secret.set_state_known(
                    set_value = True,
                    ignore_assertion = True,
                    clear_cache = True
                    )
                
                # Updating trump suit selector:
                trump_suit: str = card_secret.suit
                self.set_trump_suit(
                    set_value = card_secret.suit,
                    ignore_assertion = False,
                    clear_cache = True,
                    )

            # Clearing cache:
            if clear_cache:
                self.clear_cached_attributes()
            
            # Returning card object:
            return card
        
    
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
        for card_object in self.__cards_list:
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
        for card_object in self.__cards_list:
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
        card_count: int = len(self.__cards_list)
        if card_count > 0:
            for card_object in self.__cards_list:
                location_index: int = self.__cards_list.index(card_object)
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
        DECK GENERATOR CACHED PROPERTIES AND METHODS
    
    """
    
    
    def __generate(self, deck_size: int, trump_suit: str | None) -> list[Card]:

        # Collecting restricted cards:
        restricted_card_list: tuple[str, ...] = ()
        if deck_size == SETTINGS.DECK_SIZE_MIN:
            restricted_card_list: tuple[str, ...] = (
                context.CARD_NAME.TWO,
                context.CARD_NAME.THREE,
                context.CARD_NAME.FOUR,
                context.CARD_NAME.FIVE,
                )
        
        # Creating container:
        card_list_gen: list[Card] = []
        card_list_adjusted: list[Card] = []
        
        # Selecting trump suit:
        if trump_suit is None:
            trump_suit = random.choice(context.CARD_SUIT_LIST)
        
        # Looping through card suits and names:
        for card_suit in context.CARD_SUIT_LIST:
            for card_name in context.CARD_NAME_LIST:
                
                # Checking if card name is in restricted list:
                if card_name not in restricted_card_list:
                
                    # Updating card generated list:
                    self.__cards_gen_count += 1          # TODO: Replace with method
                    
                    # Creating card object:
                    card_location_index: int = len(card_list_gen)
                    card_location: context.Location = (
                        context.CARD_LOCATION.DECK, 
                        card_location_index,
                        )
                    card_object: Card = Card.generate(
                        init_id = self.__cards_gen_count,
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
                    card_object.set_texturepack_front(
                        texturepack_object = SESSION.TEXTUREPACK_FRONT_SELECTED,
                        update_texture = True,
                        ignore_assertion = True,
                        clear_cache = True,
                        )
                    card_object.set_texturepack_back(
                        texturepack_object = SESSION.TEXTUREPACK_BACK_SELECTED,
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
        trump_suit: str = trump_card.suit
        self.set_trump_suit(
            set_value = trump_card.suit,
            ignore_assertion = False,
            clear_cache = True,
            )
        
        # Selecting a secret card:
        secret_card: Card = random.choice(card_list_gen)
        secret_card.set_state_secret(
            set_value = True,
            ignore_assertion = True,
            clear_cache = True,
            )
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
            location: context.Location = (
                context.CARD_LOCATION.DECK, 
                card_list_adjusted.index(card_object)
                )
            card_object.set_location(
                set_value = location,
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
            card_object.set_coordinates_expected(
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
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        TRUMP SUIT SELECTOR CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def trump_suit(self) -> str:
        
        # Returning:
        return self.__trump_suit
    
    
    @cached_property
    def trump_suit_ascii(self) -> str:
        
        # Generating a dictionary index:
        suit_ascii_index = {
            attr_name.capitalize(): getattr(context.CARD_SUIT_ASCII, attr_name)
            for attr_name, attr_value in context.CARD_SUIT.__dict__.items()
            if not attr_name.startswith("_") and hasattr(context.CARD_SUIT_ASCII, attr_name)
            }
        
        # Getting correct value:
        suit_ascii: str = suit_ascii_index.get(
            self.trump_suit,
            None
            )
        
        # Returning:
        return suit_ascii
    
    
    def set_trump_suit(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
            
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_suit(
                validate_value = set_value
                )

        # Updating attribute:
        self.__trump_suit = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "trump_suit",
                "trump_suit_ascii",
                "hint_text_trump_suit"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )

    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        UPDATE METHODS
    
    """
    
    
    def update_texturepack_front(self, texturepack_object: texturepack.TexturePack, 
                                       ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_texturepack(
                validate_value = texturepack_object,
                )
        
        # Updating cards in container:
        for card_object in self.cards:
            card_object.set_texturepack_front(
                texturepack_object = texturepack_object,
                update_texture = True,
                ignore_assertion = True,
                clear_cache = clear_cache,
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
                validate_value = texturepack_object,
                )
        
        # Updating cards in container:
        for card_object in self.cards:
            card_object.set_texturepack_back(
                texturepack_object = texturepack_object,
                update_texture = True,
                ignore_assertion = True,
                clear_cache = clear_cache,
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
    
    
    @cached_property
    def __hint_text_cards_count_index(self) -> dict[int, arcade.Text]:
        
        # Generating cards count index:
        hint_text_cards_count_index: dict[int, arcade.Text] = {
            cards_count: arcade.Text(
            text = "{num} {literal}".format(
                num = cards_count,
                literal = "cards" if cards_count > 1 or cards_count == 0 else "card",
                ),
            x = SETTINGS.LOCATION_DECK_HINT_COORDINATE_X,
            y = SETTINGS.LOCATION_DECK_HINT_COORDINATE_Y_UPPER,
            color = arcade.color.WHITE,
            font_size = 15,
            anchor_x = "center",
            anchor_y = "center"
            )
            for cards_count in range(0, SETTINGS.DECK_SIZE_MAX + 1)
            }
        
        # Returning:
        return hint_text_cards_count_index
    
    
    @cached_property
    def hint_text_cards_count(self) -> arcade.Text:
        
        # Generating text object:
        hint_cards_count: arcade.Text = self.__hint_text_cards_count_index[self.cards_count]
        
        # Returning:
        return hint_cards_count
    
    
    @cached_property
    def __hint_trump_suit_index(self) -> dict[str, arcade.Text]:
        
        # Generating a dictionary index:
        suit_ascii_index = {
            attr_name.capitalize(): getattr(context.CARD_SUIT_ASCII, attr_name)
            for attr_name, attr_value in context.CARD_SUIT.__dict__.items()
            if not attr_name.startswith("_") and hasattr(context.CARD_SUIT_ASCII, attr_name)
            }

        # Generating card suit index:
        hint_trump_suit_index: dict[str, arcade.Text] = {
            card_suit: arcade.Text(
                text = suit_ascii_index[card_suit],
                x = SETTINGS.LOCATION_DECK_HINT_COORDINATE_X,
                y = SETTINGS.LOCATION_DECK_HINT_COORDINATE_Y_LOWER,
                color = arcade.color.WHITE,
                font_size = 10,
                anchor_x = "center",
                anchor_y = "center"
                ) 
            for card_suit in context.CARD_SUIT_LIST
            }

        # Returning:
        return hint_trump_suit_index


    @cached_property
    def hint_text_trump_suit(self) -> arcade.Text:
        
        
        # Getting correct arcade text:
        hint_text: arcade.Text = self.__hint_trump_suit_index[self.trump_suit]
        
        # Returning:
        return hint_text
    
    
    def display(self) -> None:
        
        # Calling display() method on all card objects:
        for card_object in self.cards:
            card_object.display()

    
    def display_hint(self) -> None:
        """
        THIS METHOD HAS NOT BEEN PROPERLY IMPLEMENTED AND IS FOR TEST USES ONLY!        
        """
        
        # Cards count remaining (if cards available):
        if self.cards_count > 0:
            self.hint_text_cards_count.draw()
        
        # Current trump suit (always on display):
        self.hint_text_trump_suit.draw()

