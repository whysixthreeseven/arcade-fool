# External libraries:
import random

# Settings, session and context:
from game import context

# Cache management:
from functools import cached_property
from game.utilities.scripts import cache

# Various utilities:
from game.utilities import texturepack
from game.utilities.scripts import assertion, validate


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    SESSION CLASS OBJECT CONSTRUCTOR
    
"""


class __SESSION:
    
    def __init__(self) -> None:
        
        # Developer options:
        self.__enable_assertion: bool = True
        self.__enable_debug: bool = True
        self.__enable_hint: bool = True
        
        # Texture pack options:
        self.__texturepack_front_default: texturepack.TexturePack = texturepack.TEXTUREPACK_FRONT.LIGHT_2_1
        self.__texturepack_front_selected: texturepack.TexturePack = texturepack.TEXTUREPACK_FRONT.LIGHT_2_1
        self.__texturepack_back_default: texturepack.TexturePack = texturepack.TEXTUREPACK_BACK.PLAIN_WHITE
        self.__texturepack_back_selected: texturepack.TexturePack = texturepack.TEXTUREPACK_BACK.PLAIN_WHITE
        
        # Game modes:
        self.__game_mode_secret: bool = True
        self.__game_mode_reverse: bool = False
        self.__game_mode_reveal: bool = False
        
        # Deck size selected:
        self.__deck_size_selected: int = 36
        
        # Hand sort modes:
        self.__hand_sort_seq_default: str = context.HAND_SORT_SEQ.SUIT
        self.__hand_sort_seq_selected: str = context.HAND_SORT_SEQ.SUIT
        self.__hand_sort_seq_reverse: bool = False

        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_debug_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "ENABLE_ASSERTION",
            "ENABLE_DEBUG",
            "ENABLE_HINT",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_texture_pack_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "TEXTUREPACK_FRONT_SELECTED",
            "TEXTUREPACK_BACK_SELECTED"
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_game_mode_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "GAME_MODE_SECRET",
            "GAME_MODE_REVERSE",
            "GAME_MODE_REVEAL",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_deck_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "DECK_SIZE_SELECTED",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_hand_sort_seq_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "HAND_SORT_SEQ_SELECTED",
            "HAND_SORT_SEQ_REVERSE",
            )
        
        # Returning:
        return cached_property_list
    
    
    def clear_cached_debug_attributes(self) -> None:
    
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_debug_attributes
            )
        
    
    def clear_cached_texture_pack_attributes(self) -> None:
        
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_texture_pack_attributes
            )
        
    
    def clear_cached_game_mode_attributes(self) -> None:
            
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_game_mode_attributes
            )
        
    
    def clear_cached_hand_sort_seq_attributes(self) -> None:
        
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_hand_sort_seq_attributes
            )
        
    
    def clear_cached_attributes(self) -> None:
            
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_debug_attributes,
            self.__cached_texture_pack_attributes,
            self.__cached_game_mode_attributes,
            self.__cached_hand_sort_seq_attributes,
            )
        
        # Looping throught the list and clearing cache:
        for cached_property_list in cached_property_list_collection:
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED DEBUG PROPERTIES AND METHODS
    
    """
        
    
    @cached_property
    def ENABLE_ASSERTION(self) -> bool:
        
        # Returning:
        return self.__enable_assertion
    
    
    @cached_property
    def ENABLE_DEBUG(self) -> bool:

        # Returning:
        return self.__enable_debug
    
    
    @cached_property
    def ENABLE_HINT(self) -> bool:

        # Returning:
        return self.__enable_hint
    
    
    def set_enable_assertion(self, set_value: bool, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__enable_assertion = set_value
        
        # Clearing cache:
        cached_property: str = "ENABLE_ASSERTION"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
    
    def switch_enable_assertion(self) -> None:
                
        # Switching:
        self.__enable_assertion = not self.__enable_assertion

        # Clearing cache:
        cached_property: str = "ENABLE_ASSERTION"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        

    def set_enable_debug(self, set_value: bool, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )

        # Updating attribute:
        self.__enable_debug = set_value

        # Clearing cache:
        cached_property: str = "ENABLE_DEBUG"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )


    def switch_enable_debug(self) -> None:

        # Switching:
        self.__enable_debug = not self.__enable_debug
        
        # Clearing cache:
        cached_property: str = "ENABLE_DEBUG"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
        
    def set_enable_hint(self, set_value, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )

        # Updating attribute:
        self.__enable_hint = set_value

        # Clearing cache:
        cached_property: str = "ENABLE_HINT"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
    
    def switch_enable_hint(self) -> None:

        # Switching:
        self.__enable_hint = not self.__enable_hint

        # Clearing cache:
        cached_property: str = "ENABLE_HINT"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        TEXTURE PACK CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def TEXTUREPACK_FRONT_DEFAULT(self) -> object:

        # Returning:
        return self.__texturepack_front_default
    
    
    @cached_property
    def TEXTUREPACK_FRONT_SELECTED(self) -> object:
        
        # Returning:
        return self.__texturepack_front_selected
    
    
    @cached_property
    def TEXTUREPACK_BACK_DEFAULT(self) -> object:

        # Returning:
        return self.__texturepack_back_default
    

    @cached_property
    def TEXTUREPACK_BACK_SELECTED(self) -> object:

        # Returning:
        return self.__texturepack_back_selected
    
    
    def set_texturepack_front(self, set_value: object, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            validate.validate_texturepack(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__texturepack_front_selected = set_value

        # Clearing cache:
        cached_property: str = "TEXTUREPACK_FRONT_SELECTED"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
        
    def set_texturepack_front_random(self, clear_cache: bool = True) -> None:
        
        # Selecting random texture pack:
        texture_pack_random: texturepack.TexturePack = random.choice(texturepack.TEXTUREPACK_FRONT_INDEX)
        
        # Updating attribute:
        self.set_texturepack_front(
            set_value = texture_pack_random,
            ignore_assertion = True,
            clear_cache = clear_cache,
            )
        

    def set_texturepack_back(self, set_value: object, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            validate.validate_texturepack(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__texturepack_back_selected = set_value

        # Clearing cache:
        cached_property: str = "TEXTUREPACK_BACK_SELECTED"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
            
    
    def set_texturepack_back_random(self, clear_cache: bool = True) -> None:

        # Selecting random texture pack:
        texturepack_random: texturepack.TexturePack = random.choice(texturepack.TEXTUREPACK_BACK_INDEX)

        # Updating attribute:
        self.set_texturepack_back(
            set_value = texturepack_random,
            ignore_assertion = True,
            clear_cache = clear_cache,
            )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        GAME MODE CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def GAME_MODE_SECRET(self) -> bool:
        
        # Returning:
        return self.__game_mode_secret
    
    
    @cached_property
    def GAME_MODE_REVERSE(self) -> bool:
        
        # Returning:
        return self.__game_mode_reverse
    
    
    @cached_property
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
        
        # Clearing cache:
        cached_property: str = "GAME_MODE_SECRET"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
    
    def switch_game_mode_secret(self) -> None:
    
        # Switching value:
        self.__game_mode_secret = not self.__game_mode_secret

        # Clearing cache:
        cached_property: str = "GAME_MODE_SECRET"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
    

    def set_game_mode_reverse(self, set_value: bool, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )

        # Updating attribute:
        self.__game_mode_reverse = set_value

        # Clearing cache:
        cached_property: str = "GAME_MODE_REVERSE"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        

    def switch_game_mode_reverse(self) -> None:

        # Switching value:
        self.__game_mode_reverse = not self.__game_mode_reverse
        
        # Clearing cache:
        cached_property: str = "GAME_MODE_REVERSE"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
    
    def set_game_mode_reveal(self, set_value: bool, ignore_assertion: bool = False) -> None:
            
        # Assertion control:
        if not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__game_mode_reveal = set_value
        
        # Clearing cache:
        cached_property: str = "GAME_MODE_REVEAL"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
    
    def switch_game_mode_reveal(self) -> None:
    
        # Switching value:
        self.__game_mode_reveal = not self.__game_mode_reveal

        # Clearing cache:
        cached_property: str = "GAME_MODE_REVEAL"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DECK CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def DECK_SIZE_DEFAULT(self) -> int:
        
        # Importing SETTINGS instance locally to avoid circular import error:
        from game.settings import SETTINGS
        
        # Getting default value:
        deck_size_default: int = SETTINGS.DECK_SIZE_DEFAULT

        # Returning:
        return deck_size_default


    @cached_property
    def DECK_SIZE_SELECTED(self) -> int:

        # Returning:
        return self.__deck_size_selected
    
    
    @cached_property
    def DECK_SIZE_MIN(self) -> int:
        
        # Importing SETTINGS instance locally to avoid circular import error:
        from game.settings import SETTINGS
        
        # Getting min value:
        deck_size_min: int = SETTINGS.DECK_SIZE_MIN

        # Returning:
        return deck_size_min


    @cached_property
    def DECK_SIZE_MAX(self) -> int:

        # Importing SETTINGS instance locally to avoid circular import error:
        from game.settings import SETTINGS

        # Getting max value:
        deck_size_max: int = SETTINGS.DECK_SIZE_MAX

        # Returning:
        return deck_size_max
    
    
    def set_deck_size(self, set_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            validate.validate_deck_size(
                validate_value = set_value
                )

        # Updating attribute:
        self.__deck_size_selected = set_value

        # Clearing cache:
        cached_property: str = "DECK_SIZE_SELECTED"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
    
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
    
    
    @cached_property
    def HAND_SORT_SEQ_DEFAULT(self) -> str:
        
        # Returning:
        return self.__hand_sort_seq_default


    @cached_property
    def HAND_SORT_SEQ_SELECTED(self) -> str:
        
        # Returning:
        return self.__hand_sort_seq_selected
    
    
    @cached_property
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

