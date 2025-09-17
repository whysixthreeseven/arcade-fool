# Dataclass import:
from dataclasses import dataclass

# Collections import:
from game.collections.texturepack import (
    Texture_Pack, 
    TEXTURE_PACK_FRONT_LIGHT_DEFAULT,
    TEXTURE_PACK_BACK_LIGHT_DEFAULT,
    )

# Variables import:
from game.variables import (

    # Player variables:
    PLAYER_ONE_NAME_DEFAULT,
    PLAYER_TWO_NAME_DEFAULT,

    # Texture pack types:
    TEXTURE_PACK_TYPE_FRONT,
    TEXTURE_PACK_TYPE_BACK,
    TEXTURE_PACK_MODE_LIGHT,
    TEXTURE_PACK_MODE_DARK,
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
SESSION_ENABLE_DEBUG: bool = True


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


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CALCULATED PROPERTIES BLOCK
    
    """


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
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    TEXTURE PACK METHODS AND PROPERTIES BLOCK
    
    """
    

    def set_texture_pack_front(self, texture_pack: Texture_Pack) -> None:
        """
        TODO: Create a docstring.
        """

        # Unpacking and setting new texture pack:
        texture_pack_container: tuple = texture_pack.pack_container
        self.texture_pack_front.set_pack(
            pack_container = texture_pack_container,
            pack_type = TEXTURE_PACK_TYPE_FRONT,
            clear_cache = True
            )
        

    def __set_texture_pack_front_default(self, texture_pack_mode: str) -> None:
        """
        TODO: Create a docstring.
        """

        # Setting new texture pack:
        self.texture_pack_front.set_pack_default(
            pack_mode = texture_pack_mode
            )
        
    
    def set_texture_pack_back(self, texture_pack: Texture_Pack) -> None:
        """
        TODO: Create a docstring.
        """

        # Unpacking and setting new texture pack:
        texture_pack_container: tuple = texture_pack.pack_container
        self.texture_pack_back.set_pack(
            pack_container = texture_pack_container,
            pack_type = TEXTURE_PACK_TYPE_FRONT,
            clear_cache = True
            )
    

    def __set_texture_pack_back_default(self, texture_pack_mode: str) -> None:
        """
        TODO: Create a docstring.
        """

        # Setting new texture pack:
        self.texture_pack_back.set_pack_default(
            pack_mode = texture_pack_mode
            )
        
    
    def set_texture_pack_default(self, texture_pack_mode: str) -> None:
        """
        TODO: Create a docstring.
        """

        # Setting default texture packs:
        self.__set_texture_pack_front_default(
            texture_pack_mode = texture_pack_mode
            )
        self.__set_texture_pack_back_default(
            texture_pack_mode = texture_pack_mode
            )
        
    
    def switch_texture_pack_front_next(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Switching texture pack:
        self.texture_pack_front.switch_pack_next()

    
    def switch_texture_pack_front_previous(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Switching texture pack:
        self.texture_pack_front.switch_pack_previous()

    
    def switch_texture_pack_back_next(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Switching texture pack:
        self.texture_pack_back.switch_pack_next()

    
    def switch_texture_pack_back_previous(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Switching texture pack:
        self.texture_pack_back.switch_pack_previous()

