from game.controllers.player import PlayerController
from game.collections import *



player = PlayerController()
player.set_player_name("andrey vostokov")
player.set_player_type(set_value=VAR_PLAYER_TYPE_PLAYER)
player.set_state_active(True)
player.set_state_attacking(True)


print(repr(player))