from game.controllers.deck import DeckController
from game.controllers.player import PlayerController
from game.controllers.card import CardObject

from game.controllers.session import SessionController

import pprint




# Deck test:
deck = DeckController()
deck.create_deck()
deck.shuffle_deck()

# Player test:
player = PlayerController()
while player.hand_count < 6:
    card_object: CardObject = deck.draw_card()
    print(card_object)
    player.add_card(
        card_object = card_object,
        update_container = True
        )
print(player.hand_container)
pprint.pprint(player.hand_position_index)


session = SessionController