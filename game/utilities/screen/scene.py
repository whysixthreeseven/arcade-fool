# Controllers:
from game.controller.player import PlayerController
from game.controller.location.discard import DiscardController
from game.controller.location.table import TableController
from game.controller.location.deck import DeckController
from game.controller.location.hand import HandController
from game.controller.card import CardController as Card
from game.utilities.screen import area
from game.utilities.screen.surface import Surface

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
from game.utilities import keymap
from game.utilities.scripts import assertion, validate


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    SCENE CLASS OBJECT CONSTRUCTOR
    
"""

class Scene:
    ...

    
""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    SCENE CLASS OBJECTS COLLECTION
    
"""


SCENE_GAME: Scene = Scene()