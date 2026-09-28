# Controllers:
from game.controller.player import Player
from game.controller.discard import Discard
from game.controller.table import Table
from game.controller.deck import Deck
from game.controller.hand import Hand
from game.controller.card import Card
from game.controller.surface import Surface

# External libraries:
import random
import arcade
import time

# Settings, session and context:
from game.settings import SETTINGS
from game.session import SESSION
from game import context

# Cache management:
from functools import cached_property
from game.utilities.scripts import cache

# Various utilities:
from game.utilities import texturepack
from game.utilities.scripts import assertion, validate


class Game:
    
    def __init__(self) -> None:
        
        # Player controllers:
        self.__player_one_controller: Player = None
        self.__player_two_controller: Player = None
        
        # Location controllers:
        self.__deck_controller: Deck = None
        self.__table_controller: Table = None
        self.__discard_controller: Discard = None
        
        # Surface and interface controllers:
        self.__surface_controller: Surface = None
        # self.__ui_controller: UI = None               # TODO: Implement!
        
        # Game state attributes:
        self.__game_started: bool = False
        self.__game_paused: bool = False
        self.__game_phase: str = None
        self.__game_ended: bool = False
        
        # Phrases:
        self.__player_attacker: Player = None
        self.__player_defender: Player = None
        
        # Round and turn attributes:
        self.__turn_num: int = 0
        self.__round_num: int = 0
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SETUP METHODS
    
    """
    
    
    def __setup_players(self) -> None:
        
        # Setting up player one (human):
        player_one_controller: Player = Player()
        player_one_controller.setup_human()

        # Setting up player two (computer):
        player_two_controller: Player = Player()
        player_two_controller.setup_computer()
        
        # Creating hand controllers and adding to player controllers:
        for player_controller in (player_one_controller, player_two_controller):
            hand_controller: Hand = Hand()
            hand_controller.setup(
                set_owner = player_controller.type,
                ignore_assertion = False,
                )
            player_controller.set_hand(
                set_value = hand_controller,
                ignore_assertion = False,
                clear_cache = True
                )
            
        # Updating attributes:
        self.__player_one_controller: Player = player_one_controller
        self.__player_two_controller: Player = player_two_controller
        
    
    def __setup_locations(self) -> None:
        
        # Creating locations controllers:
        deck_controller: Deck = Deck()
        discard_controller: Discard = Discard()
        table_controller: Table = Table()

        # Setting up controllers for the first time:
        for location_controller in (deck_controller, discard_controller, table_controller):
            location_controller.setup()
            
        # Updating attributes:
        self.__deck_controller: Deck = deck_controller
        self.__discard_controller: Discard = discard_controller
        self.__table_controller: Table = table_controller


    def __setup_surface(self) -> None:

        # Creating surface controller:
        surface_controller: Surface = Surface()
        
        # TODO: Edit Surface controller to create areas on call!
        ...

        # Updating attribute:
        self.__surface_controller: Surface = surface_controller
        

    def setup(self) -> None:
        
        # Calling setup methods in order:
        self.__setup_players()
        self.__setup_locations()
        self.__setup_surface()
        
        # TODO: Setup interface and events!
        
        
    def reset(self) -> None:
        
        # Resetting players' hand controllers:
        for player_controller in self.__player_controllers:
            player_controller.hand.reset()
            
        # Resetting location controllers:
        for location_controller in self.__location_controllers:
            location_controller.reset()
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        PLAYER CONTROLLERS PROPERTY LINKS
    
    """
    
    
    @property
    def player_human(self) -> Player:
        
        # Returning:
        return self.__player_one_controller
    

    @property
    def player_computer(self) -> Player:
        
        # Returning:
        return self.__player_two_controller
    
    
    @property
    def __player_controllers(self) -> tuple[Player, ...]:
        
        # Creating player controller list:
        player_controller_list: tuple[Player, ...] = (
            self.__player_one_controller,
            self.__player_two_controller,
            )

        # Returning player controller list:
        return player_controller_list
    
    
    @cached_property
    def player_attacking(self) -> Player:
        
        # Selecting correct player controller based on state:
        if self.player_human.state_attacking:
            return self.player_human
        elif self.player_computer.state_attacking:
            return self.player_computer
        
        # Raising error, if both controllers don't have the state enabled:
        else:
            error_message: str = f"Neither of player controllers' state is set to attacking!"
            raise AttributeError(error_message)
        
    
    @cached_property
    def player_defending(self) -> Player:
        
        # Selecting correct player controller based on state:
        if self.player_human.state_defending:
            return self.player_human
        elif self.player_computer.state_defending:
            return self.player_computer
        
        # Raising error, if both controllers don't have the state enabled:
        else:
            error_message: str = f"Neither of player controllers' state is set to defending!"
            raise AttributeError(error_message)
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        LOCATION CONTROLLERS PROPERTY LINKS
    
    """
    
    
    @property
    def deck(self) -> Deck:
        return self.__deck_controller
    
    
    @property
    def discard(self) -> Discard:
        return self.__discard_controller


    @property
    def table(self) -> Table:
        return self.__table_controller
    
    
    @property
    def __location_controllers(self) -> tuple[object, ...]:

        # Creating location controller list:
        loc_controller_list: tuple[object, ...] = (
            self.__deck_controller,
            self.__discard_controller,
            self.__table_controller,
            )

        # Returning location controller list:
        return loc_controller_list
    
    
    @property
    def surface(self) -> Surface:
        return self.__surface_controller
    
