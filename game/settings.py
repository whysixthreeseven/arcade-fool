# System management:
import os


class __SETTINGS:

    # Root directory settings:    
    DIR_APP: str = os.path.dirname(__file__)
    
    # Directory settings:
    DIR_ASSETS_NAME: str = "assets"
    DIR_ASSETS_PATH: str = os.path.join(DIR_APP, DIR_ASSETS_NAME)
    DIR_TEXTURES_NAME: str = "textures"
    DIR_TEXTURES_PATH: str = os.path.join(DIR_ASSETS_PATH, DIR_TEXTURES_NAME)
    
    # Card render settings:
    CARD_RENDER_SCALE_DEFAULT: float = 1.00
    CARD_RENDER_SCALE_SELECTED_MOD: float = 1.20
    CARD_RENDER_SCALE_SELECTED: float = CARD_RENDER_SCALE_DEFAULT * CARD_RENDER_SCALE_SELECTED_MOD
    CARD_RENDER_SCALE_STEP_MOD_DEFAULT: float = 0.015
    CARD_RENDER_SCALE_STEP_MOD_SELECTED: float = 0.045
    CARD_RENDER_TILT_DEFAULT: int = 0
    CARD_RENDER_TILT_OPP: int = 180
    CARD_RENDER_TILT_DECK: int = 0
    CARD_RENDER_TILT_DECK_BOTTOM: int = 90
    CARD_RENDER_TILT_MIN: int = 3
    CARD_RENDER_TILT_MAX: int = 12
    CARD_RENDER_TILT_AXIS_LIST: tuple[int, int] = (-1, 1)
    CARD_RENDER_TILT_STEP_IN: float = 2.15
    CARD_RENDER_TILT_STEP_OUT: float = 1.75
    CARD_RENDER_ALPHA_DEFAULT: int = 255
    CARD_RENDER_ALPHA_FADED_MOD: float = 0.75
    CARD_RENDER_ALPHA_FADED: int = int(CARD_RENDER_ALPHA_DEFAULT * CARD_RENDER_ALPHA_FADED_MOD)
    CARD_RENDER_ALPHA_STEP_MOD_DEFAULT: float = 0.015
    CARD_RENDER_ALPHA_STEP_MOD_FADED: float = 0.045
    
    # Card texture settings:
    CARD_TEXTURE_SCALE_DEFAULT: float = 0.40
    CARD_TEXTURE_WIDTH_FILE: int = 320
    CARD_TEXTURE_WIDTH: int = int(CARD_TEXTURE_WIDTH_FILE * CARD_TEXTURE_SCALE_DEFAULT)
    CARD_TEXTURE_HEIGHT_FILE: int = 480
    CARD_TEXTURE_HEIGHT: int = int(CARD_TEXTURE_HEIGHT_FILE * CARD_TEXTURE_SCALE_DEFAULT)
    
    # Deck settings:
    DECK_SIZE_MIN: int = 36
    DECK_SIZE_MAX: int = 52
    DECK_SIZE_OPTIONS: tuple[int, int] = (DECK_SIZE_MIN, DECK_SIZE_MAX)
    DECK_SIZE_DEFAULT: int = DECK_SIZE_MIN
        
        
# Initializing settings instance:
SETTINGS = __SETTINGS()

