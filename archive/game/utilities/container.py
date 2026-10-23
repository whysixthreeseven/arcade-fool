# Typing and annotations:
from typing import Literal

# External libraries:
from dataclasses import dataclass

# Timestamp function:
from game.utilities.scripts.timestamp import timestamp

# Context and namespaces:
from game import context


@dataclass(frozen = True)
class GameSnapshot:

    # Importing controllers to avoid circular imports:
    from game.controller.card import _Controller as Card

    # Turn and round information:
    turn_num: int
    turn_player: object
    turn_draw: object
    round_num: int

    # Attack and defence information:
    player_attacking: object
    player_defending: object

    # Player cards:
    player_cards: tuple[Card, ...]
    player_cards_count: int
    player_cards_value: int

    # Opponent cards:
    opponent_cards: tuple[Card, ...]
    opponent_cards_count: int
    opponent_cards_value: int

    # Deck cards:
    deck_cards: tuple[Card, ...]
    deck_cards_count: int
    deck_cards_value: int

    # Discard cards:
    discard_cards: tuple[Card, ...]
    discard_cards_count: int
    discard_cards_value: int

    # Table cards:
    table_index: dict[int, Card]
    table_cards: tuple[Card, ...]
    table_cards_count: int
    table_cards_value: int

    # Timestamp:
    __timestamp: str = timestamp()              # 2026-10-19 14:41:00


@dataclass(frozen = True)
class ComputerAction:

    # Importing controllers to avoid circular imports:
    from game.controller.card import _Controller as Card

    # Action type and card object involved:
    action_type: Literal["Attack", "Defend", "Fold", "Pass"]        # Default values found in game.context.COMPUTER_ACTION
    card_object: Card | None = None                                 # Card object, if Attack or Defend, otherwise None

