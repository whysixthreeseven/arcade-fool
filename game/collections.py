# Class checks import:
from enum import Enum


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
VARIABLES PACKED BLOCK

"""


class SORT_METHOD(Enum):
    
    # Sort method variables:
    BY_SUIT:    str = "BY_SUIT"
    BY_VALUE:   str = "BY_VALUE"
    BY_VALUE_C: str = "BY_VALUECLEAN"
    BY_ADDED:   str = "BY_ADDED"

    # Iteration variables
    ITEM_NEXT:  int = +1
    ITEM_PREV:  int = -1


class PLAYER_INFO(Enum):

    # Type variables:
    TYPE_NOT_SET:  str = "TYPE_NONE"
    TYPE_PLAYER:   str = "TYPE_PLAYER"
    TYPE_COMPUTER: str = "TYPE_COMPUTER"

    # Name variables:
    NAME_NOT_SET:    str = "NAME_NONE"
    NAME_PLAYER_ONE: str = "Player"
    NAME_PLAYER_TWO: str = "Computer"

    # State variables:
    STATE_ACTIVE:    str = "STATE_ACTIVE"
    STATE_INACTIVE:  str = "STATE_INACTIVE"
    STATE_ATTACKING: str = "STATE_ATTACKING"
    STATE_DEFENDING: str = "STATE_DEFENDING"


class CARD_INFO(Enum):

    # Suit variables:
    SUIT_NOT_SET:  str = "SUIT_NONE"
    SUIT_HEARTS:   str = "SUIT_HEARTS"
    SUIT_DIAMONDS: str = "SUIT_DIAMONDS"
    SUIT_CLUBS:    str = "SUIT_CLUBS"
    SUIT_SPADES:   str = "SUIT_SPADES"

    # Suit color variables:
    SUIT_COLOR_RED:   str = "SUIT_COLOR_RED"
    SUIT_COLOR_BLACK: str = "SUIT_COLOR_BLACK"

    # Type variables:
    TYPE_NOT_SET: str = "TYPE_NONE"
    TYPE_SIX:     str = "TYPE_SIX"
    TYPE_SEVEN:   str = "TYPE_SEVEN"
    TYPE_EIGHT:   str = "TYPE_EIGHT"
    TYPE_NINE:    str = "TYPE_NINE"
    TYPE_TEN:     str = "TYPE_TEN"
    TYPE_JACK:    str = "TYPE_JACK"
    TYPE_QUEEN:   str = "TYPE_QUEEN"
    TYPE_KING:    str = "TYPE_KING"
    TYPE_ACE:     str = "TYPE_ACE"

    # Location variables:
    LOCATION_NOT_SET: str = "LOCATION_NONE"
    LOCATION_HAND:    str = "LOCATION_HAND"
    LOCATION_TABLE:   str = "LOCATION_TABLE"
    LOCATION_DECK:    str = "LOCATION_DECK"
    LOCATION_DISCARD: str = "LOCATION_DISCARD"

    # Texture pack variables:
    TEXTURE_PACK_DEFAULT: str = "TEXTURE_PACK_DEFAULT"
