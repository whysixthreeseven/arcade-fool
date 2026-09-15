# Cache management:
from functools import cached_property
from game.utilities.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list
    )


class __SESSION:
    
    def __init__(self) -> None:
        
        # Developer options:
        self.__enable_assertion: bool = True
        self.__enable_debug: bool = True
        
        # Texture pack options:
        self.__texture_pack_front_default: object = None
        self.__texture_pack_back_default: object = None
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        VALIDATE METHODS
    
    """
    
    
    def __validate_texturepack(self, validate_value: object) -> bool:
        
        # Importing variables:
        from game.utilities.texturepack import TexturePack, TEXTURE_PACK_FRONT, TEXTURE_PACK_BACK
        
        
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
            assert_eval: bool = isinstance(set_value, bool)
            if not assert_eval:
                error_message: str = "Invalid set value, expected boolean!"
                raise AssertionError(error_message)
            
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
            assert_eval: bool = isinstance(set_value, bool)
            if not assert_eval:
                error_message: str = "Invalid set value, expected boolean!"
                raise AssertionError(error_message)

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



# Creating a session object:
SESSION = __SESSION()

