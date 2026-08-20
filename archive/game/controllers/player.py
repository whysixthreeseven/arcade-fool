# Annotations, typing etc. import:
from __future__ import annotations
from typing import Any, Optional

# Random library import:
import random

# Cache-related import:
from functools import cached_property

# Controllers import:
from game.controllers.hand import Hand_Controller
from game.controllers.card import Card_Object

# Player-related variables import:
from game.variables import (

    # Player type variables:
    PLAYER_TYPE_TAG,
    PLAYER_TYPE_NOT_SET,
    PLAYER_TYPE_PLAYER,
    PLAYER_TYPE_COMPUTER,

    # Player name variables:
    PLAYER_ONE_NAME_DEFAULT,
    PLAYER_TWO_NAME_DEFAULT,
    PLAYER_NAME_GENDER_NOT_SET,
    PLAYER_NAME_GENDER_MALE,
    PLAYER_NAME_GENDER_FEMALE,

    # Player focus variables:
    PLAYER_STATE_FOCUS_TAG,
    PLAYER_STATE_FOCUS_ATTACKING,
    PLAYER_STATE_FOCUS_DEFENDING,
    )


# Session-related import:
from game.session import (
    SESSION_ENABLE_ASSERTION,
    SESSION_ENABLE_ECHO,
    )

# Scripts import:
from game.scripts.convert import (
    convert_attribute_to_repr,
    )
from game.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list
    )
from game.scripts.assertion import (
    assert_value_is_default,
    assert_value_is_valid_type,
    )


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PLAYER CONTROLLER CLASS OBJECT BLOCK

