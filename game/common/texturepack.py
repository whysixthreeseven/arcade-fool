# Typing and annotations:
from __future__ import annotations
from typing import Literal

# External libraries:
import arcade
import random
import pathlib

# Cache management:
from functools import cached_property
from game.utilities.scripts import cache

# Settings, session and context:
from game.common.settings import SETTINGS
from game.common.session import SESSION
from game.common.context import VAR 

# Namespace module
from game.common import namespace

# Utility modules:
from game.utilities.scripts import assertion, validation


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    TEXTURE PACK CLASS CONSTRUCTOR

"""


class _TexturePack:

    def __init__(self) -> None:

        # Core attributes:
        self.__name: str = None
        self.__style: str = None
        self.__color: str = None
        self.__type: str = None


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        NAME ATTRIBUTE PROPERTIES AND METHODS
    
    """


    @property
    def name(self) -> str:

        # Returning:
        return self.__name


    @property
    def name_repr(self) -> str:

        # Raising error, if attribute is not set before call:
        if self.name is None:
            error_message: str = f"Calling name_repr property on texture pack object with no name attribute set!"
            raise AttributeError(error_message)

        # Formatting:
        name_repr: str = self.name.capitalize()

        # Returning:
        return name_repr


    def set_name(
            self, 
            set_value: str, 
            ignore_assertion: bool = False
            ) -> None:

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_is_valid_type(
                check_value = set_value,
                check_type = str,
                raise_error = True,
                custom_error = None
                )

        # Checking multiple setter call:
        if SESSION.DEBUG.ENABLE_DEBUG:
            if self.__name is not None:
                error_message: str = f"Attempting to overwrite existing name attribute: <{self.__name}> to <{set_value}>!"
                raise AttributeError(error_message)
            
        # Updating attribute:
        self.__name: str = set_value


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        STYLE ATTRIBUTE PROPERTIES AND METHODS
    
    """


    @property
    def style(self) -> str:

        # Returning:
        return self.__style


    @property
    def style_repr(self) -> str:

        # Raising error, if attribute is not set before call:
        if self.style is None:
            error_message: str = f"Calling style_repr property on texture pack object with no style attribute set!"
            raise AttributeError(error_message)

        # Formatting:
        style_repr: str = self.style.capitalize()

        # Returning:
        return style_repr


    def set_style(
            self, 
            set_value: str, 
            ignore_assertion: bool = False
            ) -> None:

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            if self.type == VAR.TEXTUREPACK.FRONT.TYPE:
                check_list: tuple[str, ...] = VAR.TEXTUREPACK.FRONT.LIST
            else:
                check_list: tuple[str, ...] = VAR.TEXTUREPACK.BACK.LIST
            assertion.assert_value_is_default(
                check_value = set_value,
                check_list = check_list,
                raise_error = True,
                custom_error = None
                )

        # Checking multiple setter call:
        if SESSION.DEBUG.ENABLE_DEBUG:
            if self.__style is not None:
                error_message: str = f"Attempting to overwrite existing style attribute: <{self.__style}> to <{set_value}>!"
                raise AttributeError(error_message)

        # Updating attribute:
        self.__style: str = set_value


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COLOR ATTRIBUTE PROPERTIES AND METHODS
    
    """


    @property
    def color(self) -> str:

        # Returning:
        return self.__color


    @property
    def color_repr(self) -> str:

        # Raising error, if attribute is not set before call:
        if self.color is None:
            error_message: str = f"Calling color_repr property on texture pack object with no style attribute set!"
            raise AttributeError(error_message)

        # Formatting:
        color_repr: str = self.color.capitalize()

        # Returning:
        return color_repr


    def set_color(self, 
            set_value: str, 
            ignore_assertion: bool = False
            ) -> None:

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            if self.type == VAR.TEXTUREPACK.FRONT.TYPE:
                color_index: dict[str, tuple[str, ...]] = VAR.CONTEXT.TEXTUREPACK.FRONT.INDEX
            else:
                color_index: dict[str, tuple[str, ...]] = VAR.CONTEXT.TEXTUREPACK.FRONT.INDEX
            check_list: tuple[str, ...] = tuple(
                color for style_name, color_list in color_index 
                    for color in color_list
                )
            assertion.assert_value_is_default(
                check_value = set_value,
                check_list = check_list,
                raise_error = True,
                custom_error = None,
                )

        # Updating attribute:
        self.__color = set_value

    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        TYPE ATTRIBUTE PROPERTIES AND METHODS
    
    """

    @property
    def type(self) -> str:

        # Returning:
        return self.__type

    
    @property
    def type_repr(self) -> str:

        # Raising error, if attribute is not set before call:
        if self.type is None:
            error_message: str = f"Calling type_repr property on texture pack object with no type attribute set!"
            raise AttributeError(error_message)

        # Formatting:
        type_repr: str = self.type.capitalize()

        # Returning:
        return type_repr


    def set_type(
            self,
            set_value: str,
            ignore_assertion: bool = False,
            ) -> None:

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            check_list: tuple[str, ...] = (
                VAR.TEXTUREPACK.FRONT.TYPE,
                VAR.TEXTUREPACK.BACK.TYPE,
                )
            assertion.assert_value_is_default(
                check_value = set_value,
                check_list = check_list,
                raise_error = True,
                custom_error = None,
                )
    

""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    TEXTURE PACK (FRONT) CLASS CONSTRUCTOR

"""



class TexturePackFront(_TexturePack):

    def __init__(
            self, 
            init_name: str, 
            init_style: Literal["Dark", "Light", "Sepia"], 
            init_color: Literal["1_1", "2_1", "2_2", "4_1", "4_2", "4_3"]
            ) -> None:

        # Setting type attribute:
        self.__type: str = VAR.TEXTUREPACK.FRONT

        # Updating existing attributes:
        self.set_name(
            set_value = init_name,
            ignore_assertion = False,
            )

        


    @cached_property
    def path(self) -> pathlib.Path:

        texturepack_path: pathlib.Path = SETTINGS.DIR.TEXTURES / "card" / self.__type
