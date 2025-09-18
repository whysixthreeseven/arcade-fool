# Annotations, typing etc. import:
from __future__ import annotations
from typing import Any

# Cache-related import:
from functools import cached_property

# Controller-related variables import:
from game.variables import (

    # Player type variables:
    PLAYER_TYPE_TAG,
    PLAYER_TYPE_NOT_SET,
    PLAYER_TYPE_PLAYER,
    PLAYER_TYPE_COMPUTER,
    PLAYER_STATE_FOCUS_ATTACKING,
    PLAYER_STATE_FOCUS_DEFENDING,

    # Hand-related methods:
    HAND_SORT_METHOD_BY_VALUE,
    HAND_SORT_METHOD_BY_VALUE_DEFAULT,
    HAND_SORT_METHOD_BY_TIME_ADDED,
    HAND_SORT_METHOD_BY_SUIT,
    )

# Controller-related settings import:
from game.settings import (

    # Game window settings:
    CARD_TEXTURE_WIDTH_SCALED,
    CARD_TEXTURE_HEIGHT_SCALED,

    # Hand settings:
    HAND_PLAYER_ONE_COORDINATE_X,
    HAND_PLAYER_ONE_COORDINATE_Y,
    HAND_PLAYER_TWO_COORDINATE_X,
    HAND_PLAYER_TWO_COORDINATE_Y,
    HAND_CARD_OVERLAP_MOD,
    HAND_CARD_OVERLAP_ITER,
    HAND_WIDTH_ALLOWED,

    # Slide settings:
    SLIDE_DISTANCE_HAND_X,
    SLIDE_DISTANCE_HAND_Y,
    SLIDE_DISTANCE_AXIS_PLAYER,
    SLIDE_DISTANCE_AXIS_COMPUTER,

    )

# Controllers import:
from game.controllers.card import Card_Object

# Scripts import:
from game.scripts.convert import (
    convert_attribute_to_repr
    )
from game.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list
    )