"""


class Player_Controller:

    # Player names index (computer):
    PLAYER_NAME_INDEX: dict[str, tuple[str, ...]] = {
        PLAYER_NAME_GENDER_MALE: (
            "Blake", "Brett", "Chase", "Clark", "Cole", "Drake", "Grant", "Jace", "Jack", "Jake",
            "James", "Luke", "Mark", "Max", "Paul", "Reed", "Rhys", "Scott", "Shawn", "Zane",
            "Axel", "Brock", "Caleb", "Carson", "Carter", "Dylan", "Ethan", "Graham", "Henry", 
            "Hunter", "Jackson", "Jasper", "Logan", "Mason", "Nolan", "Oscar", "Parker", "Riley", 
            "Simon", "Trevor", "Tyler", "Victor", "Walter", "Wyatt"
            ),
        PLAYER_NAME_GENDER_FEMALE: (
            "Brooke", "Claire", "Faith", "Faye", "Gail", "Grace", "Hope", "Jane", "Joy", "June",
            "Kate", "Leigh", "Lynn", "May", "Paige", "Pearl", "Quinn", "Rose", "Ruth", "Skye",
            "Alice", "Avery", "Bella", "Chloe", "Daisy", "Eden", "Emma", "Ella", "Hannah", "Holly",
            "Iris", "Ivy", "Jasmine", "Lily", "Maya", "Megan", "Nora", "Olive", "Piper", "Ruby",
            "Sarah", "Violet", "Willow", "Zoe"
            ),
        }
    

    def __init__(self):

        # Core attributes:
        self.__player_name: str = None
        self.__player_type: str = PLAYER_TYPE_NOT_SET
        
        # Hand controller:
        self.__hand_controller: Hand_Controller = None

        # State attributes:
        self.__state_active: bool = False
        self.__state_focus: str = None

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CLASS STATIC METHODS BLOCK
    
    """


    @staticmethod
    def create_player_controller(init_type: str, 
                                 init_name: Optional[str] = None,
                                 init_state_active: bool = False,
                                 init_state_focus: str = PLAYER_STATE_FOCUS_ATTACKING,
                                 ) -> Player_Controller:
        """
        TODO: Create a docstring.
        """        

        # Creating controller:
        player_controller: Player_Controller = Player_Controller()

        # Updating attributes:
        player_controller.set_player_type(
            set_value = init_type,
            )
        player_controller.set_state_active(
            set_value = init_state_active,
            )
        player_controller.set_state_focus(
            set_value = init_state_focus,
            )
        
        # Updating name attribute (random, default or set):
        if init_name is None:
            if init_type == PLAYER_TYPE_PLAYER:
                player_controller.set_player_name_default()
            else:
                player_controller.set_player_name_random(
                    player_gender = None
                    )
        else:
            player_controller.set_player_name(
                set_value = init_name,
                ignore_assertion = False,
                )
            
        # Creating hand:
        player_controller.create_hand()     # <- Check if init has a hand controller?
        player_controller.hand.set_hand_owner(
            set_value = init_type
            )

        # Returning:
        return player_controller

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def __cached_info_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "player_name",
            "player_type",
            "player_type_repr",
            "player_computer",
            )
        
        # Returning:
        return cached_property_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PLAYER INFO METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def player_name(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__player_name
    

    @cached_property
    def player_type(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__player_type
    

    @cached_property
    def player_type_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Formatting:
        player_type_repr: str = convert_attribute_to_repr(
            attribute_value = self.player_type,
            attribute_tag = PLAYER_TYPE_TAG,
            )
        
        # Returning:
        return player_type_repr
    

    @cached_property
    def player_computer(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Checking if player is computer-controlled:
        player_computer: bool = False
        if self.player_type == PLAYER_TYPE_COMPUTER:
            player_computer: bool = True

        # Returning:
        return player_computer
    

    def set_player_name(self, set_value: str, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if SESSION_ENABLE_ASSERTION and ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = str
            assert_value_is_valid_type(
                check_value = set_value,
                check_type  = valid_type,
                raise_error = True,
                )
            
        # Updating attribute:
        if self.player_name != set_value:
            self.__player_name: str = set_value

            # Clearing cache (property):
            cached_property: str = "player_name"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_player_name_default(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Choosing and setting default name based on player type:
        if self.player_type == PLAYER_TYPE_PLAYER:
            self.set_player_name(
                set_value = PLAYER_ONE_NAME_DEFAULT,
                ignore_assertion = True,
                )
        elif self.player_type == PLAYER_TYPE_COMPUTER:
            self.set_player_name(
                set_value = PLAYER_TWO_NAME_DEFAULT,
                ignore_assertion = True,
                )
        
        # Raising error, if no type set:
        else:
            error_message: str = f"Player type not set, cannot get default name value."
            raise AttributeError(error_message)
        
    
    def set_player_name_random(self, player_gender: Optional[str] = None) -> None:
        """
        TODO: Create a docstring.
        """

        # Checking if name should be random:
        name_random: bool = bool(
            player_gender == PLAYER_NAME_GENDER_NOT_SET or
            player_gender is None
            )
    
        # Selecting a random collection, and choosing a random name:
        if name_random:
            name_collection_combined: tuple[tuple, ...] = tuple(
                name_collection for name_collection 
                in Player_Controller.PLAYER_NAME_INDEX.values()
                )
            name_collection: tuple[str, ...] = random.choice(name_collection_combined)
            name_selected: str = random.choice(name_collection)

        # Selecting name based on parameter:
        else:
            name_selected: str = random.choice(Player_Controller.PLAYER_NAME_INDEX[player_gender])

        # Updating attribute:
        self.set_player_name(
            set_value = name_selected,
            ignore_assertion = True
            )

    
    def set_player_type(self, set_value: str) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if SESSION_ENABLE_ASSERTION:

            # Asserting value is valid type:
            valid_type: type = str
            assert_value_is_valid_type(
                check_value = set_value,
                check_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default (expected):
            default_list: tuple[str, ...] = (
                PLAYER_TYPE_PLAYER,
                PLAYER_TYPE_COMPUTER,
                )
            assert_value_is_default(
                check_value = set_value,
                check_list  = default_list,
                raise_error = True,
                )
            
        # Updating attribute:
        if self.player_type != set_value:
            self.__player_type: str = set_value

            # Clearing cache (property):
            cached_property_list: tuple[str, ...] = (
                "player_type",
                "player_type_repr",
                "player_computer",
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    HAND CONTROLLER METHODS AND PROPERTIES BLOCK
    
    """

    
    @cached_property
    def hand(self) -> Hand_Controller:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__hand_controller
    

    def create_hand(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Setting a new hand controller:
        hand_controller: Hand_Controller = Hand_Controller()
        self.__hand_controller: Hand_Controller = hand_controller

        # Updating controller:
        self.__hand_controller.set_hand_owner(
            set_value = self.player_type
            )

        # Clearing cache (property):
        cached_property: str = "hand"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property,
            )


    def reset_hand(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Resetting hand controller:
        if self.hand is not None:
            self.__hand_controller.reset_hand()


    def analyze_hand(self, table_map: dict[int, dict[int, Card_Object | None]]) -> None:
        """
        TODO: Create a docstring.
        """

        # Asserting there are cards in hand:
        if self.hand.hand_count > 0:

            # Resetting playable state:
            for card_stored in self.hand.hand_container:
                card_stored.set_state_playable(
                    set_value = False,
                    ignore_assertion = True,
                    )
                
            # Scanning table map and aquiring a card container
            table_container: list[Card_Object] = []
            for position_index in table_map:
                for stack_index in table_map[position_index]:

                    # If card object at position is not None, adding to container:
                    card_table: Card_Object | None = table_map[position_index][stack_index]
                    if card_table is not None:
                        table_container.append(
                            card_table
                            )
            
            # Counting cards:
            table_count: int = len(table_container)

            # Analyzing based on empty table:
            if table_count == 0:

                # If player is attacking:
                if self.state_attacking:

                    # Setting all cards as playable:
                    for card_stored in self.hand.hand_container:
                        card_stored.set_state_playable(
                            set_value = True,
                            ignore_assertion = True,
                            )
                
                # If player is defending:
                else:
                    pass        # <- Explicitly passing, as nothing changes
            
            # Analyzing based on table with cards played:
            else:

                # If player is attacking:
                if self.state_attacking:

                    # Collecting all played card types:
                    card_type_list: list[str] = []
                    for card_table in table_container:
                        if card_table.type_f not in card_type_list:
                            card_type_list.append(
                                card_table.type_f
                                )
                    
                    # Setting playable state to cards with same types:
                    for card_stored in self.hand.hand_container:
                        if card_stored.type_f in card_type_list:
                            card_stored.set_state_playable(
                                set_value = True,
                                ignore_assertion = True,
                                )
                
                # If player is defending:
                else:

                    # Comparing card values:
                    for card_table in table_container:
                        for card_stored in self.hand.hand_container:

                            # If card's value is greater (via __gt__), setting it as playable:
                            if card_stored > card_table:
                                card_stored.set_state_playable(
                                    set_value = True,
                                    ignore_assertion = True,
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
    def state_inactive(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Checking state:
        state_inverted: bool = True
        if self.__state_active:
            state_inverted: bool = False

        # Returning:
        return state_inverted
    

    @cached_property
    def state_attacking(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Checking state:
        state_attacking: bool = False
        if self.__state_focus == PLAYER_STATE_FOCUS_ATTACKING:
            state_attacking: bool = True
        
        # Returning:
        return state_attacking
    

    @cached_property
    def state_defending(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Checking state:
        state_defending: bool = False
        if self.__state_focus == PLAYER_STATE_FOCUS_DEFENDING:
            state_defending: bool = True
        
        # Returning:
        return state_defending
    

    @cached_property
    def state_focus(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__state_focus
    

    @cached_property
    def state_focus_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Formatting:
        state_focus_repr: str = convert_attribute_to_repr(
            attribute_value = self.state_focus,
            attribute_tag = PLAYER_STATE_FOCUS_TAG
            )
        
        # Returning:
        return state_focus_repr
    

    def set_state_active(self, set_value: bool) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if SESSION_ENABLE_ASSERTION:

            # Asserting value is valid:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                check_type  = valid_type,
                raise_error = True, 
                )
            
        # Updating attribute:
        if self.state_active != set_value:
            self.__state_active: bool = set_value

        # Clearing cache (property):
        cached_property_list: tuple[str, ...] = (
            "state_active",
            "state_inactive",
            )
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = cached_property_list
            )


    def set_state_focus(self, 
                        set_value: str, 
                        ignore_assertion: bool = False,
                        clear_cache: bool = True,
                        ) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting value is valid type:
            valid_type: type = str
            assert_value_is_valid_type(
                check_value = set_value,
                check_type  = valid_type,
                raise_error = True,
                )
            
            # Asserting value is default (expected):
            default_list: tuple[str, ...] = (
                PLAYER_STATE_FOCUS_ATTACKING,
                PLAYER_STATE_FOCUS_DEFENDING,
                )
            assert_value_is_default(
                check_value = set_value,
                check_list  = default_list,
                raise_error = True,
                )
            
        # Updating attribute:
        if self.state_focus != set_value:
            self.__state_focus: str = set_value

            # Clearing cache (property):
            if clear_cache:
                cached_property_list: tuple[str, ...] = (
                    "state_attacking",
                    "state_defending",
                    "state_focus",
                    "state_focus_repr"
                    )
                clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = cached_property_list
                    )
    

    def set_state_attacking(self, set_value: bool) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if SESSION_ENABLE_ASSERTION:

            # Asserting value is valid:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                check_type  = valid_type,
                raise_error = True, 
                )
            
        # Updating attribute:
        if not self.state_attacking:
            self.set_state_focus(
                set_value = PLAYER_STATE_FOCUS_ATTACKING,
                ignore_assertion = True,
                clear_cache = True
                )
    

    def set_state_defending(self, set_value: bool) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if SESSION_ENABLE_ASSERTION:

            # Asserting value is valid:
            valid_type: type = bool
            assert_value_is_valid_type(
                check_value = set_value,
                check_type  = valid_type,
                raise_error = True, 
                )
            
        # Updating attribute:
        if not self.state_defending:
            self.set_state_focus(
                set_value = PLAYER_STATE_FOCUS_DEFENDING,
                ignore_assertion = True,
                clear_cache = True
                )

    