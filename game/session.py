# Dataclass import:
from dataclasses import dataclass

# Collections import:
from game.collections.texturepack import (

    # Texture packs:
    Texture_Pack, 
    TEXTURE_PACK_FRONT_LIGHT_DEFAULT,
    TEXTURE_PACK_BACK_LIGHT_DEFAULT,
    )

# Variables import:
from game.variables import (

    # Player variables:
    PLAYER_ONE_NAME_DEFAULT,
    PLAYER_TWO_NAME_DEFAULT,
    )

# Settings import:
from game.settings import (

    # Deck settings:
    DECK_LOWEST_VALUE_DEFAULT,
    DECK_LOWEST_VALUE_EXTENDED,
    DECK_RENDER_SHIFT_THRESHOLD_DEFAULT,
    DECK_RENDER_SHIFT_THRESHOLD_EXTENDED,
    )


# Global (debug) session variables:
SESSION_ENABLE_ASSERTION: bool = True
SESSION_ENABLE_ECHO: bool = True


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
SESSION DATACLASS OBJECT BLOCK

"""

@dataclass(order = True)
class Session_Controller:


    # Texture pack session variables:
    texture_pack_front_default: Texture_Pack = TEXTURE_PACK_FRONT_LIGHT_DEFAULT
    texture_pack_front:         Texture_Pack = TEXTURE_PACK_FRONT_LIGHT_DEFAULT
    texture_pack_back_default:  Texture_Pack = TEXTURE_PACK_BACK_LIGHT_DEFAULT
    texture_pack_back:          Texture_Pack = TEXTURE_PACK_BACK_LIGHT_DEFAULT

    # Player name session variables:
    player_one_name_default: str = PLAYER_ONE_NAME_DEFAULT
    player_one_name:         str = PLAYER_ONE_NAME_DEFAULT
    player_two_name_default: str = PLAYER_TWO_NAME_DEFAULT
    player_two_name:         str = PLAYER_TWO_NAME_DEFAULT

    # Game session variables:
    deck_lowest_value_default: int = DECK_LOWEST_VALUE_DEFAULT
    deck_lowest_value:         int = DECK_LOWEST_VALUE_DEFAULT


    @property
    def deck_shift_threshold(self) -> int:
        """
        TODO: Create a docstring.
        """

        # Selecting the correct threshold:
        deck_shift_threshold: int = DECK_RENDER_SHIFT_THRESHOLD_DEFAULT
        if self.deck_lowest_value == DECK_LOWEST_VALUE_EXTENDED:
            deck_shift_threshold: int = DECK_RENDER_SHIFT_THRESHOLD_EXTENDED
            
        # Returning:
        return deck_shift_threshold
    

