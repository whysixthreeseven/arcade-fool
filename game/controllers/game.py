# Typing library import:
from typing import Any, Optional

# Random library:
import random

# Cache-related import:
from functools import cached_property

# Controllers import:
from game.session import Session_Controller
from game.controllers.card import Card_Object
from game.controllers.deck import Deck_Controller
from game.controllers.discard import Discard_Controller
from game.controllers.table import Table_Controller
from game.controllers.player import Player_Controller

# Collections import:
from game.collections.keyboard import Keyboard_Mapping
from game.collections.texturepack import Texture_Pack
from game.collections.zone import (

    # Zone class object:
    Zone_XYWH,

    # Debugging zones:
    ZONE_GAME_AREA_PLAY,
    ZONE_GAME_AREA_SIDE,
    ZONE_PLAYER_ONE,
    ZONE_PLAYER_TWO,
    ZONE_TABLE,
    )

# Variables import:
from game.variables import (

    # Player-related variables:
    PLAYER_ONE_NAME_DEFAULT,
    PLAYER_TWO_NAME_DEFAULT,
    PLAYER_TYPE_PLAYER,
    PLAYER_TYPE_COMPUTER,

    # Texture-related variables:
    TEXTURE_PACK_MODE_LIGHT,
    TEXTURE_PACK_MODE_DARK,

    # Hand-related methods:
    HAND_SORT_METHOD_BY_VALUE,
    HAND_SORT_METHOD_BY_VALUE_DEFAULT,
    HAND_SORT_METHOD_BY_TIME_ADDED,
    HAND_SORT_METHOD_BY_SUIT,
    )

# Settings import:
from game.settings import (
    
    # Deck-related settings:
    DECK_RENDER_SHIFT_THRESHOLD_DEFAULT,
    DECK_RENDER_SHIFT_THRESHOLD_EXTENDED,
    DECK_LOWEST_VALUE_DEFAULT,
    DECK_LOWEST_VALUE_EXTENDED,

    # Hand size default:
    HAND_CARD_COUNT_DEFAULT,
    )

# Session global variables import:
from game.session import (
    SESSION_ENABLE_ASSERTION,
    SESSION_ENABLE_ECHO,
    )

# Scripts import:
from game.scripts.convert import (
    convert_attribute_to_repr
    )
from game.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list
    )


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GAME CONTROLLER CLASS OBJECT BLOCK

