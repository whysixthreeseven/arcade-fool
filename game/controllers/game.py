# Random library:
import random

# Cache-related import:
from functools import cached_property

# Controllers import:
from game.controllers.card import Card_Object
from game.controllers.deck import Deck_Controller
from game.controllers.discard import Discard_Controller
from game.controllers.table import Table_Controller
from game.controllers.player import Player_Controller

# Variables import:
from game.variables import *

# Settings import:
from game.settings import (
    
    # Deck render/shift threshold:
    DECK_RENDER_SHIFT_THRESHOLD_DEFAULT,
    DECK_RENDER_SHIFT_THRESHOLD_EXTENDED,

    # Deck size values:
    DECK_LOWEST_VALUE_DEFAULT,
    DECK_LOWEST_VALUE_EXTENDED,
    )

# Session variables import:
from game.session import (

    # Session controller object:
    Session_Controller,

    # Global session variables:
    SESSION_ENABLE_ASSERTION,
    SESSION_ENABLE_ECHO,
    )

# Collections import:
from game.collections.texturepack import Texture_Pack

# Scripts import:
from game.scripts.convert import (
    convert_attribute_to_repr
    )
from game.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list
    )


class Game_Controller:

    def __init__(self) -> None:

        # Controllers:
        self.__player_one_controller: Player_Controller  = None
        self.__player_two_controller: Player_Controller  = None
        self.__table_controller:      Table_Controller   = None
        self.__deck_controller:       Deck_Controller    = None
        self.__discard_controller:    Discard_Controller = None
        self.__session_controller:    Session_Controller = None


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE METHODS AND PROPERTIES BLOCK
    
    """


    @cached_property
    def __cached_player_property_list(self) -> tuple[str, ...]:
        """
        TODO: Create a docstring.
        """

        # Generating cached property list:
        cached_property_list: tuple[str, ...] = (
            "player_one",
            "player_two",
            "player_active",
            "player_inactive",
            "player_attacking",
            "player_defending",
            "player_list",
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


    def __create_game(self, deck_shift: str, deck_lowest_value: int) -> None:
        """
        TODO: Create a docstring.
        """

        # Checking if session exists:
        if self.session is None:
            self.create_session()

        # Creating a new deck:
        self.__create_deck(
            deck_shift = deck_shift,
            deck_lowest_value = deck_lowest_value
            )
        
        # Preparing player controller:
        player_one_name: str = self.__session_controller.player_one_name
        player_two_name: str = self.__session_controller.player_two_name
        player_one_controller = Player_Controller.create_player_controller(
            init_type = PLAYER_TYPE_PLAYER,
            init_name = player_one_name,
            )
        player_two_controller = Player_Controller.create_player_controller(
            init_type = PLAYER_TYPE_COMPUTER,
            init_name = player_two_name,
            )

        # Drawing cards to determine active and focus states:
        player_controller_list: tuple[Player_Controller, ...] = (
            player_one_controller,
            player_two_controller
            )
        for player_controller in player_controller_list:
            card_draw_list: list[Card_Object] = []
            card_draw_count: int = 0
            while card_draw_count < 6:
                card_draw: Card_Object = self.deck.draw_card()
                card_draw_list.append(
                    card_draw
                    )
                card_draw_count += 1

            # Adding cards in bulk to avoid excessive cache clearing:
            player_controller.hand.add_card_list(
                card_list = card_draw_list
                )
            
            # Updating hand container:
            player_controller.hand.update_hand_position(
                reset_coordinates = True,
                )




        
        # Updating controller attributes:
        self.__player_one_controller: Player_Controller  = player_one_controller
        self.__player_two_controller: Player_Controller  = player_two_controller

        # Clearing cache (player):
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_player_property_list
            )


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



    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    DECK CONTROLLER METHODS AND PROPERTIES BLOCK

    """

    
    @cached_property
    def deck(self) -> Deck_Controller:
        """
        TODO: Create a docstring.
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
        deck_controller.update_deck(
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



    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    TABLE CONTROLLER METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def table_controller(self) -> Table_Controller:
        """
        TODO: Create a docstring.
        """
        
        # Returning:
        return self.__table_controller


    
    
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
