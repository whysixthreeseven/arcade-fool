# External libraries:
from dataclasses import dataclass

# Relevant controllers
from game.controller.card import CardController as Card

# Settings, session and context:
from game import context


@dataclass(frozen = True)
class GameSnapshot:

    # Opponent cards:
    opponent_cards: context.CardContainer
    opponent_cards_count: int
    opponent_cards_value: int

    # Deck cards
    deck_cards: context.CardContainer
    deck_cards_count: int
    deck_cards_value: int

    # Discard cards
    discard_cards: context.CardContainer
    discard_cards_count: int
    discard_cards_value: int

    # Table cards:
    table_index: context.CardIndex
    table_cards: context.CardContainer
    table_cards_count: int
    table_cards_value: int

