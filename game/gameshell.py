# Arcade library import:
import arcade
from arcade import Rect, Text, Texture

# Gameshell-related settings import:
from game.settings import (

    # Game window settings:
    GAME_WINDOW_WIDTH,
    GAME_WINDOW_HEIGHT,
    GAME_WINDOW_FULLSCREEN,
    GAME_WINDOW_RESIZABLE,
    GAME_WINDOW_UPDATE_RATE,
    GAME_WINDOW_ANTIALIASING,
    GAME_WINDOW_TITLE,
    )

# Gameshell-related settings import:
from game.variables import (

    # Player type:
    PLAYER_TYPE_PLAYER
    )

# Zones import:
from game.collections.zone import (

    # Zone class object:
    Zone_XYWH,

    # Debugging zones:
    ZONE_GAME_AREA_PLAY,
    ZONE_GAME_AREA_SIDE,
    ZONE_PLAYER_ONE,
    ZONE_PLAYER_TWO,
    ZONE_TABLE,
    )


class Gameshell(arcade.Window):

    def __init__(self) -> None:

        # Initializing window with predefined settings:
        super().__init__(
            width        = GAME_WINDOW_WIDTH,
            height       = GAME_WINDOW_HEIGHT,
            title        = GAME_WINDOW_TITLE,
            fullscreen   = GAME_WINDOW_FULLSCREEN,
            resizable    = GAME_WINDOW_RESIZABLE,
            update_rate  = GAME_WINDOW_UPDATE_RATE,
            antialiasing = GAME_WINDOW_ANTIALIASING
            )
        
        # Controller attributes:
        self.__game_controller = None

        from game.controllers.hand import Hand_Controller
        self.hc = Hand_Controller()
        self.hc.set_hand_owner(set_value = PLAYER_TYPE_PLAYER)

        from game.controllers.deck import Deck_Controller
        self.dc = Deck_Controller()
        self.dc.create_deck()
        while self.hc.hand_count < 6:
            card = self.dc.draw_card()
            card.set_state_revealed(True)
            self.hc.add_card(card)
        self.hc.update_hand_position(True)

        self.zones: tuple[Zone_XYWH, ...] = (
            ZONE_GAME_AREA_PLAY,
            ZONE_GAME_AREA_SIDE,
            ZONE_PLAYER_ONE,
            ZONE_PLAYER_TWO,
            ZONE_TABLE,
            )

    
    def on_update(self, delta_time):
        pass


    def on_draw(self):
        self.clear()
        for zone in self.zones:
            zone.render()
        self.hc.render()

    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.A:
            if self.dc.deck_count > 0:
                card = self.dc.draw_card()
                card.set_state_revealed(True)
                self.hc.add_card(card, True)
                self.hc.update_hand_position(True)