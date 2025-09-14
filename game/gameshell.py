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

    # Deck size:
    DECK_LOWEST_VALUE_DEFAULT,
    )

# Gameshell-related settings import:
from game.variables import *

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

# Controllers import:
from game.session import Session_Controller


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GAMESHELL CLASS OBJECT BLOCK

"""


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
        self.__session_controller: Session_Controller = Session_Controller()
        self.__game_controller = None

        from game.controllers.hand import Hand_Controller
        self.hc = Hand_Controller()
        self.hc.set_hand_owner(set_value = PLAYER_TYPE_PLAYER)

        from game.controllers.deck import Deck_Controller
        self.dc = Deck_Controller()
        self.dc.create_deck(
            deck_lowest_value = self.__session_controller.deck_lowest_value,
            deck_shift = self.__session_controller.deck_shift_threshold,
            )
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
        self.dc.render()
        self.hc.render()

    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.A:
            if self.dc.deck_count > 0:
                card = self.dc.draw_card()
                self.hc.add_card(card, True)
                self.hc.update_hand_position(True)
            
        elif symbol == arcade.key.R:
            from game.controllers.hand import Hand_Controller
            self.hc = Hand_Controller()
            self.hc.set_hand_owner(set_value = PLAYER_TYPE_PLAYER)

            from game.controllers.deck import Deck_Controller
            self.dc = Deck_Controller()
            self.dc.create_deck(
                deck_lowest_value = self.__session_controller.deck_lowest_value,
                deck_shift = self.__session_controller.deck_shift_threshold,
                )
            while self.hc.hand_count < 6:
                card = self.dc.draw_card()
                self.hc.add_card(card, True)
            self.hc.update_hand_position(True)

        elif symbol == arcade.key.T:
            self.__session_controller.texture_pack_front.switch_pack_next()

            self.dc.update_deck(
                texture_pack_front = self.__session_controller.texture_pack_front,
                texture_pack_back = self.__session_controller.texture_pack_back,
                )
            
            for card_object in self.hc.hand_container:
                card_object.update_texture(
                    texture_pack_front = self.__session_controller.texture_pack_front,
                    texture_pack_back = self.__session_controller.texture_pack_back,
                    )
                
        elif symbol == arcade.key.Y:
            self.__session_controller.texture_pack_back.switch_pack_next()
            self.dc.update_deck(
                texture_pack_front = self.__session_controller.texture_pack_front,
                texture_pack_back = self.__session_controller.texture_pack_back,
                )
            
            for card_object in self.hc.hand_container:
                card_object.update_texture(
                    texture_pack_front = self.__session_controller.texture_pack_front,
                    texture_pack_back = self.__session_controller.texture_pack_back,
                    )
                
        elif symbol == arcade.key.U:
            self.__session_controller.texture_pack_front.set_pack_default(TEXTURE_PACK_MODE_LIGHT)
            self.__session_controller.texture_pack_back.set_pack_default(TEXTURE_PACK_MODE_LIGHT)
            self.dc.update_deck(
                texture_pack_front = self.__session_controller.texture_pack_front,
                texture_pack_back = self.__session_controller.texture_pack_back,
                )
            
            for card_object in self.hc.hand_container:
                card_object.update_texture(
                    texture_pack_front = self.__session_controller.texture_pack_front,
                    texture_pack_back = self.__session_controller.texture_pack_back,
                    )
                
        elif symbol == arcade.key.I:
            self.__session_controller.texture_pack_front.set_pack_default(TEXTURE_PACK_MODE_DARK)
            self.__session_controller.texture_pack_back.set_pack_default(TEXTURE_PACK_MODE_DARK)
            self.dc.update_deck(
                texture_pack_front = self.__session_controller.texture_pack_front,
                texture_pack_back = self.__session_controller.texture_pack_back,
                )
            
            for card_object in self.hc.hand_container:
                card_object.update_texture(
                    texture_pack_front = self.__session_controller.texture_pack_front,
                    texture_pack_back = self.__session_controller.texture_pack_back,
                    )