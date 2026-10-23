# External libraries:
from pathlib import Path

# Namespace variables:
from game.common import namespace


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    APP INFORMATION SETTINGS AND MODULES

"""


class _AppSettings:
    NAME: str = "Arcade Fool"
    DESCRIPTION: str = "Fool game created with Python and arcade library"
    DATE_CREATED: str = "2026.09.01"
    DATE_UPDATED: str = "2026.10.22"
    VERSION: str = f"0.0.1.{DATE_UPDATED.replace(".", "")}"
    AUTHOR: str = "Andrey Vostokov"


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    CARD SETTINGS AND MODULES

"""


class _CardTiltModule:
    __DEFAULT: int = 0
    HAND_PLAYER: int = __DEFAULT
    HAND_OPPONENT: int = 180
    TABLE: int = __DEFAULT
    DECK_POS_COMMON: int = __DEFAULT
    DECK_POS_SECRET: int = 270
    DECK_POS_LAST: int = 270
    DECK_PILE_ANGLE_MIN: int = 5
    DECK_PILE_ANGLE_MAX: int = 21
    DECK_PILE_AXIS: tuple[int, int] = (+1, -1)
    RANDOM_ANGLE_MIN: int = 3
    RANDOM_ANGLE_MAX: int = 15
    RANDOM_AXIS: tuple[int, int] = (+1, -1)


class _CardScaleModule:
    LOAD: float = 1.00
    DEFAULT: float = 1.00
    SELECT: float = 1.00


class _CardAlphaModule:
    LOAD: int = 255
    DEFAULT: int = 255
    FADE: int = int(DEFAULT * 0.85)


class _CardDebugModule:
    COLOR_BG: namespace.RGBA_Color = (225, 225, 225, 255)
    COLOR_TEXT: namespace.RGBA_Color = (0, 0, 0, 255)
    FONT_SIZE: int = 14
    FONT_FAMILY: str = "FiraCodeNerdFont-Medium.ttf"


class _CardRenderModule:

    # Related modules:
    TILT = _CardTiltModule()
    SCALE = _CardScaleModule()
    ALPHA = _CardAlphaModule()
    DEBUG = _CardDebugModule()


class _CardTextureModule:
    WIDTH: int = 320
    HEIGHT: int = 480


class _CardSettings:

    # Modules:
    RENDER = _CardRenderModule()
    TEXTURE = _CardTextureModule()
    

""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    DIRECTORY SETTINGS AND MODULES

"""


class _DirectorySettings:

    APP: str = Path(__file__).resolve().parent.parent
    ASSETS: str = APP / "assets"
    SPRITES: str = ASSETS / "sprites"
    TEXTURES: str = ASSETS / "textures"


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    GLOBAL SETTINGS CLASS INSTANCE

"""


class _Settings:

    def __init__(self) -> None:

        # Settings collection:
        self.__app_settings: object = _AppSettings()
        self.__card_settings: object = _CardSettings()
        self.__dir_settings: object = _DirectorySettings()


    @property
    def APP(self) -> _AppSettings:

        # Returning:
        return self.__app_settings


    @property
    def CARD(self) -> _CardSettings:

        # Returning:
        return self.__card_settings


    @property
    def DIR(self) -> _DirectorySettings:

        # Returning:
        return self.__dir_settings


# Initializing settings class object:
SETTINGS = _Settings()

