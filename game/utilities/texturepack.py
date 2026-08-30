# Annotations and typing:
from __future__ import annotations

# System management:
import os

# Cache management:
from functools import cached_property
from game.utilities.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list,
    refresh_object,
    )

# Settings and session instances:
from game.settings import SETTINGS
from game.session import SESSION

# Card-related variables:
from game.context import (
    CARD_SUIT,
    CARD_NAME,
    CARD_TEXTURE_FRONT_INDEX,
    CARD_TEXTURE_BACK_INDEX,
    )

# Assertion scripts:
from game.utilities.scripts.assertion import (
    assert_value_type,
    assert_value_default,
    assert_value_not_empty,
    )


class TexturePack:
    
    def __init__(self) -> None:
        
        # Core attributes:
        self.__name: str = None
        self.__type: str = None
        self.__colorcode: str = None
        self.__style: str = None
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CLASS METHODS
    
    """
    
    
    @classmethod
    def create(cls, init_name: str, init_type: str, init_colorcode: str, init_style: str, ignore_assertion: bool = False) -> None:
        
        # Creating texturepack
        texture_pack = TexturePack()
        
        # Adjusting attributes:
        texture_pack.set_name(
            set_value = init_type,
            ignore_assertion = ignore_assertion,
            clear_cache = False,
            )
        texture_pack.set_type(
            set_value = init_type,
            ignore_assertion = ignore_assertion,
            clear_cache = False,
            )
        texture_pack.set_colorcode(
            set_value = init_colorcode,
            ignore_assertion = ignore_assertion,
            clear_cache = False,
            )
        texture_pack.set_style(
            set_value = init_style,
            ignore_assertion = ignore_assertion,
            clear_cache = False,
            )
        
        # Clearing cache:
        texture_pack.clear_cached_attributes()
        refresh_object(
            target_object = texture_pack
            )
        
        # Returning:
        return texture_pack
    
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
        
        
    @cached_property
    def __cached_core_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "name",
            "type",
            "colorcode",
            "style"
            )   
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_path_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "texture_path",
            "texture_index",
            )   
        
        # Returning:
        return cached_property_list
        
        
    def clear_cached_core_attributes(self) -> None:
        
        # Clearing cache:
        clear_cached_property_list(
            target_object = self, 
            target_attribute_list = self.__cached_core_attributes
            )
        
    
    def clear_cached_path_attributes(self) -> None:
            
        # Clearing cache:
        clear_cached_property_list(
            target_object = self, 
            target_attribute_list = self.__cached_path_attributes
            )
        
    
    def clear_cached_attributes(self) -> None:
        
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_core_attributes,
            self.__cached_path_attributes,
            )
        
        # Looping throught the list and clearing cache:
        for cached_property_list in cached_property_list_collection:
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CORE CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def name(self) -> str:
        
        # Returning:
        return self.__name
    
    
    def __valudate_name(self, validate_value: str) -> None:
        
        # Asserting value type:
        assert_value_type(
            check_value = validate_value,
            check_type = str,
            raise_error = True
            )
        
        # Asserting value is not empty:
        assert_value_not_empty(
            check_value = validate_value,
            raise_error = True
            )
        
        
    def set_name(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__valudate_name(
                validate_value = set_value,
                
                )
            
        # Updating attribute:
        self.__name = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "name"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
        
    
    @cached_property
    def type(self) -> str:
        
        # Returning:
        return self.__type
    
    
    def __validate_type(self, validate_value: str) -> None:
        
        # Asserting style is not set prior:
        if self.style is not None:
            error_message: str = f"Attempting to overwrite current type <{self.type}> for TexturePack object!"
            raise AttributeError(error_message)
        
        # Asserting value type:
        assert_value_type(
            check_value = validate_value,
            check_type = str,
            raise_error = True
            )
        
        # Asserting value is not empty:
        assert_value_not_empty(
            check_value = validate_value,
            raise_error = True
            )

        # Asserting value is default:
        default_list: tuple[str, ...] = ("Back", "Front")
        assert_value_default(
            check_value = validate_value.capitalize(),
            check_list = default_list,
            raise_error = True
            )

        
    def set_type(self, set_value: str, ignore_assertion = False, clear_cache = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_type(
                validate_value = set_value,
                )
        
        # Updating attribute:
        self.__type = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "type"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    @cached_property
    def colorcode(self) -> str:
        
        # Returning:
        return self.__colorcode
    
    
    @cached_property
    def __colorcode_front_list(self) -> tuple[str, ...]:
        
        # Generating list:
        colorcode_list: tuple[str, ...] = tuple(
            colorcode for colorcode, index_list
            in CARD_TEXTURE_FRONT_INDEX.__dict__.items()
            if not colorcode.startswith("_") and index_list
            )

        # Returning:    
        return colorcode_list
    
    
    @cached_property
    def __colorcode_back_list(self) -> tuple[str, ...]:

        # Returning:
        return CARD_TEXTURE_BACK_INDEX.COLOR_LIST
    
    
    @cached_property
    def __colorcode_list(self) -> tuple[str, ...]:
        
        # Returning:
        return self.__colorcode_front_list + self.__colorcode_back_list
    
    
    def __validate_colorcode(self, validate_value: str) -> None:
        
        # Asserting style is not set prior:
        if self.colorcode is not None:
            error_message: str = f"Attempting to overwrite current colorcode <{self.colorcode}> for TexturePack object!"
            raise AttributeError(error_message)
        
        # Asserting value type:
        assert_value_type(
            check_value = validate_value,
            check_type = str,
            raise_error = True,
            )
        
        # Asserting value is not empty:
        assert_value_not_empty(
            check_value = validate_value,
            raise_error = True
            )
        
        # Asserting value is default:
        default_list: tuple[str, ...] = (colorcode.lower() for colorcode in self.__colorcode_list)
        assert_value_default(
            check_value = validate_value.lower(),
            check_list = default_list,
            raise_error = True
            )
        

    def set_colorcode(self, set_value: str, ignore_assertion = False, clear_cache = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_colorcode(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__colorcode = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "colorcode"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
        
    @cached_property
    def style(self) -> str:
        
        # Returning:
        return self.__style
    
    
    @cached_property
    def __style_back_list(self) -> tuple[str, ...]:
        
        # Returning:
        return CARD_TEXTURE_BACK_INDEX.STYLE_LIST
    
    
    @cached_property
    def __style_front_list(self) -> tuple[str, ...]:
        
        # Generating list:
        color_count: tuple[int, ...] = (1, 2, 4)
        variant_count: int = 3
        style_list: tuple[str, ...] = tuple(
            f"{color}_{variant}" 
            for color in color_count 
            for variant in range(1, variant_count + 1)
            )
        
        # Returning:
        return style_list


    @cached_property
    def __style_list(self) -> tuple[str, ...]:
        
        # Creating list of styles:
        style_list: tuple[str, ...] = self.__style_back_list + self.__style_front_list

        # Returning:
        return style_list
    

    def __validate_style(self, validate_value: str) -> None:
        
        # Asserting style is not set prior:
        if self.style is not None:
            error_message: str = f"Attempting to overwrite current style <{self.style}> for TexturePack object!"
            raise AttributeError(error_message)

        # Asserting value type:
        assert_value_type(
            check_value = validate_value,
            check_type = str,
            raise_error = True,
            )
        
        # Asserting value is not empty:
        assert_value_not_empty(
            check_value = validate_value,
            raise_error = True
            )

        # Asserting value is default:
        assert_value_default(
            check_value = validate_value,
            check_list = self.__style_list,
            raise_error = True
            )
        
        
    def set_style(self, set_value: str, ignore_assertion = False, clear_cache = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_style(
                validate_value = set_value,
                )
            
        # Updating attribute:
        self.__style = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "style"
            clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
            
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        PATH CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def texture_path(self) -> str:
        
        # Adding all folders in order:
        dir_list: list[str] = ["card", self.type, self.colorcode]
        if self.type == "Front":
            dir_list.append(self.style)
        dir_list: tuple[str, ...] = (dir_name.lower() for dir_name in dir_list)
        
        # Creating path:
        dir_path: str = os.path.join(SETTINGS.DIR_TEXTURES_PATH, *dir_list)
        
        # Returning:
        return dir_path
    
    
    @cached_property
    def texture_index(self) -> dict:

        # Preparing variables:        
        texture_index: dict = {}
        card_suit_list: tuple[str, ...] = tuple(
            attribute_value for attribute_name, attribute_value
            in CARD_SUIT.__dict__.items()
            if not attribute_name.startswith("_")
            )
        card_name_list: tuple[str, ...] = tuple(
            attribute_value for attribute_name, attribute_value
            in CARD_NAME.__dict__.items()
            if not attribute_name.startswith("_")
            )

        # Generating index:
        for card_suit in card_suit_list:
            if card_suit not in texture_index:
                texture_index[card_suit] = {}
            for card_name in card_name_list:
                if card_name not in texture_index[card_suit]:
                    if self.type == "Front":
                        texture_filepath: str = os.path.join(
                            self.texture_path,
                            f"{card_suit.lower()}_{card_name.lower()}.png"
                            )
                    else:
                        texture_filepath: str = os.path.join(
                            self.texture_path,
                            f"{self.style.lower()}.png"
                            )
                    if os.path.exists(texture_filepath):
                        texture_index[card_suit][card_name] = texture_filepath
                    else:
                        error_message: str = f"Unable to locate file <{texture_filepath}>."
                        raise FileNotFoundError(error_message)
                        
        
        # Returning:
        return texture_index        

# Texture pack collection (front):
class TEXTURE_PACK_FRONT:
    
    # Dark texture packs:
    DARK_1_1 = TexturePack.create("Ghost", "Front", "Dark", "1_1")
    DARK_2_1 = TexturePack.create("Phantom", "Front", "Dark", "2_1")
    
    # Light texture packs:
    LIGHT_1_1 = TexturePack.create("Monochrome", "Front", "Light", "1_1")
    LIGHT_2_1 = TexturePack.create("Classic", "Front", "Light", "2_1")
    LIGHT_2_2 = TexturePack.create("Fancy", "Front", "Light", "2_2")
    LIGHT_4_1 = TexturePack.create("Bright", "Front", "Light", "4_1")
    LIGHT_4_2 = TexturePack.create("Colorful", "Front", "Light", "4_2")
    LIGHT_4_3 = TexturePack.create("Candy", "Front", "Light", "4_3")
    
    # Sepia texture packss
    SEPIA_1_1 = TexturePack.create("Washed", "Front", "Sepia", "1_1")
    SEPIA_2_1 = TexturePack.create("Faded", "Front", "Sepia", "2_1")


# Texture pack collection (back):
class TEXTURE_PACK_BACK:

    # Cross style texture pack:
    CROSS_BLUE = TexturePack.create("Cross (Blue)", "Back", "Blue", "Cross")
    CROSS_GREEN = TexturePack.create("Cross (Green)", "Back", "Green", "Cross")
    CROSS_NAVY = TexturePack.create("Cross (Navy)", "Back", "Navy", "Cross")
    CROSS_ORANGE = TexturePack.create("Cross (Orange)", "Back", "Orange", "Cross")
    CROSS_PURPLE = TexturePack.create("Cross (Purple)", "Back", "Purple", "Cross")
    CROSS_RED = TexturePack.create("Cross (Red)", "Back", "Red", "Cross")
    CROSS_WHITE = TexturePack.create("Cross (White)", "Back", "White", "Cross")
    
    # Mountain style texture pack:
    MOUNTAIN_BLUE = TexturePack.create("Mountains (Blue)", "Back", "Blue", "Mountains")
    MOUNTAIN_GREEN = TexturePack.create("Mountains (Green)", "Back", "Green", "Mountains")
    MOUNTAIN_NAVY = TexturePack.create("Mountains (Navy)", "Back", "Navy", "Mountains")
    MOUNTAIN_ORANGE = TexturePack.create("Mountains (Orange)", "Back", "Orange", "Mountains")
    MOUNTAIN_PURPLE = TexturePack.create("Mountains (Purple)", "Back", "Purple", "Mountains")
    MOUNTAIN_RED = TexturePack.create("Mountains (Red)", "Back", "Red", "Mountains")
    MOUNTAIN_WHITE = TexturePack.create("Mountains (White)", "Back", "White", "Mountains")
    
    # Plain (empty) style texture pack:
    PLAIN_BLUE = TexturePack.create("Plain (Blue)", "Back", "Blue", "Plain")
    PLAIN_GREEN = TexturePack.create("Plain (Green)", "Back", "Green", "Plain")
    PLAIN_NAVY = TexturePack.create("Plain (Navy)", "Back", "Navy", "Plain")
    PLAIN_ORANGE = TexturePack.create("Plain (Orange)", "Back", "Orange", "Plain")
    PLAIN_PURPLE = TexturePack.create("Plain (Purple)", "Back", "Purple", "Plain")
    PLAIN_RED = TexturePack.create("Plain (Red)", "Back", "Red", "Plain")
    PLAIN_WHITE = TexturePack.create("Plain (White)", "Back", "White", "Plain")
    
    # Sun style texture pack:
    SUN_BLUE = TexturePack.create("Sun (Blue)", "Back", "Blue", "Sun")
    SUN_GREEN = TexturePack.create("Sun (Green)", "Back", "Green", "Sun")
    SUN_NAVY = TexturePack.create("Sun (Navy)", "Back", "Navy", "Sun")
    SUN_ORANGE = TexturePack.create("Sun (Orange)", "Back", "Orange", "Sun")
    SUN_PURPLE = TexturePack.create("Sun (Purple)", "Back", "Purple", "Sun")
    SUN_RED = TexturePack.create("Sun (Red)", "Back", "Red", "Sun")
    SUN_WHITE = TexturePack.create("Sun (White)", "Back", "White", "Sun")
    
    