from game.controller.card import Card


card = Card()

card.set_name("Jack", True, False)
card.set_suit("Hearts", True, False)
card.clear_cached_attributes()

print(card.name_ascii, card.suit_ascii, card.value, card.color)