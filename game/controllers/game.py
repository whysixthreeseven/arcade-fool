# Cache-related import:
from functools import cached_property

# Session variables import:
from game.session import (

    # Session controller object:
    Session_Controller,

    # Global session variables:
    SESSION_ENABLE_ASSERTION,
    SESSION_ENABLE_ECHO,
    )

# Controllers import:
from game.controllers.card import Card_Object
from game.controllers.deck import Deck_Controller
from game.controllers.discard import Discard_Controller
from game.controllers.table import Table_Controller
from game.controllers.player import Player_Controller

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
                    ignore_assertion = True,
                    update_related   = True,    # <- Switches related to False
                    )
                self.__player_one_controller.set_state_attacking(
                    set_value        = True,
                    ignore_assertion = True,
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
                    set_value        = False,
                    ignore_assertion = True,
                    update_related   = True,    # <- Switches related to False
                    )
                self.__player_two_controller.set_state_defending(
                    set_value        = True,
                    ignore_assertion = True,
                    update_related   = True,    # <- Switches related to False
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
                    set_value        = True,
                    ignore_assertion = True,
                    update_related   = True,    # <- Switches related to False
                    )
                
            # Setting player controller active:
            else:
                player_controller.set_state_active(
                    set_value        = True,
                    ignore_assertion = True,
                    update_related   = True,    # <- Switches related to False
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