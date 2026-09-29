# External libraries:
import os

# Settings, session and context:
from game.settings import SETTINGS
from game.session import SESSION
from game import context

# Cache management:
from functools import cached_property
from game.utilities.scripts import cache

# Various utilities:
from game.utilities.scripts import assertion


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
        cache.clear_cached_property_list(
            target_object = self, 
            target_attribute_list = self.__cached_core_attributes
            )
        
    
    def clear_cached_path_attributes(self) -> None:
            
        # Clearing cache:
        cache.clear_cached_property_list(
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
            cache.clear_cached_property_list(
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
        
        
    def set_name(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = str,
                raise_error = True
                )
            assertion.assert_value_not_empty(
                check_value = set_value,
                raise_error = True
                )
            
        # Updating attribute:
        self.__name = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "name"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
        
    
    @cached_property
    def type(self) -> str:
        
        # Returning:
        return self.__type
    
    
    def set_type(self, set_value: str, ignore_assertion = False, clear_cache = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = str,
                raise_error = True
                )
            assertion.assert_value_not_empty(
                check_value = set_value,
                raise_error = True
                )
            default_list: tuple[str, ...] = ("Back", "Front")
            assertion.assert_value_default(
                check_value = set_value.capitalize(),
                check_list = default_list,
                raise_error = True
                )
        
        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "type",
                sentinel_value = None,
                raise_error = True
                )
        
        # Updating attribute:
        self.__type = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "type"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    @cached_property
    def colorcode(self) -> str:
        
        # Returning:
        return self.__colorcode
    
    
    @cached_property
    def __colorcode_front_list(self) -> tuple[str, ...]:
        
        # Returning:    
        return context.CARD_TEXTURE_FRONT_NAME_LIST
    
    
    @cached_property
    def __colorcode_back_list(self) -> tuple[str, ...]:

        # Returning:
        return context.CARD_TEXTURE_BACK_COLOR_LIST
    
    
    @cached_property
    def __colorcode_list(self) -> tuple[str, ...]:
        
        # Returning:
        return self.__colorcode_front_list + self.__colorcode_back_list
        

    def set_colorcode(self, set_value: str, ignore_assertion = False, clear_cache = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = str,
                raise_error = True,
                )
            assertion.assert_value_not_empty(
                check_value = set_value,
                raise_error = True
                )
            default_list: tuple[str, ...] = (colorcode.lower() for colorcode in self.__colorcode_list)
            assertion.assert_value_default(
                check_value = set_value.lower(),
                check_list = default_list,
                raise_error = True
                )
            
        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "colorcode",
                sentinel_value = None,
                raise_error = True
                )

        # Updating attribute:
        self.__colorcode = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "colorcode"
            cache.clear_cached_property(
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
        return context.CARD_TEXTURE_BACK_INDEX
    
    
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
        
        
    def set_style(self, set_value: str, ignore_assertion = False, clear_cache = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = str,
                raise_error = True,
                )
            assertion.assert_value_not_empty(
                check_value = set_value,
                raise_error = True
                )
            assertion.assert_value_default(
                check_value = set_value,
                check_list = self.__style_list,
                raise_error = True
                )
        
        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "style",
                sentinel_value = None,
                raise_error = True
                )
            
        # Updating attribute:
        self.__style = set_value
        
        # Clearing cache:
        if clear_cache:
            cached_property: str = "style"
            cache.clear_cached_property(
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

        # Generating index:
        for card_suit in context.CARD_SUIT_LIST:
            if card_suit not in texture_index:
                texture_index[card_suit] = {}
            for card_name in context.CARD_NAME_LIST:
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


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    TEXTURE PACK COLLECTION (FRONT & BACK)

"""


class TEXTUREPACK_FRONT:
    
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


TEXTUREPACK_FRONT_INDEX: tuple[TexturePack, ...] = tuple(
    attribute_value for attribute_name, attribute_value 
    in TEXTUREPACK_FRONT.__dict__.items()
    if isinstance(attribute_value, TexturePack)
    )
    

# Texture pack collection (back):
class TEXTUREPACK_BACK:

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


TEXTUREPACK_BACK_INDEX: tuple[TexturePack, ...] = tuple(
    attribute_value for attribute_name, attribute_value 
    in TEXTUREPACK_BACK.__dict__.items()
    if isinstance(attribute_value, TexturePack)
    )

