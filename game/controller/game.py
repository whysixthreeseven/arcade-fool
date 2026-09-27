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
        
        