class Hand_Controller:

    def __init__(self):
        
        # Core attributes:
        self.__hand_container: list[Card_Object] = []
        self.__hand_added: int = 0
        self.__hand_owner: str = PLAYER_TYPE_NOT_SET

        # Coordinates attribute:
        self.__coordinate_x_center: int = 0
        self.__coordinate_y_center: int = 0

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    OVERWRITTEN MAGIC METHODS BLOCK
    
    """

    
    def __str__(self):
        """
        TODO: Create a docstring.
        """

        # Generating new string value:
        echo_string: str = ""

        # Returning:
        return echo_string
    

    def __repr__(self):
        """
        TODO: Create a docstring.
        """

        # Generating new string value:
        echo_string: str = ""

        # Returning:
        return echo_string
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def __cached_hand_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "hand_container",
            "hand_count",
            "hand_playable",
            "hand_playable_count",
            "hand_value",
            "hand_value_default",
            "hand_owner",
            "hand_position_index",
            )
        
        # Returning:
        return cached_property_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    HAND CONTAINER METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def hand_container(self) -> list[Card_Object]:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__hand_container
    

    @cached_property
    def hand_count(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        hand_count: int = len(self.hand_container)

        # Returning:
        return hand_count
    

    @cached_property
    def hand_playable(self) -> list[Card_Object]:
        """
        TODO: Create a docstring.
        """

        # Creating a new list of card objects:
        hand_playable: list[Card_Object] = [
            card_object for card_object 
            in self.hand_container
            if card_object.state_playable
            ]
        
        # Returning:
        return hand_playable
    

    @cached_property
    def hand_playable_count(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        hand_playable_count: int = len(self.hand_playable)

        # Returning:
        return hand_playable_count
    

    @cached_property
    def hand_value(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        hand_value: int = 0
        for card_object in self.hand_container:
            hand_value += card_object.type_value

        # Returning:
        return hand_value
    

    @cached_property
    def hand_value_default(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        hand_value_default: int = 0
        for card_object in self.hand_container:
            hand_value_default += card_object.type_value_default

        # Returning:
        return hand_value_default
    

    @cached_property
    def hand_added(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__hand_added
    

    @cached_property
    def hand_owner(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__hand_owner
    

    @cached_property
    def hand_owner_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Converting:
        hand_owner_repr: str = convert_attribute_to_repr(
            attribute_value = self.hand_owner,
            attribute_tag = PLAYER_TYPE_TAG
            )
        
        # Returning:
        return hand_owner_repr


    @cached_property
    def hand_position_index(self) -> dict[int, tuple[int, int]]:
        """
        TODO: Create a docstring.
        """

        # Calculating width value:
        hand_overlap_current: float = HAND_CARD_OVERLAP_MOD
        hand_width_current: int = int(
            self.hand_count * 
            CARD_TEXTURE_WIDTH_SCALED * 
            hand_overlap_current
            )
        
        # Recalculating if width value is larger than expected
        while hand_width_current > HAND_WIDTH_ALLOWED:
            hand_overlap_current *= HAND_CARD_OVERLAP_ITER
            hand_width_current: int = int(
                self.hand_count * 
                CARD_TEXTURE_WIDTH_SCALED * 
                hand_overlap_current
                )
        
        # Generating coordinates start:
        hand_coordinate_x_start: int = int(self.__coordinate_x_center - hand_width_current / 2)
        card_coordinate_x: int = int(hand_coordinate_x_start + CARD_TEXTURE_WIDTH_SCALED / 2)
        card_coordinate_y: int = self.__coordinate_y_center
        
        # Creating a new hand position index:
        hand_position_index: dict[int, tuple[int, int]] = {}
        hand_position_index_range: range = range(0, self.hand_count)
        for position_index in hand_position_index_range:
            hand_position_index[position_index] = (
                card_coordinate_x,
                card_coordinate_y
                )
            
            # Shifting coordinates per card:
            card_coordinate_x_shift: int = int(CARD_TEXTURE_WIDTH_SCALED * hand_overlap_current)
            card_coordinate_x += card_coordinate_x_shift

        # Returning:
        return hand_position_index


    def set_hand_added(self, set_value: int) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.hand_added != set_value:
            self.__hand_added: int = set_value

            # Clearing cache (property):
            cached_property: str = "hand_added"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def adjust_hand_added(self, adjust_value: int = 1) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        set_value: int = self.hand_added + adjust_value
        if set_value > 0:
            if self.hand_added != set_value:
                self.__hand_added: int = set_value

                # Clearing cache (property):
                cached_property: str = "hand_added"
                clear_cached_property(
                    target_object = self,
                    target_attribute = cached_property
                    )
        
        # Raising error, if attribute is to be decreased below zero:
        else:
            error_message: str = f"Parameter {adjust_value=} decreases hand added attribute below 0."
            raise AttributeError(error_message)


    def set_hand_owner(self, set_value: str) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.hand_owner != set_value:
            self.__hand_owner: str = set_value

            # Selecting correct coordinates based on hand owner:
            set_coordinate_x: int = int(
                HAND_PLAYER_ONE_COORDINATE_X if set_value == PLAYER_TYPE_PLAYER else 
                HAND_PLAYER_TWO_COORDINATE_X
                )
            set_coordinate_y: int = int(
                HAND_PLAYER_ONE_COORDINATE_Y if set_value == PLAYER_TYPE_PLAYER else 
                HAND_PLAYER_TWO_COORDINATE_Y
                )
            
            # Updating coordinates:
            self.__set_coordinate_x_center(
                set_value = set_coordinate_x,
                ignore_assertion = False,
                )
            self.__set_coordinate_y_center(
                set_value = set_coordinate_y,
                ignore_assertion = False,
                )
            
            # Clearing cache (property):
            cached_property: str = "hand_owner"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    

    def reset_hand(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Creating a new empty container:
        hand_container: list[Card_Object] = []
        hand_added: int = 0

        # Updating attributes:
        self.__hand_container: list[Card_Object] = hand_container
        self.__hand_added: int = hand_added

        # Clearing cache:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_hand_property_list
            )



    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ADD/REMOVE CARD OBJECT METHODS BLOCK
    
    """


    def add_card(self, card_object: Card_Object, clear_cache: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Checking if card does not exist in hand container:
        if card_object not in self.hand_container:

            # Resetting card object's position and state:
            card_object.reset_position()

            # Updating card object's hand position:
            position_hand_index: int = len(self.__hand_container)   # <- Using init container
            card_object.set_position_hand(
                position_index = position_hand_index
                )
            
            # Revealing the card:
            card_object.set_state_revealed(
                set_value = True,
                )
            
            if card_object.state_showcase:
                card_object.set_state_showcase(
                    set_value = False,
                    )
            
            # Updating card object's added position:
            self.adjust_hand_added(
                adjust_value = 1
                )
            card_object.set_position_added(
                position_index = self.__hand_added
                )

            # Adding card object to hand container:
            self.__hand_container.append(
                card_object
                )
            
            # Clearing cache (hand):
            if clear_cache:
                clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = self.__cached_hand_property_list
                    )
    

    def add_card_list(self, card_list: list[Card_Object]) -> None:
        """
        TODO: Create a docstring.
        """

        # Adding cards to the hand container:
        for card_object in card_list:
            self.add_card(
                card_object = card_object,
                clear_cache = False,
                )
            
        # Clearing cache (hand):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_hand_property_list
            )
            
    
    def remove_card(self, card_object: Card_Object) -> None:
        """
        TODO: Create a docstring.
        """

        # Checking if card exists in hand container:
        if card_object in self.hand_container:

            # Resetting card object's position:
            position_removed: int = card_object.position_hand
            card_object.reset_position()

            # Removing card object from hand container:
            self.__hand_container.remove(
                card_object
                )
            
            # Auto-updating other card's positions:
            hand_count: int = len(self.__hand_container)
            if hand_count > 0:

                # Checking card object's at position higher than removed:
                for card_object_rm in self.__hand_container:
                    if card_object_rm.position_hand > position_removed:

                        # Calculating and updating position index:
                        position_update: int = card_object_rm.position_hand - 1
                        card_object_rm.set_position_hand(
                            position_index = position_update
                            )
            
            # Clearing cache (hand):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_hand_property_list
                )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    UPDATE METHODS BLOCK
    
    """


    def update_hand_position(self, reset_coordinates: bool = False) -> None:
        """
        TODO: Create a docstring.
        """

        # Looping through cards:
        for card_object in self.hand_container:

            # Acquiring default coordinates:
            position_index: int = card_object.position_hand
            hand_coordinates: tuple[int, int] = self.hand_position_index[position_index]

            # Updating default coordinates:
            card_object.set_coordinates_default(
                set_container = hand_coordinates,
                ignore_assertion = True
                )
            if reset_coordinates:
                card_object.set_coordinates_current(
                    set_container = hand_coordinates,
                    ignore_assertion = True,
                    )
            
            # Calculating slide coordinates:
            hand_coordinate_x, hand_coordinate_y = hand_coordinates
            slide_axis: int = SLIDE_DISTANCE_AXIS_PLAYER 
            if self.hand_owner == PLAYER_TYPE_COMPUTER:
                slide_axis: int = SLIDE_DISTANCE_AXIS_COMPUTER
            slide_coordinate_x: int = hand_coordinate_x + SLIDE_DISTANCE_HAND_X
            slide_coordinate_y: int = int(hand_coordinate_y + SLIDE_DISTANCE_HAND_Y * slide_axis)

            # Updating slide coordinates:
            slide_coordinates: tuple[int, int] = (
                slide_coordinate_x,
                slide_coordinate_y
                )
            card_object.set_coordinates_slide(
                set_container = slide_coordinates,
                ignore_assertion = False,
                )
            
            
    def update_hand_state(self, 
                          player_focus_state: str,      # <- Default var (attacking or defending)
                          table_map: dict[int, dict[int, Card_Object | None]]
                          ) -> None:
        """
        TODO: Create a docstring.
        """

        # Asserting there are cards in hand to update:
        if self.hand_count > 0:

            # Resetting playable state prior to further checks:
            for card_object_hand in self.hand_container:
                card_object_hand.set_state_playable(
                    set_value = False
                    )
                
            # Collecting cards on the table:
            table_container: list[Card_Object] = []
            for position_index in table_map:
                for stack_index in table_map[position_index]:

                    # Adding card object to the list:
                    card_object_table: Card_Object | None = table_map[position_index][stack_index]
                    if card_object_table is not None:
                        table_container.append(
                            card_object_table
                            )
            
            # Counting cards on table:
            table_count: int = len(table_container)
            
            # Updating hand state based on attacking focus:
            if player_focus_state == PLAYER_STATE_FOCUS_ATTACKING:

                # Setting all cards as playable, if no cards have been played yet:
                if table_count == 0:
                    for card_object_hand in self.hand_container:
                        card_object_hand.set_state_playable(
                            set_value = True,
                            )
                        
                # Checking card types played:
                else:

                    # Collecting card types played:
                    card_type_list: list[str] = []
                    for card_object_table in table_container:
                        if card_object_table.type_f not in card_type_list:
                            card_type: str = card_object_table.type_f
                            card_type_list.append(
                                card_type
                                )
                    
                    # Checking if there are any cards in hand with the same type:
                    for card_object_hand in self.hand_container:
                        if card_object_hand.type_f in card_type_list:
                            card_object_hand.set_state_playable(
                                set_value = True
                                )

            # Updating hand state based on defending focus:
            elif player_focus_state == PLAYER_STATE_FOCUS_DEFENDING:
                
                # Skipping, if no cards have been played yet:
                if table_count == 0:
                    pass

                # Comparing card values, if cards have been played:
                else:
                    for card_object_hand in self.hand_container:
                        for card_object_table in table_container:

                            # Comarping cards based on values:
                            if card_object_hand > card_object_table:
                                card_object_hand.set_state_playable(
                                    set_value = True,
                                    )
                                break
                    

            # Raising error if state is not recognized:
            else:
                error_message: str = f"Unknown player focus state: ({player_focus_state=})."
                raise ValueError(error_message)
            
            # Clearing cache:
            cached_property_list: tuple[str, ...] = (
                "hand_playable",
                "hand_playable_count",
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    SORT METHODS BLOCK
    
    """

    def sort_hand(self, sort_method: str, reset_coordinates: bool = False) -> None:
        """
        TODO: Create a docstring.
        """

        # Preparing suit list to reference:
        suit_list: tuple[str, ...] = Card_Object.CARD_SUIT_LIST

        # Sorting hand by card's value:
        if sort_method == HAND_SORT_METHOD_BY_VALUE:
            hand_sorted: list[Card_Object] = sorted(
                self.hand_container,
                key = lambda card_object: (
                        card_object.type_value,
                        -suit_list.index(card_object.suit),
                        ),
                reverse = True,        # <- Strongest left, weakest right;
                )
        
        # Sorting hand by card's default value (ignore trump): 
        elif sort_method == HAND_SORT_METHOD_BY_VALUE_DEFAULT:
            hand_sorted: list[Card_Object] = sorted(
                self.hand_container,
                key = lambda card_object: (
                        card_object.type_value_default,
                        -suit_list.index(card_object.suit),
                        ),
                reverse = True,        # <- Strongest left, weakest right;
                )

        # Sorting hand by time it was added to container:
        elif sort_method == HAND_SORT_METHOD_BY_TIME_ADDED:
            hand_sorted: list[Card_Object] = sorted(
                self.hand_container,
                key = lambda card_object: card_object.position_added,
                reverse = False,         # <- 0 left, 52 right (old left, newest right);
                )

        # Sorting hand by suit index:
        elif sort_method == HAND_SORT_METHOD_BY_SUIT:
            hand_sorted: list[Card_Object] = sorted(
                self.hand_container,
                key = lambda card_object: (
                    suit_list.index(card_object.suit),
                    -card_object.type_value_default
                    ),
                reverse = False         # <- Hearts 0 > Diamonds 1 > Clubs 2 > Spades 3;
                )

        # Raising error if sort method is not recognized:
        else:
            error_message: str = f"Sort method provided {sort_method=} is not recognized."
            raise ValueError(error_message)
        
        # Updating card objects' based on their new position within the sorted container:
        for position_index, card_object in enumerate(hand_sorted):
            card_object.set_position_hand(
                position_index = position_index,
                ignore_assertion = True
                )
        
        # Forcing new coordinates:
        self.update_hand_position(
            reset_coordinates = reset_coordinates
            )
        
        # Forcing new attribute:
        self.__hand_container: list[Card_Object] = hand_sorted

        # Clearing cache:
        cached_property: str = "hand_container"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    COORDINATES METHODS AND PROPERTIES BLOCK
    
    """


    def __set_coordinate_x_center(self, 
                                  set_value: int, 
                                  ignore_assertion: bool = False
                                  ) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.__coordinate_x_center != set_value:
            self.__coordinate_x_center: int = set_value
    

    def __set_coordinate_y_center(self, 
                                  set_value: int, 
                                  ignore_assertion: bool = False
                                  ) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.__coordinate_y_center != set_value:
            self.__coordinate_y_center: int = set_value


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    RENDER METHODS AND PROPERTIES BLOCK
    
    """


    def render(self) -> None:
        """
        TODO: Create a docstring.
        """
        
        # Rendering each card object via own native render method:
        for card_object in self.hand_container:
            card_object.render()

