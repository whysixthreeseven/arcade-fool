from game.collections.deck import DeckController







deck = DeckController()

deck.create_deck()

deck.shuffle_deck()



import pprint



pprint.pprint(deck.deck_container)



