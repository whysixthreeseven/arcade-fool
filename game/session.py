# Random library:
import random

# Texture packs:
from game.utilities.texturepack import (
    TexturePack, 
    TEXTURE_PACK_FRONT, 
    TEXTURE_PACK_BACK, 
    TEXTURE_PACK_FRONT_INDEX, 
    TEXTURE_PACK_BACK_INDEX,
    )


# Cache management:
from functools import cached_property
from game.utilities.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list
    )

# Assertion scripts:
from game.utilities.scripts.assertion import (
    assert_setter_entry,
    assert_value_type,
    assert_value_default,
    assert_value_ge_zero,
    assert_value_not_empty,
    assert_value_in_range,
    )


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    SESSION CLASS OBJECT CONSTRUCTOR
    
"""


class __SESSION:
    
    def __init__(self) -> None:
        
        # Developer options:
        self.__enable_assertion: bool = True
        self.__enable_debug: bool = True
        
        # Texture pack options:
        self.__texture_pack_front_default: TexturePack = TEXTURE_PACK_FRONT.LIGHT_2_1
        self.__texture_pack_front_selected: TexturePack = TEXTURE_PACK_FRONT.LIGHT_2_1
        self.__texture_pack_back_default: TexturePack = TEXTURE_PACK_BACK.PLAIN_WHITE
        self.__texture_pack_back_selected: TexturePack = TEXTURE_PACK_BACK.PLAIN_WHITE
        
        # Game modes:
        self.__game_mode_secret: bool = True
        self.__game_mode_reverse: bool = True
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_debug_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "ENABLE_ASSERTION",
            "ENABLE_DEBUG"
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_texture_pack_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "TEXTURE_PACK_FRONT_SELECTED",
            "TEXTURE_PACK_BACK_SELECTED"
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_game_mode_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "GAME_MODE_SECRET",
            "GAME_MODE_REVERSE"
            )
        
        # Returning:
        return cached_property_list
    
    
    def clear_cached_debug_attributes(self) -> None:
    
        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_debug_attributes
            )
        
    
    def clear_cached_texture_pack_attributes(self) -> None:
        
        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_texture_pack_attributes
            )
        
    
    def clear_cached_game_mode_attributes(self) -> None:
            
        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_game_mode_attributes
            )
        
    
    def clear_cached_attributes(self) -> None:
            
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_debug_attributes,
            self.__cached_texture_pack_attributes,
            self.__cached_game_mode_attributes,
            )
        
        # Looping throught the list and clearing cache:
        for cached_property_list in cached_property_list_collection:
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        VALIDATE METHODS
    
    """
    
    
    def __validate_flag(self, validate_value: bool) -> bool:
        
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = bool,
            raise_error = True,
            )
    
    
    def __validate_texture_pack(self, validate_value: TexturePack) -> bool:
        
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = TexturePack,
            raise_error = True,
            )
        
        # Asserting value is default:
        texture_pack_index: tuple[TexturePack, ...] = TEXTURE_PACK_FRONT_INDEX + TEXTURE_PACK_BACK_INDEX
        assert_value_default(
            check_value = validate_value,
            check_default = texture_pack_index,
            raise_error = True,
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
    
    
    def set_enable_assertion(self, set_value: bool, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if not ignore_assertion:
            self.__validate_flag(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__enable_assertion = set_value
        
        # Clearing cache:
        cached_property: str = "ENABLE_ASSERTION"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        

    def set_enable_debug(self, set_value: bool, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            self.__validate_flag(
                validate_value = set_value
                )

        # Updating attribute:
        self.__enable_debug = set_value

        # Clearing cache:
        cached_property: str = "ENABLE_DEBUG"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
    
    def switch_enable_assertion(self) -> None:
            
            # Switching:
            self.__enable_assertion = not self.__enable_assertion
    
            # Clearing cache:
            cached_property: str = "ENABLE_ASSERTION"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )


    def switch_enable_debug(self) -> None:

        # Switching:
        self.__enable_debug = not self.__enable_debug
        
        # Clearing cache:
        cached_property: str = "ENABLE_DEBUG"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        TEXTURE PACK CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def TEXTURE_PACK_FRONT_DEFAULT(self) -> object:

        # Returning:
        return self.__texture_pack_front_default
    
    
    @cached_property
    def TEXTURE_PACK_FRONT_SELECTED(self) -> object:
        
        # Returning:
        return self.__texture_pack_front_selected
    
    
    @cached_property
    def TEXTURE_PACK_BACK_DEFAULT(self) -> object:

        # Returning:
        return self.__texture_pack_back_default
    

    @cached_property
    def TEXTURE_PACK_BACK_SELECTED(self) -> object:

        # Returning:
        return self.__texture_pack_back_selected
    
    
    def set_texture_pack_front(self, set_value: object, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            self.__validate_texture_pack(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__texture_pack_front_selected = set_value

        # Clearing cache:
        cached_property: str = "TEXTURE_PACK_FRONT_SELECTED"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
        
    def set_texture_pack_front_random(self, clear_cache: bool = True) -> None:
        
        # Selecting random texture pack:
        texture_pack_random: TexturePack = random.choice(TEXTURE_PACK_FRONT_INDEX)
        
        # Updating attribute:
        self.set_texture_pack_front(
            set_value = texture_pack_random,
            ignore_assertion = True,
            clear_cache = clear_cache,
            )
        

    def set_texture_pack_back(self, set_value: object, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            self.__validate_texture_pack(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__texture_pack_back_selected = set_value

        # Clearing cache:
        cached_property: str = "TEXTURE_PACK_BACK_SELECTED"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
            
    
    def set_texture_pack_back_random(self, clear_cache: bool = True) -> None:

        # Selecting random texture pack:
        texture_pack_random: TexturePack = random.choice(TEXTURE_PACK_BACK_INDEX)

        # Updating attribute:
        self.set_texture_pack_back(
            set_value = texture_pack_random,
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
    
    
    def GAME_MODE_REVERSE(self) -> bool:
        
        # Returning:
        return self.__game_mode_reverse
    

    def set_game_mode_secret(self, set_value: bool, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if not ignore_assertion:
            self.__validate_flag(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__game_mode_secret = set_value
        
        # Clearing cache:
        cached_property: str = "GAME_MODE_SECRET"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
    

    def set_game_mode_reverse(self, set_value: bool, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if not ignore_assertion:
            self.__validate_flag(
                validate_value = set_value
                )

        # Updating attribute:
        self.__game_mode_reverse = set_value

        # Clearing cache:
        cached_property: str = "GAME_MODE_REVERSE"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
        
    def switch_game_mode_secret(self) -> None:

        # Switching value:
        self.__game_mode_secret = not self.__game_mode_secret

        # Clearing cache:
        cached_property: str = "GAME_MODE_SECRET"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        

    def switch_game_mode_reverse(self) -> None:

        # Switching value:
        self.__game_mode_reverse = not self.__game_mode_reverse
        
        # Clearing cache:
        cached_property: str = "GAME_MODE_REVERSE"
        clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )


# Creating a session object:
SESSION = __SESSION()

