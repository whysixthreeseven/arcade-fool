# External libraries:
from dataclasses import dataclass

# Timestamp function:
from game.utilities.scripts.timestamp import timestamp


@dataclass(frozen = True)
class GameSnapshot:

    # Importing controllers to avoid circular imports:
    from game.controller.player import PlayerController
    from game.controller.card import CardController as Card


    # Timestamp:
    __timestamp: str = timestamp()              # 2026-10-19 14:41:00

    # Turn and round information:
    turn_num: int
    turn_player: PlayerController
    round_num: int

    # Attack and defence information:
    player_attacking: PlayerController
    player_defending: PlayerController

    # Player cards:
    player_cards: tuple[Card, ...]
    player_cards_count: int
    player_cards_value: int

    # Opponent cards:
    opponent_cards: tuple[Card, ...]
    opponent_cards_count: int
    opponent_cards_value: int

    # Deck cards
    deck_cards: tuple[Card, ...]
    deck_cards_count: int
    deck_cards_value: int

    # Discard cards
    discard_cards: tuple[Card, ...]
    discard_cards_count: int
    discard_cards_value: int

    # Table cards:
    table_index: dict[int, Card]
    table_cards: tuple[Card, ...]
    table_cards_count: int
    table_cards_value: int