"""


class Game_Controller:

    def __init__(self) -> None:

        # Controllers:
        self.__player_one_controller: Player_Controller  = None
        self.__player_two_controller: Player_Controller  = None
        self.__table_controller:      Table_Controller   = None
        self.__deck_controller:       Deck_Controller    = None
        self.__discard_controller:    Discard_Controller = None
        self.__session_controller:    Session_Controller = None

        # Keyboard mapping controller:
        self.__keyboard_mapping:      Keyboard_Mapping   = Keyboard_Mapping()


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def __cached_player_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.

        :return tuple[str, ...]: ...
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "player_one",
            "player_two",
            "player_list",
            "player_active",
            "player_inactive",
            "player_attacking",
            "player_defending",
            )
        
        # Returning:
        return cached_property_list
    

    @cached_property
    def __cached_controller_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.

        :return tuple[str, ...]: ...
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "player_one",
            "player_two",
            "session",
            "deck",
            "discard",
            "table"
            )
        
        # Returning:
        return cached_property_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    SESSION METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def session(self) -> Session_Controller:
        """
        TODO: Create a docstring.

        :return Session_Controller: ...
        """

        # Returning:
        return self.__session_controller
    

    def create_session(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating session:
        self.__session_controller: Session_Controller = Session_Controller()

        # Clearing cache:
        cached_property: str = "session"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
    

    def reset_session(self, preserve_name: bool = True) -> None:
        """
        TODO: Create a docstring.

        :param bool preserve_name: ...
        """

        # Setting default player names:
        player_one_name: str = PLAYER_ONE_NAME_DEFAULT
        player_two_name: str = PLAYER_TWO_NAME_DEFAULT

        # Checking if should preserve name:
        preserve_enabled: bool = preserve_name and self.session is not None 
        if preserve_enabled :
            player_one_name: str = self.session.player_one_name
            player_two_name: str = self.session.player_two_name

        # Creating a new session controller object:
        session_controller = Session_Controller(
            player_one_name = player_one_name,
            player_two_name = player_two_name
            )
        
        # Updating session:
        self.__session_controller: Session_Controller = session_controller

        # Clearing cache:
        cached_property: str = "session"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    GAME METHODS AND PROPERTIES BLOCK

    """


    @property
    def game_ready(self) -> bool:
        """
        TODO: Create a docstring.

        :return bool: ...
        """

        # Asserting all controllers are set:
        controllers_list: tuple[Any, ...] = (
            self.__player_one_controller,
            self.__player_two_controller,
            self.__table_controller,
            self.__deck_controller,
            self.__discard_controller,
            self.__session_controller,  
            )
        game_ready: bool = all(controllers_list)
        
        # Returning:
        return game_ready


    def __create_game(self, deck_shift: int, deck_lowest_value: int) -> None:
        """
        TODO: Create a docstring.

        :param int deck_shift: ...
        :param int deck_lowest_value: ...
        """

        # Checking if session exists:
        if self.session is None:
            self.create_session()

        # Creating various controllers:
        self.__create_deck(
            deck_shift = deck_shift,
            deck_lowest_value = deck_lowest_value,
            )
        self.__create_table()
        self.__create_discard()

        # Checking if player controllers exist:
        preserve_player_controllers: bool = bool(
            self.__player_one_controller is not None and
            self.__player_two_controller is not None
            ) 
        
        # Resetting or creating player controllers based on check:
        if preserve_player_controllers:
            for player_controller in self.player_list:
                player_controller.reset_hand()
        else:
            self.__create_player_controllers()
        
        # Filling hands for players:
        for player_controller in self.player_list:
            self.event_fill_hand(
                player_controller = player_controller
                )
            
            # Updating hand positions and sorting:
            player_controller.hand.sort_hand(
                sort_method = self.session.sort_method_default,
                reset_coordinates = True
                )
            
        # Getting player priority (who plays first):
        self.__update_player_priority()

        # Clearing cache (player):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_player_property_list
            )
        
        # Clearing cache (controllers):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_controller_property_list
            )
        
        # Updating textures (from previous game):
        update_texture_pack: bool = bool(
            self.session.texture_pack_front != self.session.texture_pack_front_default and
            self.session.texture_pack_back != self.session.texture_pack_back_default
            )
        if update_texture_pack:
            self.update_texture_pack()


    def create_game_custom(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Getting custom session values:
        deck_shift_custom: int = self.session.deck_shift_threshold
        deck_lowest_value: int = self.session.deck_lowest_value

        # Calling create method:
        self.__create_game(
            deck_shift = deck_shift_custom,
            deck_lowest_value = deck_lowest_value,
            )


    def create_game_default(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Calling create method:
        self.__create_game(
            deck_shift = DECK_RENDER_SHIFT_THRESHOLD_DEFAULT,
            deck_lowest_value = DECK_LOWEST_VALUE_DEFAULT,
            )
        

    def create_game_extended(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Calling create method:
        self.__create_game(
            deck_shift = DECK_RENDER_SHIFT_THRESHOLD_EXTENDED,
            deck_lowest_value = DECK_LOWEST_VALUE_EXTENDED,
            )
        
    
    def reset_game(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Resetting controllers:
        self.__reset_deck()
        self.__reset_discard()
        self.__reset_table()

        # Resetting hand controllers in players:
        for player_controller in self.player_list:
            player_controller.reset_hand()

        # Clearing cache (player):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_player_property_list
            )
        
        # Clearing cache (controllers):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_controller_property_list
            )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    DECK CONTROLLER METHODS AND PROPERTIES BLOCK

    """

    
    @cached_property
    def deck(self) -> Deck_Controller:
        """
        TODO: Create a docstring.

        :return Deck_Controller: ...
        """

        # Returning:
        return self.__deck_controller
    

    def __create_deck(self, 
                      deck_shift: int, 
                      deck_lowest_value: int, 
                      clear_cache: bool = True
                      ) -> None:
        """
        TODO: Create a docstring.

        :param int deck_shift: ...
        :param int deck_lowest_value: ...
        :param bool clear_cache: ...
        """

        # Creating deck controller object:
        deck_controller: Deck_Controller = Deck_Controller()

        # Calling core methods:
        deck_controller.create_deck(
            deck_shift = deck_shift,
            deck_lowest_value = deck_lowest_value,
            ignore_assertion = True
            )
        
        # Updating card objects' texture packs within deck:
        texture_pack_front = self.__session_controller.texture_pack_front
        texture_pack_back = self.__session_controller.texture_pack_back
        deck_controller.update_render_texture(
            texture_pack_front = texture_pack_front,
            texture_pack_back = texture_pack_back,
            ignore_assertion = True,
            )
        
        # Updating attribute:
        self.__deck_controller: Deck_Controller = deck_controller
        
        # Clearing cache (property):
        if clear_cache:
            cached_property: str = "deck"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
        
    
    def __reset_deck(self, clear_cache: bool = True) -> None:
        """
        TODO: Create a docstring.

        :param bool clear_cache: ...
        """

        # Acquiring session variables:
        deck_shift: int = self.__session_controller.deck_shift_threshold
        deck_lowest_value: int = self.__session_controller.deck_lowest_value

        # Calling methods:
        self.__create_deck(
            deck_shift = deck_shift,
            deck_lowest_value = deck_lowest_value,
            clear_cache = clear_cache
            )
        

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    DISCARD CONTROLLER METHODS AND PROPERTIES BLOCK

    """
        
    
    @cached_property
    def discard(self) -> Discard_Controller:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__discard_controller
        
    
    def __create_discard(self, clear_cache: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Creating discard controller:
        discard_controller: Discard_Controller = Discard_Controller()
        
        # Updating attribute:
        self.__discard_controller: Discard_Controller = discard_controller

        # Clearing cache:
        if clear_cache:
            cached_property: str = "discard"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )

    
    def __reset_discard(self, clear_cache: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        self.__discard_controller.reset_discard()

        # Clearing cache:
        if clear_cache:
            cached_property: str = "discard"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    TABLE CONTROLLER METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def table(self) -> Table_Controller:
        """
        TODO: Create a docstring.
        """
        
        # Returning:
        return self.__table_controller
    

    def __create_table(self, clear_cache: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Creating discard controller:
        table_controller: Table_Controller = Table_Controller()
        
        # Updating attribute:
        self.__table_controller: Table_Controller = table_controller

        # Clearing cache:
        if clear_cache:
            cached_property: str = "table"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )

    
    def __reset_table(self, clear_cache: bool = True) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        self.__table_controller.reset_table()

        # Clearing cache:
        if clear_cache:
            cached_property: str = "table"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PLAYER METHODS AND PROPERTIES BLOCK

    """

    @cached_property
    def player_one(self) -> Player_Controller:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__player_one_controller
    

    @cached_property
    def player_two(self) -> Player_Controller:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__player_two_controller
    

    @cached_property
    def player_active(self) -> Player_Controller:
        """
        TODO: Create a docstring.
        """

        # Selecting and returning with active state:
        if self.player_one.state_active:
            return self.player_one
        elif self.player_two.state_active:
            return self.player_two

        # Raising error if neither controller's state is active:
        else:
            error_message: str = f"Both player controllers appear to be inactive."
            raise AttributeError(error_message)
        

    @cached_property
    def player_inactive(self) -> Player_Controller:
        """
        TODO: Create a docstring.
        """

        # Selecting and returning controller with inactive state:
        if self.player_one.state_inactive:
            return self.player_one
        elif self.player_two.state_inactive:
            return self.player_two

        # Raising error if neither controller's state is active:
        else:
            error_message: str = f"Both player controllers appear to be active."
            raise AttributeError(error_message)
        
    
    @cached_property
    def player_attacking(self) -> Player_Controller:
        """
        TODO: Create a docstring.
        """

        # Selecting and returning controller with inactive state:
        if self.player_one.state_attacking:
            return self.player_one
        elif self.player_two.state_attacking:
            return self.player_two

        # Raising error if neither controller's state is active:
        else:
            error_message: str = f"Both player controllers appear to be defending."
            raise AttributeError(error_message)
        
    
    @cached_property
    def player_attacking(self) -> Player_Controller:
        """
        TODO: Create a docstring.
        """

        # Selecting and returning controller with inactive state:
        if self.player_one.state_defending:
            return self.player_one
        elif self.player_two.state_defending:
            return self.player_two

        # Raising error if neither controller's state is active:
        else:
            error_message: str = f"Both player controllers appear to be attacking."
            raise AttributeError(error_message)
    

    @cached_property
    def player_list(self) -> tuple[Player_Controller, Player_Controller]:
        """
        TODO: Create a docstring.
        """

        # Packing up:
        player_list: tuple[Player_Controller, Player_Controller] = (
            self.player_one,
            self.player_two
            )
        
        # Returning:
        return player_list
    

    def set_player_one(self, 
                       player_controller: Player_Controller, 
                       set_default_state: bool = True
                       ) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.player_one != player_controller:
            self.__player_one_controller: Player_Controller = player_controller

            # Setting default states to avoid conflicts:
            if set_default_state:
                self.__player_one_controller.set_state_active(
                    set_value        = True,
                    update_related   = True,    # <- Switches related to False
                    )
                self.__player_one_controller.set_state_attacking(
                    update_related   = True,    # <- Switches related to False
                    )

            # Clearing cache (player):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_player_property_list
                )
    

    def set_player_two(self, 
                       player_controller: Player_Controller, 
                       set_default_state: bool = True
                       ) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.player_two != player_controller:
            self.__player_two_controller: Player_Controller = player_controller

            # Setting default states to avoid conflicts:
            if set_default_state:
                self.__player_two_controller.set_state_active(
                    set_value = False,
                    )
                self.__player_two_controller.set_state_defending(
                    set_value = True,
                    )

            # Clearing cache (player):
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = self.__cached_player_property_list
                )
            
    
    def switch_players_active(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Cycling through player controllers:
        for player_controller in self.player_list:

            # Setting player controller inactive:
            if player_controller.state_active:
                player_controller.set_state_inactive(
                    set_value = True,
                    )
                
            # Setting player controller active:
            else:
                player_controller.set_state_active(
                    set_value = True,
                    )
        
        # Clearing cache (property):
        cached_property_list: tuple[str, ...] = (
            "player_active",
            "player_inactive",
            )
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = cached_property_list
            )


    def switch_players_focus(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Cycling through player controllers:
        for player_controller in self.player_list:

            # Setting player controller state defending:
            if player_controller.state_attacking:
                player_controller.set_state_defending(
                    set_value        = True,
                    ignore_assertion = True,
                    update_related   = True,    # <- Switches related to False
                    )
                
            # Setting player controller state attacking:
            else:
                player_controller.set_state_attacking(
                    set_value        = True,
                    ignore_assertion = True,
                    update_related   = True,    # <- Switches related to False
                    )
        
        # Clearing cache (property):
        cached_property_list: tuple[str, ...] = (
            "player_attacking",
            "player_defending",
            )
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = cached_property_list
            )
        
    
    def __create_player_controllers(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Selecting player names if session controller exists:
        player_one_name: str = PLAYER_ONE_NAME_DEFAULT
        player_two_name: str = PLAYER_TWO_NAME_DEFAULT
        if self.session is not None:
            player_one_name: str = self.__session_controller.player_one_name
            player_two_name: str = self.__session_controller.player_two_name

        # Preparing player controller:
        player_one_controller = Player_Controller.create_player_controller(
            init_type = PLAYER_TYPE_PLAYER,
            init_name = player_one_name,
            )
        player_two_controller = Player_Controller.create_player_controller(
            init_type = PLAYER_TYPE_COMPUTER,
            init_name = player_two_name,
            )
            
        # Updating controller attributes:
        self.__player_one_controller: Player_Controller  = player_one_controller
        self.__player_two_controller: Player_Controller  = player_two_controller

        # Clearing cache (player):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_player_property_list
            )
        
    
    # def __fill_player_hand_init(self, player_controller: Player_Controller) -> None:
    
    #     # Drawing cards:
    #     card_draw_list: list[Card_Object] = []
    #     card_draw_count: int = 0
    #     while card_draw_count < HAND_CARD_COUNT_DEFAULT:
    #         card_draw: Card_Object = self.deck.draw_card()
    #         card_draw_list.append(
    #             card_draw
    #             )
    #         card_draw_count += 1

    #     # Adding cards in bulk to avoid excessive cache clearing:
    #     player_controller.hand.add_card_list(
    #         card_list = card_draw_list
    #         )
        
    #     # Updating hand container:
    #     player_controller.hand.update_hand_position(
    #         reset_coordinates = True,
    #         )
        
    
    def __update_player_priority(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Preparing loop variables:
        card_trump_lowest_value: int | None = None
        player_priority: Player_Controller | None = None
        player_second: Player_Controller | None = None

        # Filtering cards by trump state for each player:
        for player_controller in self.player_list:
            card_trump_list: list[Card_Object] = [
                card_object for card_object
                in player_controller.hand.hand_container
                if card_object.state_trump
                ]
            
            # If player has trump cards, comparing values:
            card_trump_count: int = len(card_trump_list)
            if card_trump_count > 0:
                for card_trump in card_trump_list:

                    # First trump card found:
                    if card_trump_lowest_value is None:
                        card_trump_lowest_value: int = card_trump.type_value
                        player_priority: Player_Controller = player_priority

                    # Comparing trump cards with card's __gt__ and/or __lt__ methods:
                    else:
                        if card_trump.type_value < card_trump_lowest_value:
                            card_trump_lowest_value: int = card_trump.type_value
                            player_priority: Player_Controller = player_priority
        
        # Assigning priority variables:
        if player_priority is not None:
            if player_priority == self.player_one:
                player_second: Player_Controller = self.player_two
            else:
                player_second: Player_Controller = self.player_one
        
        # Assigning player one as player priority:
        player_priority: Player_Controller = self.player_one
        player_second: Player_Controller = self.player_two

        # Updating priority player states:
        player_priority.set_state_active(
            set_value = True,
            )
        player_priority.set_state_attacking(
            set_value = True,
            )
        
        # Updating second player states:
        player_second.set_state_active(
            set_value = False,
            )
        player_second.set_state_defending(
            set_value = True,
            )
        

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    KEYBOARD MAPPING PROPERTIES BLOCK

    """

    
    @cached_property
    def keyboard(self) -> Keyboard_Mapping:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__keyboard_mapping
    

    @cached_property
    def keyboard_sort_index(self) -> dict[int, str]:
        """
        TODO: Create a docstring.
        """

        # Generating:
        sort_key_index: dict[int, str] = {
            self.keyboard.KEY_DEBUG_SORT_HAND_BY_VALUE:         HAND_SORT_METHOD_BY_VALUE,
            self.keyboard.KEY_DEBUG_SORT_HAND_BY_VALUE_DEFAULT: HAND_SORT_METHOD_BY_VALUE_DEFAULT,
            self.keyboard.KEY_DEBUG_SORT_HAND_BY_TIME_ADDED:    HAND_SORT_METHOD_BY_TIME_ADDED,
            self.keyboard.KEY_DEBUG_SORT_HAND_BY_SUIT:          HAND_SORT_METHOD_BY_SUIT,
            }
        
        # Returning:
        return sort_key_index
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    TEXTURE UPDATE METHODS BLOCK

    """

    
    @property
    def __card_container_list(self) -> tuple[list[Card_Object]] | None:
        """
        TODO: Create a docstring.
        """

        # Collecting containers:
        card_container_list: tuple | None = None
        if self.game_ready:
            card_container_list: tuple[list[Card_Object]] = (
                self.player_one.hand.hand_container,
                self.player_two.hand.hand_container,
                self.deck.deck_container,
                self.discard.discard_container,
                self.table.table_container,
                )
        
        # Returning:
        return card_container_list


    def update_texture_pack(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Acquiring texture packs selected:
        texture_pack_front: Texture_Pack = self.session.texture_pack_front
        texture_pack_back: Texture_Pack = self.session.texture_pack_back
            
        # Updating card objects in all containers:
        for card_container in self.__card_container_list:
            for card_object in card_container:
                card_object.update_texture(
                    texture_pack_front = texture_pack_front,
                    texture_pack_back = texture_pack_back,
                    )
                
            # Manually updating render (fake) container:
            if card_container == self.deck.deck_container:
                self.deck.update_render_texture(
                    texture_pack_front = texture_pack_front,
                    texture_pack_back = texture_pack_back,
                    ignore_assertion = True
                    )
                
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    SORTING METHODS AND PROPERTIES BLOCK
    
    """


    def set_sort_method(self, sort_method: str) -> None:
        """
        TODO: Create a docstring.

        :param str sort_method: ...
        """

        # Updating session attribute
        self.session.sort_method = sort_method


    def set_sort_method_default(self) -> None:
        """
        TODO: Create a docstring.

        :param str sort_method: ...
        """

        # Getting default sort method:
        sort_method: str = self.session.sort_method_default

        # Updating session attribute
        self.session.sort_method = sort_method


    def handle_sort(self, 
                    player_controller: Player_Controller, 
                    reset_coordinates: bool = False
                    ) -> None:
        """
        TODO: Create a docstring.
        """

        # Getting current sort method:
        sort_method: str = self.session.sort_method

        # Sorting hand:
        player_controller.hand.sort_hand(
            sort_method = sort_method,
            reset_coordinates = reset_coordinates,
            )
        
    
    def event_sort_hand_default(self, 
                                player_controller: Player_Controller, 
                                reset_coordinates: bool = False
                                ) -> None:
        """
        TODO: Create a docstring.
        """

        # Getting current sort method:
        sort_method: str = self.session.sort_method_default

        # Sorting hand:
        player_controller.hand.sort_hand(
            sort_method = sort_method,
            reset_coordinates = reset_coordinates,
            )
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    DEBUG HANDLERS BLOCK
    
    """


    def handle_debug_key_pressed(self, key_pressed: Any) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating texture pack on call:
        if key_pressed in self.keyboard.key_debug_texture_list:

            # Switching texture packs:
            if key_pressed == self.keyboard.KEY_DEBUG_SWITCH_TEXTURE_PACK_FRONT:
                self.session.switch_texture_pack_front_next()
            elif key_pressed == self.keyboard.KEY_DEBUG_SWITCH_TEXTURE_PACK_BACK:
                self.session.switch_texture_pack_back_next()

            # Setting default texture packs:
            elif key_pressed == self.keyboard.KEY_DEBUG_SET_TEXTURE_PACK_DEFAULT_LIGHT:
                self.session.set_texture_pack_default(
                    texture_pack_mode = TEXTURE_PACK_MODE_LIGHT
                    )
            elif key_pressed == self.keyboard.KEY_DEBUG_SET_TEXTURE_PACK_DEFAULT_DARK:
                self.session.set_texture_pack_default(
                    texture_pack_mode = TEXTURE_PACK_MODE_DARK
                    )

            # Updating texture pack:
            self.update_texture_pack()

        # Sorting player's hand on call:
        elif key_pressed in self.keyboard.key_debug_sort_list:

            # Getting sort method from cached key index:
            if key_pressed in self.keyboard_sort_index:
                sort_method_selected: str = self.keyboard_sort_index[key_pressed]

            # Raising error on unrecognized or not implemented command call:
            else:
                error_message: str = f"Command call [{key_pressed=}] not implemented."
                raise NotImplemented(error_message)
            
            # Sorting:
            self.handle_sort(
                player_controller = self.player_one,
                sort_method = sort_method_selected,
                reset_coordinates = True,
                )

        # Adding card to player or opponent:
        elif key_pressed in self.keyboard.key_debug_draw_list:

            # Ensuring there are cards to draw:
            if self.deck.deck_count > 0:

                # Selecting player controller to draw cards for:
                player_controller: Player_Controller | None = None
                if key_pressed == self.keyboard.KEY_DEBUG_DRAW_CARD_PLAYER:
                    player_controller: Player_Controller = self.player_one
                elif key_pressed == self.keyboard.KEY_DEBUG_DRAW_CARD_OPPONENT:
                    player_controller: Player_Controller = self.player_two

                # Raising error on unrecognized or not implemented command call:
                else:
                    error_message: str = f"Command call [{key_pressed=}] not implemented."
                    raise NotImplemented(error_message)

                # Drawing card for selected controller:
                self.event_draw_card(
                    player_controller = player_controller
                    )
                
                # Automatically sorting, if enabled:
                if self.session.enable_autosort:
                    self.event_sort_hand_default(
                        player_controller = player_controller,
                        reset_coordinates = True    # <- DEBUG, remove when slide is finished
                        )
                # Updating hand position without sorting:
                else:
                    player_controller.hand.update_hand_position(
                        reset_coordinates = True        
                        )

        # RESTART GAME:
        elif key_pressed == self.keyboard.KEY_DEBUG_RESTART_GAME:
            self.create_game_default()


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    GAME HANDLERS BLOCK
    
    """


    def handle_key_pressed(self, key_pressed: int, ignore_assertion: bool = False) -> None:
        """
        TODO: Create a docstring.

        :param int key_pressed: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        """

        # Assertion control:
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:
            ...

        # Nothing to do, yet.
        if key_pressed in self.keyboard.key_user_list:
            ...


    def handle_mouse_click(self, click_coordinates: tuple[int, int]) -> None:
        """
        TODO: Create a docstring.
        """

        # Nothing to do, yet.
        pass


    def handle_mouse_release(self, click_coordinates: tuple[int, int]) -> None:
        """
        TODO: Create a docstring.
        """

        # Nothing to do, yet.
        pass


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    FIND ZONE METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def __zone_selection_list(self) -> tuple[Zone_XYWH, ...]:
        """
        TODO: Create a docstring.

        Cannot be cleared.

        :return tuple[Zone_XYWH, ...]: ...
        """

        # Creating a container:
        zone_list: tuple[Zone_XYWH, ...] = (
            ZONE_PLAYER_ONE,
            ZONE_PLAYER_TWO,
            ZONE_TABLE
            )
        
        # Returning:
        return zone_list
    

    @cached_property
    def __zone_area_list(self)-> tuple[Zone_XYWH, ...]:
        """
        TODO: Create a docstring.

        Cannot be cleared.

        :return tuple[Zone_XYWH, ...]: ...
        """

        # Creating a container:
        zone_list: tuple[Zone_XYWH, ...] = (
            ZONE_GAME_AREA_PLAY,
            ZONE_GAME_AREA_SIDE
            )
        
        # Returning:
        return zone_list
    

    def __find_zone_by_coordinates(self, 
                                   check_coordinates: tuple[int, int], 
                                   zone_container: tuple[Zone_XYWH, ...],
                                   ignore_assertion: bool = False,
                                   ) -> Zone_XYWH | None:
        """
        TODO: Create a docstring.

        :param tuple[int, int] check_coordinates: ...
        :param tuple[Zone_XYWH, ...] zone_container: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        """

        # Assertion control:
        if SESSION_ENABLE_ASSERTION and not ignore_assertion:
            ...

        # Unpacking:
        check_coordinate_x, check_coordinate_y = check_coordinates

        # Finding the correct zone:
        zone_object_found: Zone_XYWH | None = None
        for zone_object in zone_container:

            # Checking if coordinates are within zone object's boundaries:
            zone_accessed: bool = bool(
                check_coordinate_x in zone_object.coordinate_x_boundary and
                check_coordinate_y in zone_object.coordinate_y_boundary
                )
            
            # Updating variables and breaking:
            if zone_accessed:
                zone_object_found: Zone_XYWH = zone_object
                break
        
        # Returning:
        return zone_object_found
    

    def find_zone_selection_by_coordinates(self, 
                                           check_coordinates: tuple[int, int],
                                           ignore_assertion: bool = False,
                                           ) -> Zone_XYWH | None:
        """
        TODO: Create a docstring.

        :param tuple[int, int] check_coordinates: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        """

        # Finding zone object:
        zone_object_found: Zone_XYWH | None = self.__find_zone_by_coordinates(
            check_coordinates = check_coordinates,
            zone_container = self.__zone_selection_list,
            ignore_assertion = ignore_assertion,
            )
        
        # Returning:
        return zone_object_found


    def find_zone_area_by_coordinates(self, 
                                      check_coordinates: tuple[int, int],
                                      ignore_assertion: bool = False,
                                      ) -> Zone_XYWH | None:
        """
        TODO: Create a docstring.

        :param tuple[int, int] check_coordinates: ...
        :param bool ignore_assertion: ...

        :raise AssertionError: ...
        """

        # Finding zone object:
        zone_object_found: Zone_XYWH | None = self.__find_zone_by_coordinates(
            check_coordinates = check_coordinates,
            zone_container = self.__zone_area_list,
            ignore_assertion = ignore_assertion,
            )
        
        # Returning:
        return zone_object_found

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    EVENT METHODS BLOCK

    """


    def event_click_card(self, card_object: Card_Object) -> None:
        """
        TODO: Create a docstring.
        """

        # Nothing to do, yet.
        pass


    def event_draw_card(self, player_controller: Player_Controller) -> None:
        """
        TODO: Create a docstring.
        """

        # Drawing, if deck has cards to draw:
        if self.deck.deck_count > 0:
            card_object: Card_Object = self.deck.draw_card()

            # Adding card to player controller:
            player_controller.hand.add_card(
                card_object = card_object,
                clear_cache = True
                )
            
    
    def event_fill_hand(self, player_controller: Player_Controller) -> None:
        """
        TODO: Create a docstring.
        """

        # Adding card to the hand container:
        while player_controller.hand.hand_count < HAND_CARD_COUNT_DEFAULT:

            # Exiting, if no more cards available:
            if self.deck.deck_count == 0:
                break

            # Drawing cards:
            else:
                self.event_draw_card(
                    player_controller = player_controller,
                    )



    
