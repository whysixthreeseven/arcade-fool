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
        self.__owner: str = context.PLAYER_TYPE.HUMAN       # TODO: TEST CODE, REMOVE!
        
        # Container attributes:
        self.__card_list: list[Card] = []
    
    
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
        Clears all public cached cards properties of this card object.
        
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
        OWNER CACHED PROPERTIES AND METHODS
    
    """      
    
    
    @cached_property
    def owner(self) -> str:
        
        # Returning:
        return self.__owner
    
    
    def set_owner(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_player_type(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__owner = set_value

        # Clearing cache, if required:
        if clear_cache:
            cached_property: str = "owner"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
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
    
    
    def add_card(self, card_object: Card, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
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
        
        # Updating card added index:
        added_index: int = len(self.__card_list)
        card_object.set_added_index(
            set_value = added_index,
            ignore_assertion = True,
            clear_cache = True
            )
        
        # Updatin card's tilt:
        tilt_expected: int = card_object.render_tilt_default 
        if self.owner == context.PLAYER_TYPE.COMPUTER:
            tilt_expected: int = card_object.render_tilt_opp
        if card_object.render_tilt != tilt_expected:
            card_object.set_render_tilt(
                set_value = tilt_expected,
                ignore_assertion = True,
                clear_cache = True
                )
        
        # Updating card's location:
        location: context.Location = (
            context.CARD_LOCATION.PLAYER,
            self.__card_list.index(card_object)
            )
        card_object.set_location(
            set_value = location,
            ignore_assertion = True,
            clear_cache = True
            )
        
        # Updating card's states:
        card_object.set_state_location(
            clear_cache = True
            )
        
        # Updating card's expected coordinates:
        card_count: int = len(self.__card_list)
        container_index: int = self.__card_list.index(card_object)
        coordinates_expected: context.Coordinates = self.precalc_coordinates[card_count][container_index]
        card_object.set_coordinates_expected(
            set_value = coordinates_expected,
            ignore_assertion = True,
            clear_cache = True
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
            

    @cached_property
    def precalc_coordinates(self) -> dict[int, dict[int, context.Coordinates]]:
        
        # Creating coordinates dictionary index:
        coordinates_index: dict[int, dict[int, context.Coordinates]] = {
            card_count: {} for card_count in range(1, SETTINGS.DECK_SIZE_MAX)
            }
        
        # Starting loop:
        for card_count, inner_index in coordinates_index.items():
            
            # Preparing loop variables
            card_width: int = SETTINGS.CARD_TEXTURE_WIDTH
            card_overlap: int = SETTINGS.HAND_CARD_OVERLAP_START
            card_overlap_stop: int = SETTINGS.HAND_CARD_OVERLAP_STOP
            card_overlap_incr: int = SETTINGS.HAND_CARD_OVERLAP_INCREMENT
            
            # Getting hand width for only one card available:
            if card_count == 1:
                hand_width_current: int = card_width
                
            # Calculating hand width for more than one card:
            else:
                
                # First calculation attempt (for lesser amount of cards):
                hand_width_current: int = (
                    card_width +                                        # Fully visible card
                    card_width * card_overlap * (card_count - 1)        # Obscured (overlapped) cards
                    )
                
                # Incrementing card overlap value until hand width current is less than max available:
                hand_width_max: int = SETTINGS.HAND_WIDTH
                while hand_width_current > hand_width_max:
                    card_overlap = card_overlap - card_overlap * card_overlap_incr
                    if card_overlap < card_overlap_stop:
                        error_message: str = f"Card overlap value reached limit, check settings!"
                        raise ValueError(error_message)
                    hand_width_current: int = (
                        card_width +                                    # Fully visible card
                        card_width * card_overlap * (card_count - 1)    # Obscured (overlapped) cards
                        )
                
            # Calculating start and shift x coordinates:
            coordinate_x_start: int = int(
                SETTINGS.AREA_PLAYER_CENTER_COORDINATE_X - 
                hand_width_current / 2 +
                card_width / 2
                )
            coordinate_x_shift: int = int(
                card_width -
                card_width * (1.00 - card_overlap)
                )
            
            # Choosing start, hover and select y coordinate:
            coordinate_y: int = SETTINGS.AREA_PLAYER_CENTER_COORDINATE_Y
            if self.__owner == context.PLAYER_TYPE.COMPUTER:
                coordinate_y: int = SETTINGS.AREA_OPPONENT_CENTER_COORDINATE_Y

            for location_index in range(0, card_count):
                coordinate_x: int = coordinate_x_start + coordinate_x_shift * location_index
                coordinates_index[card_count][location_index] = (
                    coordinate_x,
                    coordinate_y,
                    )
            
        # Returning:
        return coordinates_index
    
    
    def __get_precalc_coordinates(self, card_object: Card) -> context.Coordinates:
        
        # Locating coordinates:
        coordinates_index: dict[int, dict[int, context.Coordinates]] = self.precalc_coordinates
        card_count: int = len(self.__card_list)
        calculated_cordinates: context.Coordinates = coordinates_index[card_count][card_object.location_index]
        
        # Returning:
        return calculated_cordinates

    
    def update_coordinates(self, clear_cache: bool = True) -> None:
        
        # Looping through each card, if cards are available:
        card_count: int = len(self.__card_list)
        if card_count > 0:
            for card_object in self.__card_list:
                
                # Obtaining coordinates and updating card object:
                coordinates_position: context.Coordinates = self.__get_precalc_coordinates(
                    card_object = card_object
                    )
                coordinate_x_position, coordinate_y_position = coordinates_position
                card_object.set_coordinates_position(
                    set_value = coordinates_position,
                    ignore_assertion = False,
                    clear_cache = clear_cache,
                    )
                
                # Calculating hover coordinates and updating card object:
                coordinate_x_hover: int = int(
                    coordinate_x_position +
                    SETTINGS.LOCATION_HAND_HOVER_SHIFT_COORDINATE_X if self.owner == context.PLAYER_TYPE.HUMAN 
                        else SETTINGS.LOCATION_OPP_HOVER_SHIFT_COORDINATE_X * -1
                    )
                coordinate_y_hover: int = int(
                    coordinate_y_position +
                    SETTINGS.LOCATION_HAND_HOVER_SHIFT_COORDINATE_Y if self.owner == context.PLAYER_TYPE.HUMAN 
                        else SETTINGS.LOCATION_HAND_HOVER_SHIFT_COORDINATE_Y * -1
                    )
                coordinates_hover: context.Coordinates = (
                    coordinate_x_hover,
                    coordinate_y_hover,
                    )
                card_object.set_coordinates_hover(
                    set_value = coordinates_hover,
                    ignore_assertion = False,
                    clear_cache = clear_cache,
                    )
                
                # Calculating selec coordinates and updating card object:
                coordinate_x_select: int = int(
                    coordinate_x_position +
                    SETTINGS.LOCATION_HAND_SELECT_SHIFT_COORDINATE_X if self.owner == context.PLAYER_TYPE.HUMAN 
                        else SETTINGS.LOCATION_OPP_SELECT_SHIFT_COORDINATE_X * -1
                    )
                coordinate_y_select: int = int(
                    coordinate_y_position +
                    SETTINGS.LOCATION_HAND_SELECT_SHIFT_COORDINATE_Y if self.owner == context.PLAYER_TYPE.HUMAN 
                        else SETTINGS.LOCATION_HAND_SELECT_SHIFT_COORDINATE_Y * -1
                    )
                coordinates_select: context.Coordinates = (
                    coordinate_x_select,
                    coordinate_y_select,
                    )
                card_object.set_coordinates_select(
                    set_value = coordinates_select,
                    ignore_assertion = False,
                    clear_cache = clear_cache,
                    )
                
        # Clearing cache:
        if clear_cache:
            self.clear_cached_cards_attributes()

    
    def reset_coordinates(self, clear_cache: bool = True) -> None:
        
        # Updating position, hover and select coordinates:
        self.update_coordinates(
            clear_cache = False
            )
        
        # Resetting current coordinates to position coordinates:
        for card_object in self.__card_list:
            card_object.set_coordinates(
                set_value = card_object.coordinates_position,
                ignore_assertion = True,
                clear_cache = True,
                )

        # Clearing cache:
        if clear_cache:
            self.clear_cached_cards_attributes()

    
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
            cached_property: str = "cards"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property,
            )
        
        
    def __sort_value(self, sort_reverse: bool = False, clear_cache: bool = True) -> None:
        
        # Sorting cards:
        self.__card_list.sort(
            key = lambda card: card.value,
            reverse = not sort_reverse,             # not sort_reverse, otherwise sorts ascending!
            )
        
        # Clearing cache, if required:
        if clear_cache:
            cached_property: str = "cards"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property,
            )
        
        
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
            cached_property: str = "cards"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property,
            )
    
        
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
            cached_property: str = "cards"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property,
            )
            
    
    def __sort_random(self, sort_reverse: bool = False, clear_cache: bool = True) -> None:
        
        # Sorting cards:
        random.shuffle(self.__card_list)
        
        # Clearing cache, if required:
        if clear_cache:
            cached_property: str = "cards"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property,
            )
        
    
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
        sort_seq_index: dict[str, function] = {
            context.HAND_SORT_SEQ.ADDED: lambda: self.__sort_added(sort_reverse = sort_reverse, clear_cache = False),
            context.HAND_SORT_SEQ.VALUE: lambda: self.__sort_value(sort_reverse = sort_reverse, clear_cache = False),
            context.HAND_SORT_SEQ.SUIT: lambda: self.__sort_suit(sort_reverse = sort_reverse, clear_cache = False),
            context.HAND_SORT_SEQ.COLOR: lambda: self.__sort_color(sort_reverse = sort_reverse, clear_cache = False),
            context.HAND_SORT_SEQ.RANDOM: lambda: self.__sort_random(sort_reverse = sort_reverse, clear_cache = False),
            }
        
        # Getting correct sorting sequence:
        sort_seq_func: function = sort_seq_index.get(
            sort_seq, 
            lambda: self.__sort_default(sort_reverse = False, clear_cache = False)
            )
        
        # Calling sorting sequence:
        sort_seq_func()
        
        # Updating location index:
        self.update_location_index(
            clear_cache = False
            )

        # Clearing cache, if required:
        if clear_cache:
            cached_property: str = "cards"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property,
                )
            
        # Updating coordinates, if required:
        if update_coordinates:
            self.update_coordinates(
                clear_cache = clear_cache
                )
                
        
    def sort_default(self, update_coordinates: bool = True, clear_cache: bool = True) -> None:
        
        # Calling default sorting sequence:
        self.sort(
            sort_seq = SESSION.HAND_SORT_SEQ_DEFAULT,
            sort_reverse = SESSION.HAND_SORT_SEQ_REVERSE,
            update_coordinates = update_coordinates,
            ignore_assertion = True,
            clear_cache = clear_cache
            )
        
    
    def sort_selected(self, update_coordinates: bool = True, clear_cache: bool = True) -> None:

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
    
    