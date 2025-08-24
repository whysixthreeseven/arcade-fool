# Annotation import:
from __future__ import annotations

# Cache-related modules and scripts import:
from game.scripts import clear_cached_property
from functools import cached_property
from itertools import product

# Random library import:
import random

# Settings and variables import list:
from game.variables import *
from game.settings import *

# Developer session values:
from game.controllers.session import (
    DEV_ENABLE_ASSERTION,
    DEV_ENABLE_ECHO,
    )

# Assertion functions import:
from game.scripts import (
    assert_value_is_default,
    assert_value_is_valid_type,
    assert_value_in_valid_range,
    )

# Collections import:
from game.controllers.card import CardObject


class PlayerController:

    def __init__(self) -> None:

        self.__hand_container: list[CardObject] = []

        # State attributes:
        self.__state_active:    bool = False
        self.__state_attacking: bool = False
        self.__state_defending: bool = False

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    MISC METHODS BLOCK
    
    Miscellaneous private methods related to player controller designed to reduce code repetition 
    and redundancy, or to simplify several for-loops when clearing cache with a function imported 
    from scripts.py.

    """

    
    def __clear_cached_property(self, target_attribute: str) -> None:
        """
        Clears cache based on the attribute name, if it exeists in class object's dictionary via
        hasattr and delattr functions. Uses script from scripts.py. "Wraps" the script's function
        to shorten the syntax, since target_object is always self.

        :param str target_attribute: Cached attribute name string name.
        """

        # Clearing cache:
        clear_cached_property(
            target_object = self,
            target_attribute = target_attribute
            )
        
    
    def __clear_cached_property_list(self, target_list: tuple[str, ...]) -> None:
        """
        Clears cache based on the attribute name from the provided tuple container of properties
        list. Cycles through the attribute names and if it exists, deletes it.

        :param tuple[str, ...] target_list: Tuple container with attribute name strings.
        """

        # CLearing cache:
        for target_attribute in target_list:
            self.__clear_cached_property(
                target_attribute = target_attribute
                )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE PROPERTIES BLOCK
    
    Private cached properties dedicated to storing and returning tuple containers with related to
    their block's cachced property lists (e.g. __cached_hand_property_list would return all the 
    cached property (attribute) string value names to clear via a different clear cache function).

    """


    @cached_property
    def __cached_hand_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache. 
        
        Cached.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g. for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "hand_container",
            "hand_playable",
            "hand_count",
            "hand_value",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_state_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache. 
        
        Cached.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g. for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "state_active",
            "state_attacking",
            "state_defending",
            )
        
        # Returning:
        return cached_property_list


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    HAND METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def hand_container(self) -> list[CardObject]:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__hand_container
    

    @cached_property
    def hand_playable(self) -> list[CardObject]:
        """
        TODO: Create a docstring.
        """

        # Preparing a list:
        hand_playable: list[CardObject] = []

        # Acquiring all card objects that are playable:
        if self.hand_count > 0:
            hand_playable: list[CardObject] = [
                card_object for card_object
                in self.hand_container
                if card_object.state_playable
                ]
        
        # Returning:
        return hand_playable


    @cached_property
    def hand_count(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        hand_container_count: int = len(self.hand_container)

        # Returning:
        return hand_container_count

    
    @cached_property
    def hand_value(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Calculating:
        hand_value: int = 0
        if self.hand_count >= 1:
            for card_object in self.hand_container:
                hand_value += card_object.type_value
        
        # Returning:
        return hand_value


    @property
    def hand_position_index(self) -> dict[int, tuple[int, int]]:
        """
        TODO: Create a docstring.
        """

        # Preparing  dictionary to fill in:
        hand_position_index: dict[int, tuple[int, int]] = {
            position_index: ()
            for position_index in range(self.hand_count)
            }

        # Calculating the current hand width:
        card_overlap_current: int = HAND_OVERLAP_MARGIN_MAX
        hand_width_max: int = int(GAME_WINDOW_WIDTH * HAND_BOUNDARY_SIZE)
        hand_width_current: int = int(
            self.hand_count * 
            CARD_TEXTURE_WIDTH_SCALED * card_overlap_current
            )
        
        # Reducing hand size by increasing card overlap:
        while hand_width_current > hand_width_max:
            card_overlap_current: int = (card_overlap_current * HAND_OVERLAP_ITERATION)
            hand_width_current: int = int(
                self.hand_count * 
                CARD_TEXTURE_WIDTH_SCALED * card_overlap_current
                )

        # Calculating start position:
        card_coordinate_x_start: int = int(
            (GAME_WINDOW_WIDTH / 2 - hand_width_current / 2) + 
            CARD_TEXTURE_WIDTH_SCALED / 2
            )

        # Updating position index dictionary:
        for position_index in hand_position_index:
            coordinate_x: int = int(
                card_coordinate_x_start + 
                CARD_TEXTURE_WIDTH_SCALED * card_overlap_current * position_index
                )
            coordinate_y: int = CARD_COORDINATE_Y_HAND_PLAYER
            hand_position_index[position_index] = (coordinate_x, coordinate_y)
        
        # Returning:
        return hand_position_index


    def __update_hand_position(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Cycling through each card in hand:
        for card_object in self.hand_container:

            # Acquiring card object's position in hand and getting its appropriate coordinates:
            card_position: int = card_object.position_hand
            position_coordinates: tuple[int, int] = self.hand_position_index[card_position]

            # Updating coordiantes:
            card_object.set_coordinates(
                set_value = position_coordinates
                )


    def __update_hand_state(self) -> None:
        """
        TODO: Create a docstring.
        """

        ...


    def update_hand(self, table_map: dict[int, dict[int, tuple[int, int]]]) -> None:
        """
        TODO: Create a docstring.
        """

        # Resetting cards state:
        for card_object in self.hand_container:
            card_object.reset_state()

        # Updating based on attacking state:
        if self.state_attacking:

            # Acquiring cards avaialble:
            card_list_available: list[CardObject] = []

            # Cycling through all positions on table:
            for position_index in table_map:
                for stack_index in table_map[position_index]:

                    # If position is not empty, adding card to the list:
                    card_object: CardObject = table_map[position_index][stack_index]
                    if card_object is not None:
                        card_list_available.append(
                            card_object
                            )
            
            # Checking cards available count:
            card_list_available_count: int = len(card_list_available)

            # No cards on the table, all are playable:
            if card_list_available_count == 0:
                for card_object in self.hand_container:
                    card_object.set_state_playable(
                        set_value = True
                        )
            
            # Cards on table:
            else:
                ... # TODO: Continue




    def sort_hand(self, 
                  sort_method: str,                 # Default sort method as in SESSION controller
                  ascending_order: bool = True      # Value and card suit priority order
                  ) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:
            
            # Asserting sort method is valid type:
            valid_type: bool = str
            assert_value_is_valid_type(
                check_value = sort_method,
                valid_type = valid_type,
                raise_error = True
                )
            
            # Asserting sort method is a default variable:
            valid_list: tuple = (
                VAR_SESSION_SORT_METHOD_ADDED,
                VAR_SESSION_SORT_METHOD_VALUE,
                VAR_SESSION_SORT_METHOD_VALUE_CLEAN,
                VAR_SESSION_SORT_METHOD_SUIT
                )
            assert_value_is_default(
                check_value = sort_method,
                valid_list = valid_list,
                raise_error = True
                )
            
            # Asserting ascending order flag is valid type:
            valid_type: bool = bool
            assert_value_is_valid_type(
                check_value = ascending_order,
                valid_type = valid_type,
                raise_error = True
                )

        # Sorting if there are two or more cards in hand:
        if self.hand_count >= 2:

            # Sorting by suit priority (Hearts > Diamonds > Clubs > Spades):
            if sort_method == VAR_SESSION_SORT_METHOD_SUIT:
                reverse_check: bool = True if not ascending_order else False
                hand_sorted: list[CardObject] = sorted(
                    self.hand_container,
                    key = lambda card_object: int(          # Suit priority by index
                        CardObject.CARD_SUIT_LIST.index(
                            card_object.suit
                            )
                        ),
                    reverse = reverse_check,    # Top priority left (default)
                    )

            # Sorting by value (ignoring trump value):
            elif sort_method == VAR_SESSION_SORT_METHOD_VALUE_CLEAN:
                reverse_check: bool = True if not ascending_order else False
                hand_sorted: list[CardObject] = sorted(
                    self.hand_container,
                    key = lambda card_object: card_object.type_value_clean,
                    reverse = reverse_check,    # Highest left (default)
                    )

            # Sorting by value (default):
            elif sort_method == VAR_SESSION_SORT_METHOD_VALUE:
                reverse_check: bool = True if not ascending_order else False
                hand_sorted: list[CardObject] = sorted(
                    self.hand_container,
                    key = lambda card_object: card_object.type_value,
                    reverse = reverse_check,    # Highest left (default)
                    )

            # Sorting by time added to hand:
            elif sort_method == VAR_SESSION_SORT_METHOD_ADDED:
                reverse_check: bool = True if ascending_order else False
                hand_sorted: list[CardObject] = sorted(
                    self.hand_container,
                    key = lambda card_object: card_object.position_added,
                    reverse = reverse_check,        # First left (default)
                    )
            
            # Updating container:
            self.__hand_container: list[CardObject] = hand_sorted

            # Clearing cache:
            self.__clear_cached_property_list(
                target_list = self.__cached_hand_property_list
                )
            
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    STATE METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def state_active(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__state_active
    

    @cached_property
    def state_active_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Choosing correct repr string:
        state_active_repr: str = VAR_PLAYER_STATE_ACTIVE
        if not self.state_active:
            state_active_repr: str = VAR_PLAYER_STATE_INACTIVE

        # Returning:
        return state_active_repr
    

    @cached_property
    def state_attacking(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__state_attacking
    

    @cached_property
    def state_defending(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__state_defending
    

    @cached_property
    def state_focus_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Choosing correct repr string:
        if self.state_attacking and not self.state_defending:
            state_focus_repr: str = VAR_PLAYER_STATE_ATTACKING
        elif not self.state_attacking and self.state_defending:
            state_focus_repr: str = VAR_PLAYER_STATE_INACTIVE

        # Raising error, if both focus states are active or inactive:
        else:
            error_message: str = "{error_info}: {error_defails}.".format(
                error_info = "Player appears to have both focus states active or inactive",
                error_defails = f"{self.state_attacking=}, {self.state_defending=}"
                )
            raise AttributeError(error_message)

        # Returning:
        return state_focus_repr
    

    def reset_state(self) -> None:
        """
        TODO: Create a docstring.
        """

        # State attributes:
        self.__state_active:    bool = False
        self.__state_attacking: bool = False
        self.__state_defending: bool = False

        # Clearing cache:
        self.__clear_cached_property_list(
            target_list = self.__cached_state_property_list
            )
    

    def set_state_active(self, set_value: bool, ignore_assertion: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )
            
        # Updating attribute:
        if self.state_active != set_value:
            self.__state_active: bool = set_value

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "state_active"
                )
            
    
    def switch_state_active(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Switching flag value:
        switch_value: bool = True if not self.state_active else False
        self.set_state_active(
            set_value = switch_value,
            ignore_assertion = True,
            )
        
    
    def set_state_attacking(self, set_value: bool, ignore_assertion: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )
            
        # Updating attribute:
        if self.state_attacking != set_value:
            self.__state_attacking: bool = set_value

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "state_attacking"
                )
            
    
    def switch_state_attacking(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Switching flag value:
        switch_value: bool = True if not self.state_attacking else False
        self.set_state_attacking(
            set_value = switch_value,
            ignore_assertion = True,
            )
        
    
    def set_state_defending(self, set_value: bool, ignore_assertion: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )
            
        # Updating attribute:
        if self.state_defending != set_value:
            self.__state_defending: bool = set_value

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "state_defending"
                )
            
    
    def switch_state_defending(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Switching flag value:
        switch_value: bool = True if not self.state_defending else False
        self.set_state_attacking(
            set_value = switch_value,
            ignore_assertion = True,
            )
        

    def switch_state_focus(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Switching states:
        self.switch_state_attacking()
        self.switch_state_defending()            


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ADD/REMOVE CARD METHODS BLOCK

    """


    def add_card(self, card_object: CardObject, update_container: bool = True) -> None:
        """
        TODO: Create a docstring.
        """
        
        # Assertion control:
        if DEV_ENABLE_ASSERTION:
            ... # TODO

        # Checking if card already exists in the container:
        if card_object not in self.hand_container:

            # Updating card position:
            card_position: int = self.hand_count
            card_object.set_position_hand(
                position_index = card_position,
                update_related = True
                )
            
            # Adding card to the list:
            self.__hand_container.append(
                card_object
                )

            # Clearing cache:
            self.__clear_cached_property_list(
                target_list = self.__cached_hand_property_list
                )

            # Updating hand container (if required):
            if update_container:
                ... # TODO

    
    def remove_card(self, card_object: CardObject, update_container: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:
            ... # TODO

        # Checking if card exists in the container:
        if card_object in self.hand_container:

            # Updating card position:
            card_object.reset_position()

            # Removing card from the list:
            self.__hand_container.remove(
                card_object
                )
            
            # Clearing cache:
            ...

            # Updating hand container (if required):
            if update_container:
                ... # TODO

