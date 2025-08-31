# Cache-related modules and scripts import:
from game.scripts import clear_cached_property
from functools import cached_property

# Dataclass import:
from dataclasses import dataclass

# Class checks import:
from enum import Enum
from typing import ClassVar

# Settings and variables import list:
from game.collections import *
from game.settings import *

# Controller import:
from game.controllers.player import PlayerController

# Assertion functions import:
from game.scripts import (
    convert_to_repr,
    assert_value_is_valid_type,
    )

# Developer session values:
from game.controllers.session import (
    DEV_ENABLE_ASSERTION,
    DEV_ENABLE_ECHO,
    )


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GAME STATUS DATACLASS BLOCK

"""


class GAME_STATE(Enum):
    NOT_STARTED: str = "NOTSTARTED"
    PREPARING:   str = "PREPARING"
    STARTED:     str = "STARTED"
    PAUSED:      str = "PAUSED"
    FINISHED:    str = "FINISHED"


class TURN_STATE(Enum):
    NOT_STARTED:        str = "NOT-STARTED"
    WAITING_FOR_PLAYER: str = "WAITINGFORPLAYER"
    ANALYZING:          str = "ANALYZING"
    FINISHED:           str = "FINISHED"


class ROUND_STATE(Enum):
    NOT_STARTED: str = "NOTSTARTED"
    ON_GOING:    str = "ONGOING"
    ANALYZING:   str = "ANALYZING"
    FINISHING:   str = "FINISHING"


@dataclass
class Function_Set:
    sweep_cards: bool
    sweep_player_controller: PlayerController | None
    switch_active: bool
    switch_focus: bool



@dataclass
class GameStatus:
    
    # Core attributes:
    game_state:    GAME_STATE  = GAME_STATE.NOT_STARTED
    turn_state:    TURN_STATE  = TURN_STATE.NOT_STARTED
    round_state:   ROUND_STATE = ROUND_STATE.NOT_STARTED

    # Manual input attribute:
    waiting_input: bool = False

    # End turn func set:
    end_turn_func_set: Function_Set | None = None


    def __setattr__(self, name, value):
        
        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Mapping attribute names:
            attribute_map: dict[str, object] = {
                "game_state":  GAME_STATE,
                "turn_state":  TURN_STATE,
                "round_state": ROUND_STATE,
                "waiting_input": bool,
                }

            # Asserting attribute name is a default:
            if name in attribute_map.keys():
                attribute_type: type = attribute_map[name]            
                assert_value_is_valid_type(
                    check_value = value,
                    valid_type  = attribute_type,
                    raise_error = True
                    )
        
        # Setting attribute:
        super().__setattr__(name, value)


    @property
    def game_state_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Formatting:
        game_state_repr: str = convert_to_repr(
            attribute_string = self.game_state
            )
        
        # Returning:
        return game_state_repr
    

    @property
    def turn_state_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Formatting:
        turn_state_repr: str = convert_to_repr(
            attribute_string = self.turn_state
            )
        
        # Returning:
        return turn_state_repr
    

    @property
    def round_state_repr(self) -> str:
        """
        TODO: Create a docstring.
        """

        # Formatting:
        round_state_repr: str = convert_to_repr(
            attribute_string = self.round_state
            )
        
        # Returning:
        return round_state_repr
