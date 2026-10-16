# External libraries:
import random

# Settings, session and context:
from game import context

# Various utilities:
from game.utilities import texturepack as tp
from game.utilities.scripts import validate


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    SESSION CLASS OBJECT CONSTRUCTOR
    
"""


class __SESSION:
    
    def __init__(self) -> None:
        
        # Developer options:
        self.__enable_assertion: bool = True
        self.__enable_debug: bool = False
        self.__enable_hint: bool = True
        self.__enable_reveal: bool = False
        
        # Texture pack options:
        self.__texturepack_front_default: tp.TexturePack = tp.TEXTUREPACK_FRONT.LIGHT_2_1
        self.__texturepack_front_selected: tp.TexturePack = tp.TEXTUREPACK_FRONT.LIGHT_2_1
        self.__texturepack_back_default: tp.TexturePack = tp.TEXTUREPACK_BACK.PLAIN_WHITE
        self.__texturepack_back_selected: tp.TexturePack = tp.TEXTUREPACK_BACK.PLAIN_WHITE
        
        # Game modes:
        self.__game_mode_secret: bool = True
        self.__game_mode_reverse: bool = False
        self.__game_mode_reveal: bool = False
        
        # Deck size selected:
        self.__deck_size_selected: int = 36             # Default value!
        
        # Hand sort modes:
        self.__hand_sort_seq_default: str = context.HAND_SORT_SEQ.SUIT
        self.__hand_sort_seq_selected: str = context.HAND_SORT_SEQ.SUIT
        self.__hand_sort_seq_reverse: bool = False

        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED DEBUG PROPERTIES AND METHODS
    
    """
        
    
    @property
    def ENABLE_ASSERTION(self) -> bool:
        
        # Returning:
        return self.__enable_assertion
    
    
    @property
    def ENABLE_DEBUG(self) -> bool:

        # Returning:
        return self.__enable_debug
    
    
    @property
    def ENABLE_HINT(self) -> bool:

        # Returning:
        return self.__enable_hint
    
    
    @property
    def ENABLE_REVEAL(self) -> bool:

        # Returning:
        return self.__enable_reveal
    
    
    def set_enable_assertion(self, set_value: bool, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__enable_assertion = set_value

    
    def switch_enable_assertion(self) -> None:
                
        # Switching:
        self.__enable_assertion = not self.__enable_assertion


    def set_enable_debug(self, set_value: bool, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )

        # Updating attribute:
        self.__enable_debug = set_value


    def switch_enable_debug(self) -> None:

        # Switching:
        self.__enable_debug = not self.__enable_debug
        
        
    def set_enable_hint(self, set_value: bool, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )

        # Updating attribute:
        self.__enable_hint = set_value

    
    def switch_enable_hint(self) -> None:

        # Switching:
        self.__enable_hint = not self.__enable_hint

    
    def set_enable_reveal(self, set_value: bool, ignore_assertion: bool = False) -> None:
            
        # Assertion control:
        if not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__enable_reveal = set_value
        
    
    def switch_enable_reveal(self) -> None:
                
        # Switching:
        self.__enable_reveal = not self.__enable_reveal


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        TEXTURE PACK CACHED PROPERTIES AND METHODS
    
    """
    
    
    @property
    def TEXTUREPACK_FRONT_DEFAULT(self) -> tp.TexturePack:

        # Returning:
        return self.__texturepack_front_default
    
    
    @property
    def TEXTUREPACK_FRONT_SELECTED(self) -> tp.TexturePack:
        
        # Returning:
        return self.__texturepack_front_selected
    
    
    @property
    def TEXTUREPACK_FRONT_SELECTED_INDEX(self) -> int:
        
        # Locating index:
        texturepack_index: int = tp.TEXTUREPACK_FRONT_LIST.index(
            self.__texturepack_front_selected
            )

        # Returning:
        return texturepack_index
    
    
    @property
    def TEXTUREPACK_BACK_DEFAULT(self) -> tp.TexturePack:

        # Returning:
        return self.__texturepack_back_default
    

    @property
    def TEXTUREPACK_BACK_SELECTED(self) -> tp.TexturePack:

        # Returning:
        return self.__texturepack_back_selected
    
    
    @property
    def TEXTUREPACK_BACK_SELECTED_INDEX(self) -> int:
        
        # Locating index:
        texturepack_index: int = tp.TEXTUREPACK_BACK_LIST.index(
            self.__texturepack_back_selected
            )

        # Returning:
        return texturepack_index
    
    
    def set_texturepack_front(self, set_value: tp.TexturePack, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            validate.validate_texturepack(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__texturepack_front_selected = set_value

    
    def set_texturepack_front_next(self) -> None:
        
        # Retrieving next index:
        texturepack_next: int = (self.TEXTUREPACK_FRONT_SELECTED_INDEX + 1) % len(tp.TEXTUREPACK_FRONT_LIST)
            
        # Updating attribute:
        self.set_texturepack_front(
            set_value = tp.TEXTUREPACK_FRONT_LIST[texturepack_next],
            ignore_assertion = True,
            )
        
    
    def set_texturepack_front_previous(self) -> None:
            
        # Retrieving next index:
        texturepack_previous: int = (self.TEXTUREPACK_FRONT_SELECTED_INDEX - 1) % len(tp.TEXTUREPACK_FRONT_LIST)
            
        # Updating attribute:
        self.set_texturepack_front(
            set_value = tp.TEXTUREPACK_FRONT_LIST[texturepack_previous],
            ignore_assertion = True,
            )
        
        
    def set_texturepack_front_random(self) -> None:
        
        # Selecting random texture pack:
        texture_pack_random: tp.TexturePack = random.choice(tp.TEXTUREPACK_FRONT_LIST)
        
        # Updating attribute:
        self.set_texturepack_front(
            set_value = texture_pack_random,
            ignore_assertion = True,
            )
        

    def set_texturepack_back(self, set_value: tp.TexturePack, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            validate.validate_texturepack(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__texturepack_back_selected = set_value

    
    def set_texturepack_back_next(self) -> None:
            
        # Retrieving next index:
        texturepack_next: int = self.TEXTUREPACK_BACK_SELECTED_INDEX + 1
        texturepack_count: int = len(tp.TEXTUREPACK_BACK_LIST)
        if texturepack_next >= texturepack_count:
            texturepack_next = 0
            
        # Updating attribute:
        self.set_texturepack_back(
            set_value = tp.TEXTUREPACK_BACK_LIST[texturepack_next],
            ignore_assertion = True,
            )
        
    
    def set_texturepack_back_previous(self) -> None:
                
        # Retrieving next index:
        texturepack_previous: int = self.TEXTUREPACK_BACK_SELECTED_INDEX - 1
        texturepack_count: int = len(tp.TEXTUREPACK_BACK_LIST)
        if texturepack_previous < 0:
            texturepack_previous = texturepack_count - 1
            
        # Updating attribute:
        self.set_texturepack_back(
            set_value = tp.TEXTUREPACK_BACK_LIST[texturepack_previous],
            ignore_assertion = True,
            )
            
    
    def set_texturepack_back_random(self) -> None:

        # Selecting random texture pack:
        texturepack_random: tp.TexturePack = random.choice(tp.TEXTUREPACK_BACK_LIST)

        # Updating attribute:
        self.set_texturepack_back(
            set_value = texturepack_random,
            ignore_assertion = True,
            )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        GAME MODE CACHED PROPERTIES AND METHODS
    
    """
    
    
    @property
    def GAME_MODE_SECRET(self) -> bool:
        
        # Returning:
        return self.__game_mode_secret
    
    
    @property
    def GAME_MODE_REVERSE(self) -> bool:
        
        # Returning:
        return self.__game_mode_reverse
    
    
    @property
    def GAME_MODE_REVEAL(self) -> bool:
        
        # Returning:
        return self.__game_mode_reveal
    

    def set_game_mode_secret(self, set_value: bool, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__game_mode_secret = set_value
        
    
    def switch_game_mode_secret(self) -> None:
    
        # Switching value:
        self.__game_mode_secret = not self.__game_mode_secret

    

    def set_game_mode_reverse(self, set_value: bool, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )

        # Updating attribute:
        self.__game_mode_reverse = set_value


    def switch_game_mode_reverse(self) -> None:

        # Switching value:
        self.__game_mode_reverse = not self.__game_mode_reverse
        
    
    def set_game_mode_reveal(self, set_value: bool, ignore_assertion: bool = False) -> None:
            
        # Assertion control:
        if not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__game_mode_reveal = set_value
        
    
    def switch_game_mode_reveal(self) -> None:
    
        # Switching value:
        self.__game_mode_reveal = not self.__game_mode_reveal

        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DECK CACHED PROPERTIES AND METHODS
    
    """
    
    
    @property
    def DECK_SIZE_DEFAULT(self) -> int:
        
        # Importing SETTINGS instance locally to avoid circular import error:
        from game.settings import SETTINGS
        
        # Returning:
        return SETTINGS.DECK_SIZE_DEFAULT


    @property
    def DECK_SIZE_SELECTED(self) -> int:

        # Returning:
        return self.__deck_size_selected
    
    
    @property
    def DECK_SIZE_MIN(self) -> int:
        
        # Importing SETTINGS instance locally to avoid circular import error:
        from game.settings import SETTINGS
        
        # Returning:
        return SETTINGS.DECK_SIZE_MIN


    @property
    def DECK_SIZE_MAX(self) -> int:

        # Importing SETTINGS instance locally to avoid circular import error:
        from game.settings import SETTINGS

        # Returning:
        return SETTINGS.DECK_SIZE_MAX
    
    
    def set_deck_size(self, set_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            validate.validate_deck_size(
                validate_value = set_value
                )

        # Updating attribute:
        self.__deck_size_selected = set_value

    
    def set_deck_size_default(self) -> None:
        
        # Updating attribute:
        self.set_deck_size(
            set_value = self.DECK_SIZE_DEFAULT,
            ignore_assertion = True
            )
        
    
    def switch_deck_size(self) -> None:
        
        # Selecting deck size to switch to:
        if self.DECK_SIZE_SELECTED == self.DECK_SIZE_MIN:
            deck_size = self.DECK_SIZE_MAX
        else:
            deck_size = self.DECK_SIZE_MIN
        
        # Updating attribute:
        self.set_deck_size(
            set_value = deck_size,
            ignore_assertion = True
            )


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        HAND SORT CACHED PROPERTIES AND METHODS
    
    """
    
    
    @property
    def HAND_SORT_SEQ_DEFAULT(self) -> str:
        
        # Returning:
        return self.__hand_sort_seq_default


    @property
    def HAND_SORT_SEQ_SELECTED(self) -> str:
        
        # Returning:
        return self.__hand_sort_seq_selected
    
    
    @property
    def HAND_SORT_SEQ_REVERSE(self) -> bool:

        # Returning:
        return self.__hand_sort_seq_reverse


    def set_hand_sort_seq(self, set_value: str, set_reverse_value: bool = False, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            validate.validate_hand_sort_seq(
                validate_value = set_value
                )
            validate.validate_flag(
                validate_value = set_reverse_value
                )

        # Updating attribute:
        self.__hand_sort_seq_selected = set_value
        self.__hand_sort_seq_reverse = set_reverse_value

        # Clearing cache:
        self.clear_cached_hand_sort_seq_attributes()
        
    
    def set_hand_sort_seq_default(self) -> None:
        
        # Updating attribute:
        self.set_hand_sort_seq(
            set_value = context.HAND_SORT_SEQ.SUIT,
            set_reverse_value = False,
            ignore_assertion = True
            )


# Creating a session object:
SESSION = __SESSION()

